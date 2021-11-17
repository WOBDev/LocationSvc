from flask import Flask
from PointCheck import pointcheck_api

app = Flask(__name__)  
app.register_blueprint(pointcheck_api, url_prefix='/pointcheck') 
#app.register_blueprint(db_api, url_prefix='/dbaccess') 

@app.route("/")  
def hello():  
    return "Welcome to DebrisPro Geo Service!"  
  
if __name__ == "__main__":  
    app.run(host='0.0.0.0',port=5000)  
#Requirements