from flask import Flask, render_template, request, send_from_directory, url_for
from sqlalchemy import create_engine
import yaml
import pyodbc
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
        path_firma = "C:/Descargas/firma.jpg"
    
        
        with engine.connect() as connection:
            #print(f"Insert into Datos_conductor( Nombre,CC,Direccion,Email,propietario,tipo_vehiculo,fecha_cumple,path_firma) values(\"{Nombre}\", \"{CC}\" , \"{Direccion}\", \"{Email}\", \"{propietario}\" , \"{tipo_vehiculo}\", {fecha_cumple}, \"{path_firma}\")")
            connection.execute(f"Insert into Datos_conductor(Nombre,CC,Direccion,Email,propietario,tipo_vehiculo,fecha_cumple,path_firma) values(\'{Nombre}\', \'{CC}\' , \'{Direccion}\', \'{Email}\', {propietario}, \'{tipo_vehiculo}\', \'{fecha_cumple}\', \'{path_firma}\');")

    #return a
    return render_template('index.html')





@app.route('/consultar')
def consultar():
    with engine.connect() as connection:
        a = ""
        result = connection.execute("Select * from Datos_conductor")
        for row in result:
            a = a + f"username: {row[1]}"
            print(f"Ahhhhhhhhh {a}")

    return a

if __name__ == '__main__':
    app.run(debug=True)

