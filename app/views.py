import csv
import io
from flask import render_template
from app import app
from app.models import Track

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/artists_overview', methods=['GET'])
def artists_overview():
    return render_template('artists_overview.html')