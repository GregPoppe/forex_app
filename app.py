# Dependencies
import numpy as np
import pandas as pd
import config
import matplotlib.pyplot as plt
import requests
from flask import Flask, jsonify, render_template, request
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
DEFAULT_UNIX = 1530791700
signal_field = 'MACD_Signal'
signal_direction = 1

#################################################
# Flask Routes
#################################################

@app.route("/")
def index():
    """List all available api routes."""
    return render_template('index.html')

@app.route("/scatter")
def scatter():
   """List all available api routes."""
   return render_template('index2.html')

@app.route("/terms")
def terms():
   """List all available api routes."""
   return render_template('index3.html')

@app.route("/resources")
def resources():
   """List all available api routes."""
   return render_template('index4.html')



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
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    latest = pd.read_sql(f'select * from EUR_USD_M5_A_Source where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=enginerawDB).to_json(orient='records')
    return latest


@app.route("/latest_short")
def latest_short_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    latest_short = pd.read_sql(f'select * from EUR_USD_M5_A_Source where unix >= {unixObs} - 30000 and unix <= {unixObs}', con=enginerawDB).to_json(orient='records')
    return latest_short




@app.route("/RSI")
def RSI_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    RSI = pd.read_sql(f'select * from RSI where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return RSI

@app.route("/RSI_short")
def RSI_short_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    RSI_short = pd.read_sql(f'select * from RSI where unix >= {unixObs} - 30000 and unix <= {unixObs}', con=engineindicatorsDB).to_json(orient='records')
    return RSI_short

@app.route("/MACD")
def MACD_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    MACD = pd.read_sql(f'select * from MACD where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return MACD

@app.route("/MACD_short")
def MACD_short_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    MACD_short = pd.read_sql(f'select * from MACD where unix >= {unixObs} - 30000 and unix <= {unixObs}', con=engineindicatorsDB).to_json(orient='records')
    return MACD_short

@app.route("/BollBand")
def BB_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    BB = pd.read_sql(f'select * from Boll_Bands where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return BB

@app.route("/Stochastics")
def Stoc_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    Stc = pd.read_sql(f'select * from Stochastics where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return Stc

@app.route("/Williams_R")
def Williams_R_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    WR = pd.read_sql(f'select * from Williams_R where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return WR

@app.route("/ATR")
def ATR_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    ATR = pd.read_sql(f'select * from ATR where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=engineindicatorsDB).to_json(orient='records')
    return ATR

@app.route("/signals")
def sig_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    sig = pd.read_sql(f'select * from signals where unix >= {unixObs} - 30000 and unix <= {unixObs} + 15000', con=enginesignalsDB).to_json(orient='records')
    return sig

@app.route("/strategy_tester")
def tester_data():
   unixObs = request.args.get('ts',DEFAULT_UNIX)
   tester = pd.read_sql(f'select * from strategy_tester where MACD_Signal = 1 limit 1000', con=enginesignalsDB).to_json(orient='records')
   return tester

def getUnixTime(signal_field, signal_direction):
  tester = pd.read_sql(f"select * from strategy_tester where {signal_field} = '{signal_direction}'", con=enginesignalsDB).to_json(orient='records')
  tester = tester.tolist()
  return tester

@app.route("/observations")
def obs_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    signal_field = request.args.get('Ind')
    signal_direction = request.args.get('Dir')
    obs = pd.read_sql(f"select unix from signals where {signal_field} = '{signal_direction}'", con=enginesignalsDB).to_json(orient='records')
    return obs



@app.route("/indexed_change")
def IDX_change_data():
    unixObs = request.args.get('ts',DEFAULT_UNIX)
    test = pd.read_sql(f'select unix from strategy_tester where Change_15Minutes between -5 and 30 and Change_30Minutes between 0 and 30 and Change_2Hours between -20 and 10 and (unix >= {DEFAULT_UNIX} - 300000000 and unix <= {DEFAULT_UNIX} + 10000000)limit 100', con=enginesignalsDB)
    test_list = test['unix'].tolist()
    output = []
    avg = None
    for x in test_list:
        data = pd.read_sql(f'select unix, time, ask_o, ask_c from EUR_USD_M5_A_Source where unix >= {x} limit 24', con=enginerawDB)
        indexer = (data['ask_o'][0] + data['ask_c'][0])
        data['Change'] = 1000*((data['ask_o'] + data['ask_c']) - indexer)
        dict_output =  { 'x':list(data.index),
                    'y':list(data['Change'])
            }
        if avg is None:
            avg = data
        else:
            avg['Change'] += data['Change']

        dict_output =  { 'x':list(data.index),
        'y':list(data['Change'])
        }
        output.append(dict_output)

    output.append({'x': list(avg.index), 'y': list(avg['Change']/len(test_list))})

 
    return jsonify(output)







if __name__ == '__main__':
    app.run(debug=True)