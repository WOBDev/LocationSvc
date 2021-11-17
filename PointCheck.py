from flask import Blueprint, request
import json
import zipfile
from io import StringIO
import shapefile 
from shapely.geometry import shape, Point
from azure.storage.blob import BlobClient # BlobServiceClient
import os 
from DB import *
import logging


pointcheck_api = Blueprint('pointcheck_api', __name__)

STORAGEACCOUNTURL = "https://devopsrg01diag.blob.core.windows.net"
STORAGEACCOUNTKEY = "MZJPXI8yBZfA8/67P2yJsZFxtVaGSEWuIQ6nrU3Oxm9qtrNwF9F1vWE6vsaxQ9DxYizuc6wefzl1kxjhuMQtuQ=="
CONTAINERNAME = "debrisprostg"
BLOBNAME = ""         # "shape/LaFourcheZONES.zip"
my_connection_string = "DefaultEndpointsProtocol=https;AccountName=devopsrg01diag;AccountKey=MZJPXI8yBZfA8/67P2yJsZFxtVaGSEWuIQ6nrU3Oxm9qtrNwF9F1vWE6vsaxQ9DxYizuc6wefzl1kxjhuMQtuQ==;EndpointSuffix=core.windows.net"


@pointcheck_api.route("/pointcheck")
def checkifInside():
    isPointinShapeFile = False
    try:
        id = request.args.get('id', default = 0, type = int)
        lat = request.args.get('lat', default = 0, type = float)
        lon  = request.args.get('lon', default = 0, type = float)

        BLOBNAME = getShapeFile(id)
    

        blob = BlobClient.from_connection_string(conn_str=my_connection_string, container_name=CONTAINERNAME, blob_name=BLOBNAME)


        with open(BLOBNAME, "wb") as my_blob:
            stream = blob.download_blob()
            data = stream.readall()
            my_blob.write(data)

    
        #Open the zip file 
        zipshape = zipfile.ZipFile(open(BLOBNAME,"rb"))
        shp = shapefile.Reader(
        shp=zipshape.open("ZONES.shp"),
        shx=zipshape.open("ZONES.shx"),
        dbf=zipshape.open("ZONES.dbf"),
        )

        #point = Point(29.7392333,-90.8099107)
        #point = Point(-90.5165969,29.4888085)
        point = Point(lon,lat)

        # get the shapes
        all_shapes = shp.shapes()

        all_records = shp.records()
      
        i = 0

        #Loop through all shapes to check if the point exists in anyone of them. 
        for i in range(len(all_shapes)):
            polygon = all_shapes[i]
            if Point(point).within(shape(polygon)):
                isPointinShapeFile = True

        return json.dumps(isPointinShapeFile)
    except Exception as err:
        return json.dumps(isPointinShapeFile)