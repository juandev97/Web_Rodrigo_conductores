from flask import Flask, render_template, request, send_from_directory, url_for, redirect
from sqlalchemy import create_engine
import yaml
import pyodbc
import re
#from flask_mysqldb import flask_mysqldb
#from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

db = yaml.load(open('db.yaml'))

#app.config['MYSQL_HOST'] = db['sql_host']
#app.config['MYSQL_USER'] =  db['sql_user']
#app.config['MYSQL_PASSWORD'] =  db['sql_password']
#app.config['MYSQL_DB'] =  db['sql_db']

SERVER = db['sql_host']
DATABASE =  db['sql_db'] 
DRIVER = 'SQL+Server+Native+Client+11.0'
USERNAME = db['sql_user']
PASSWORD = db['sql_password']

InstanceName = ''

#sql = f'mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?drive=SQL+Server+Native+Client+11.0'
sql = f'mssql+pyodbc://' + SERVER + "\\" + InstanceName + '/' + DATABASE + '?driver=SQL+Server+Native+Client+11.0'

engine = create_engine(sql)


@app.route('/', methods=["GET","POST"])
def index():
    if request.method == 'POST':
        conductor = request.form

        Nombre = conductor['Nombre']
        CC = conductor['CC']
        Direccion = conductor['Direccion']
        Email = conductor['Email']
        propietario = conductor['Propietario']
        tipo_vehiculo = conductor['tipo']
        fecha_cumple = conductor['fecha_cumple']

        email_validator = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        CC_validator = '^[ 0-9]+$'
        


        #path_firma = f"../../../../../../../Downloads/firma_{CC}.jpg"
        path_firma = f"file://C:/Users/Usuario/Downloads/firma_{CC}.jpg"
    
        
        with engine.connect() as connection:
            #print(f"Insert into Datos_conductor( Nombre,CC,Direccion,Email,propietario,tipo_vehiculo,fecha_cumple,path_firma) values(\"{Nombre}\", \"{CC}\" , \"{Direccion}\", \"{Email}\", \"{propietario}\" , \"{tipo_vehiculo}\", {fecha_cumple}, \"{path_firma}\")")
            if(re.search(email_validator,Email) and re.search(CC_validator,CC)):
                connection.execute(f"Insert into Datos_conductor(Nombre,CC,Direccion,Email,propietario,tipo_vehiculo,fecha_cumple,path_firma) values(\'{Nombre}\', \'{CC}\' , \'{Direccion}\', \'{Email}\', {propietario}, \'{tipo_vehiculo}\', \'{fecha_cumple}\', \'{path_firma}\');")
                return render_template('index.html', error="__", e=False)
            else:
                print(len(Email))
                print(len(CC))
                return render_template('index.html', error="El registro ingresado fue invalido, intente de nuevo", e=True)
    #return a
    return render_template('index.html', error="-", e=False)





@app.route('/consultar')
def consultar():
    with engine.connect() as connection:
        result = connection.execute("Select * from Datos_conductor")
        #count = result.scalar()
        conductores = result.fetchall()
        count = len(conductores)
        
        if count > 0:
            return render_template('consultar.html', conductores= conductores)

        else:
            return f"No hay registros {count}"
            
        """for row in result:
            a = a + f"username: {row[1]}"
            print(f"Ahhhhhhhhh {a}")
        """

@app.route('/delete/<int:id>')
def delete(id):
     with engine.connect() as connection:
        connection.execute(f"Delete from Datos_conductor where ID={id}")
        return redirect(url_for('consultar'))

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    if request.method == 'GET':
        with engine.connect() as connection:
            result = connection.execute(f"Select * from Datos_conductor where ID={id}")
            #count = result.scalar()
            conductor = result.fetchall()
            count = len(conductor)
            if count > 0:

                return render_template('update.html',conductor=conductor)

    elif request.method == 'POST':
        conductor = request.form

        Nombre = conductor['Nombre']
        CC = conductor['CC']
        Direccion = conductor['Direccion']
        Email = conductor['Email']
        propietario = conductor['Propietario']
        tipo_vehiculo = conductor['tipo']
        fecha_cumple = conductor['fecha_cumple']

        email_validator = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        CC_validator = '^[ 0-9]+$'
        


        #path_firma = f"../../../../../../../Downloads/firma_{CC}.jpg"
        path_firma = f"file://C:/Users/Usuario/Downloads/firma_{CC}_updated.jpg"
    
        with engine.connect() as connection:
            if(re.search(email_validator,Email) and re.search(CC_validator,CC)):
                connection.execute(f"update Datos_conductor set Nombre = \'{Nombre}\' ,CC = \'{CC}\' ,Direccion = \'{Direccion}\' ,Email = \'{Email}\',propietario = {propietario},tipo_vehiculo = \'{tipo_vehiculo}\' ,fecha_cumple = \'{fecha_cumple}\' ,path_firma = \'{path_firma}\' where ID= {id};")
                return redirect(url_for('consultar'))
            else:
                return render_template('index.html', error="El registro ingresado fue invalido, intente de nuevo", e=True)

            
        

if __name__ == '__main__':
    app.run(debug=True)

