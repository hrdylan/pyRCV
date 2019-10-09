from flask import Flask
from flask import request
from flask_cors import CORS
from io import StringIO
import csv

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/pyRCV', methods=['POST'])
def run_pyRCV():
    data = request.get_data()
    data = data.decode('utf-8')
    csvfile = StringIO(data)
    reader = csv.reader(csvfile)
    for line in reader:
        print(line)
    return 'all good'
