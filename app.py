
# Dependencies
import numpy as np
import pandas as pd
import config
import matplotlib.pyplot as plt
import requests
from flask import Flask, jsonify
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


#################################################
# Flask Routes
#################################################

@app.route("/")
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
    latest = pd.read_sql(f'select * from EUR_USD_M5_A_Source limit 10', con=enginerawDB).to_json()
    return latest


@app.route("/RSI")
def RSI_data():
    RSI = pd.read_sql(f'select * from RSI limit 10', con=engineindicatorsDB).to_json()
    return RSI

@app.route("/MACD")
def MACD_data():
    MACD = pd.read_sql(f'select * from MACD limit 10', con=engineindicatorsDB).to_json()
    return MACD


@app.route("/BollBand")
def BB_data():
    BB = pd.read_sql(f'select * from Boll_Bands limit 10', con=engineindicatorsDB).to_json()
    return BB




if __name__ == '__main__':
    app.run(debug=True)