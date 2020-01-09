# Import Dependencies

import os

import pandas as pd
import numpy as np
from datetime import datetime

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


#################################################
# Database Setup
#################################################

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/etfiso.sqlite"
db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
etf_table = Base.classes.etf_data


@app.route('/')
def index():
    """Return the homepage."""
    return render_template('index.html')

@app.route("/ticker")
def ticker():
    """Return a list of unique tickers."""

    sel = [
        etf_table.ticker
    ]
    results = db.session.query(*sel).all()
# Dictionary entry for each row of information 
    tickers = []

    for r in results:
        ticker = r
        tickers.append(ticker)
    # print(tickers)

# Removing duplicate ticker symbols    
    seen = set()
    unique_ticker = []
    # print(tickers)
    for t in tickers:
        if t not in seen:
            seen.add(t)
            unique_ticker.append(t)

    # print(unique_ticker)

    unique_tickers = []
    no = 0
    for t in unique_ticker:
        etfs = {}
        etfs["ticker"] = t
        no = no + 1
        etfs["id"] = no
        unique_tickers.append(etfs)

    return jsonify(unique_tickers)


@app.route("/line_graph/<etf>")
def line_graph(etf):
    """Return information to create a line graph."""

    sel = [
        etf_table.date,
        etf_table.close,
        etf_table.ticker
    ]

    results = db.session.query(*sel).filter(etf_table.ticker == etf).all()
    # print(results)

    etf_stats = []
    # date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%d')
    for r in results:
        etf = {}
        # etf["date"] = date_time_obj.date(r[0])
        # etf["date"] = datetime.strptime(r[0],'%Y-%m-%d')
        etf["date"] = r[0]
        etf["close"] = r[1]
        etf["ticker"] = r[2]
        etf_stats.append(etf)


    # test = [{"close":111,"date":"2015-01-01","ticker":"SPY"}]
    # return jsonify(test)  
    return jsonify(etf_stats)




####################################################
#####                TEST ROUTE                #####
####################################################

@app.route("/test")
def daily():
    """Return data for a line graph of performance"""

    sel = [
        # etf_table.date,
        # etf_table.ticker,
        etf_table.close

    ]

    # results = db.session.query(*sel).filter(daily_etf.date).all()
    results = db.session.query(*sel).all()
    # print(results)

    # Dictionary entry for each row of information 
    tickers = []
    # dates = []


    for r in results:
        etfs ={}
        etfs["ticker"] = r[0]
        # etfs["close"] = r[1]
        # datetime_object = dt.strptime(r,'m%/d%/Y%')
        # etfs["date"] = r
        # tickers.append(etfs)
        # dates.append(etfs)
        # ticker = r
        tickers.append(etfs)

    # removing duplicate values    
    # seen = set()
    # unique_ticker = []
    # print(tickers)
    # for t in tickers:
    #     if t not in seen:
    #         seen.add(t)
    #         unique_ticker.append(t)

    return jsonify(tickers)
    # return jsonify(dates)


# @app.route("/test_graph/<etf>")
# def test_graph(etf):
#     """Return information to create a line graph."""
#     sel = [
#         etf_table.date,
#         etf_table.close,
#         etf_table.ticker
#     ]
#     results = db.session.query(*sel).filter(etf_table.ticker == etf).all()
#     # print(results)
#     etf_stats = []
#     for r in results:
#         etf = {}
#         etf["datum"] = r[0]
#         etf["close"] = r[1]
#         etf["ticker"] = r[2]
#         etf_stats.append(etf)
#     ###########
#     test = [{"close":111,"datum":"2015-01-01","ticker":"SPY"}]
#     return jsonify(test)
    #return jsonify(etf_stats)
    ##########


if __name__ == "__main__":
    app.run()