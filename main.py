from flask import Flask, request , render_template
from flask import Response
import os
from flask_cors import CORS, cross_origin
from prediction_Validation_Insertion import pred_validation
from trainingModel import trainModel
from training_Validation_Insertion import train_validation
import flask_monitoringdashboard as dashboard
from predictFromModel import prediction

os.putenv('LANG','en_US.UTF-8')
os.putenv('LC_ALL','en_US.UTF-8')

app = Flask(__name__)
dashboard.bind(app)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()

def home():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)