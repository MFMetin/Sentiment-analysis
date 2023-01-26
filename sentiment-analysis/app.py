from flask import Flask,request
from sentiment_analysis import analyze
from flask_cors import CORS, cross_origin



app = Flask(__name__)

cors = CORS(app)

@cross_origin()
@app.route('/')
def hello_world():  # put application's code here
    
    return 'Hello World!'
    
@cross_origin()
@app.route("/analyze", methods=["POST", "GET"])
def analyser():
    if request.method == "POST":

        message = request.json["message"]
        result = analyze(message)
        
        if result[0][0] == 1:         
            return {
                "result": True,
                "message": message      
            }
        elif result[0][0] == 0:
            return {
                "result": False,
                "message": message      
            }
        else:
            return{
                "message" : "Wrong input"
            }

    else:
        return {"message": "Welcome analyser API", "Author": "FurkanMETIN"}


if __name__ == '__main__':
    app.run()
