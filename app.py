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
        propietario = conductor['propietario']
        tipo_vehiculo = conductor['tipo_vehiculo']
        fecha_cumple = conductor['fecha_cumple']
        path_firma = conductor['path_firma']
    contador = 0
    print(f"Ehhhhhhh {contador} ")
    
    with engine.connect() as connection:
        result = connection.execute("Select * from Datos_conductor")
        for row in result:
            a = f"username: {row[1]}"
            contador = contador +1
            print(f"Ahhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh {a}")
    
    print(f"Ehhhhhhh {contador}")
    
    #return a
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

