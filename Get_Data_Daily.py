
# Dependencies
import numpy as np
import pandas as pd
import config
import matplotlib.pyplot as plt
import requests
import time
from datetime import date, datetime, timedelta
import json
import dateutil
from time import mktime
from pandas.io.json import json_normalize
from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

# OANDA API Key

api_key =  config.oanda_api
pw = config.sql_pw

#Initialize MySQL Connection

rds_connection_string = f'root:{pw}@127.0.0.1/raw_data_db'
engine = create_engine(f'mysql://{rds_connection_string}')


#set paramaters of data

#Price: A = Ask, B = Bid, M = Midpoint
price = 'A'

#Offset hours: In Hours. Set to 48 for now
offset = 48

#Granularity: S/M/H/D and time interval. Example M5 = 5 minutes
gran = 'M5'

#Pair
pair = 'EUR_USD'


#Get Dates for previous day
end_date = int(time.time()) 
start_date = end_date - 3600*offset




headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}',
}


params = {
    'price': price,
    'from': start_date,
    'to' : end_date,   
    'granularity': gran,
}


response = requests.get(f'https://api-fxpractice.oanda.com/v3/instruments/{pair}/candles', headers=headers, params=params).json()

data = pd.DataFrame.from_dict(json_normalize(response['candles']), orient='columns')
data = data.rename(index = str, columns = 
                   {"ask.l" : "ask_l",
                   "ask.o" : "ask_o",
                   "ask.h" : "ask_h",
                   "ask.c" : "ask_c"})
data['pair'] = pair
data['unix'] = data['time'].apply(lambda x : mktime(dateutil.parser.parse(x).timetuple()))
data['DateTime'] = data['unix'].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%Y-%m-%d-%H-%M'))
data['Yr'] = data['unix'].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%Y'))
data['Mo'] = data['unix'].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%m'))
data['Day'] = data['unix'].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%d'))
data['Hour'] = data['unix'].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%H'))
data['Minute'] = data['unix'].apply(lambda x : datetime.utcfromtimestamp(x).strftime('%M'))
data = data.loc[data['complete'] == True]


table_name_Daily = pair+"_"+gran+"_"+price+"_Daily"
table_name_Source = pair+"_"+gran+"_"+price+"_Source"


#Create Table Name

with engine.connect() as con:
    con.execute(f'drop table if exists {table_name_Daily};')
    con.execute(f'''create table if not exists {table_name_Daily} 
                (ask_c decimal(13,5), 
                ask_h decimal(13,5),
                ask_l decimal(13,5),
                ask_o decimal(13,5),
                complete boolean,
                time varchar(255),
                volume int,
                pair varchar(255),
                unix double,
                DateTime varchar(255),
                Yr double,
                Mo double,
                Day double,
                Hour double,
                Minute double,
                PRIMARY KEY (unix)
                )

;''')

data.to_sql(name=table_name_Daily, con=engine, if_exists='append', index=False)

with engine.connect() as con:
    
    con.execute(f'''INSERT INTO {table_name_Source}
    select {table_name_Daily}.* from {table_name_Daily}
        left join {table_name_Source}
            on {table_name_Daily}.unix = {table_name_Source}.unix
    where {table_name_Source}.unix is null
;''')



