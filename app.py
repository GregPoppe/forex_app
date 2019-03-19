
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
signalsDB = f'root:{pw}@127.0.0.1/signals_db'


enginerawDB = create_engine(f'mysql://{rawDB}')
engineindicatorsDB = create_engine(f'mysql://{indicatorsDB}')
enginesignalsDB = create_engine(f'mysql://{signalsDB}')



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


@app.route("/latest_short")
def latest_short_data():
    latest_short = pd.read_sql(f'select * from EUR_USD_M5_A_Source where unix >= {unixObs} - 30000 and unix <= {unixObs}', con=enginerawDB).to_json(orient='records')
    return latest_short




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


@app.route("/Stochastics")
def Stoc_data():
    Stc = pd.read_sql(f'select * from Stochastics where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return Stc

@app.route("/Williams_R")
def Williams_R_data():
    WR = pd.read_sql(f'select * from Williams_R where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return WR


@app.route("/ATR")
def ATR_data():
    ATR = pd.read_sql(f'select * from ATR where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return ATR



@app.route("/signals")
def sig_data():
    sig = pd.read_sql(f'select * from signals where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=enginesignalsDB).to_json(orient='records')
    return sig


if __name__ == '__main__':
    app.run(debug=True)