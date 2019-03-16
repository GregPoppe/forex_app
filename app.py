
# Dependencies
import numpy as np
import pandas as pd
import config
import matplotlib.pyplot as plt
import requests
from flask import Flask, jsonify, render_template
import time
from datetime import date, datetime, timedelta
import json
import dateutil
from time import mktime
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import pymysql
import config
pymysql.install_as_MySQLdb()


pw = config.sql_pw

# Create connention strings

rawDB = f'root:{pw}@127.0.0.1/raw_data_db'
indicatorsDB = f'root:{pw}@127.0.0.1/indicators_db'

enginerawDB = create_engine(f'mysql://{rawDB}')
engineindicatorsDB = create_engine(f'mysql://{indicatorsDB}')



#################################################
# Flask Setup
#################################################
app = Flask(__name__)
unixObs = 1530791700

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """List all available api routes."""
    return render_template('index.html')

@app.route("/routes")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/latest<br/>"
        f"/MACD<br/>"
        f"/RSI<br/>"
        f"/BollBand<br/>"

    )


@app.route("/latest")
def latest_data():
    latest = pd.read_sql(f'select * from EUR_USD_M5_A_Source where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=enginerawDB).to_json(orient='records')
    return latest


@app.route("/RSI")
def RSI_data():
    RSI = pd.read_sql(f'select * from RSI where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return RSI

@app.route("/MACD")
def MACD_data():
    MACD = pd.read_sql(f'select * from MACD where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return MACD


@app.route("/BollBand")
def BB_data():
    BB = pd.read_sql(f'select * from Boll_Bands where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return BB




if __name__ == '__main__':
    app.run(debug=True)