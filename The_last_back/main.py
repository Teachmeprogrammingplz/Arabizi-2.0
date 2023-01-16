from flask import Flask, request
from Functions import Predict_Root
app = Flask(__name__)
# Members API Route
@app.route("/root",methods=['GET'])
def Predict():
    text = request.args.get('text')
    return Predict_Root(text)
    # return text
if __name__== '__main__':
    app.run()
