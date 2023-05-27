import os
from src.language.constants import *
from flask import Flask, render_template,request,url_for
from src.language.pipeline.prediction_pipeline import SinglePrediction

app = Flask(__name__)

@app.route('/',methods= ['GET',"POST"])
def index():
    if request.method == 'POST':
        search_text = request.form.get('search')
        prediction = SinglePrediction()
        result = prediction.prediction(search_text)
        print(result)
        return render_template("index.html",sentence=search_text,result= result[0])
    return render_template("index.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)