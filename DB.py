from flask import Blueprint, request
import json
import pyodbc 


#db_api = Blueprint('db_api', __name__)


def getShapeFile(id):
    #id = request.args.get('id', default = 0, type = int)
    cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=tcp:devopssqlsvr01.database.windows.net;' 
                          'DATABASE=sqldb-debrispro-stg01; UID=wobdevopadmin;PWD=V0p5sQL@dm1n!d2;')
    
   
    
    cursor = cnxn.cursor()
    cursor.execute('SELECT ShapeFile FROM tblIncidents WHERE incidentid=?', (id,))

    for row in cursor.fetchall():
        return row.ShapeFile