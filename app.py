import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, json, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

#print(Base.classes.keys())

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route("/")
def home():
    print("Homepage Requested")
    return (
        f"Welcome to the Homepage!<br/>!"
        f"Here are the available routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"

    )


@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    most_recent =session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    try:
        prcp_table=[]
        prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=query_date).all()
        for rain in prcp_results:
            prcp_table.append({
                rain.date :rain.prcp
            }
        )
        print("Precipitation Requested")
        return jsonify(prcp_table)
    except:
        print("There was an error. Please try again.")
    finally:
        session.close()


@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    try:
        total_stations = []
        station_results = session.query(Station).all()
        for s in station_results:
            total_stations.append({
                "id" : s.id,
                "station" : s.station,
                "name": s.name,
                "latitude": s.latitude,
                "longitude": s.longitude,
                "elevation": s.elevation
            })
        print("Station List Requested")
        return jsonify(total_stations)
    except:
        print("There was an error. Please try again.")
    finally:
        session.close()

@app.route("/api/v1.0/tobs")
def temps():
    session = Session(engine)
    most_recent =session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)

    try:
        active_station_table=[]
        tobs_results = session.query(Measurement.station,Measurement.date,Measurement.tobs).filter(Measurement.station =="USC00519281").filter(Measurement.date>=query_date).all()
        for t in tobs_results:
            active_station_table.append({
                "station": t.station,
                "date" : t.date,
                "temperature observations": t.tobs
            }
        )
        print("Active Station Tobs Requested")
        return (
            # f"Below are the previous year's temperature observations for station USC00519281<br/>",
            jsonify(active_station_table)
        )
    except:
        print("There was an error. Please try again.")
    finally:
        session.close()
    
@app.route("/api/v1.0/<start>")
def Start_Date_Only(start):
    session= Session(engine)
    low_temp_results = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=start).all()
    high_temp_results= session.query(func.max(Measurement.tobs)).filter(Measurement.date>=start).all()
    avg_temp_results= session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=start).all()
    print("Start Date Requested")
    return jsonify(low_temp_results,high_temp_results,avg_temp_results)
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def endDate(start,end):
    session= Session(engine)
    low_temp_results = session.query(func.min(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<end).all()
    high_temp_results= session.query(func.max(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<end).all()
    avg_temp_results= session.query(func.avg(Measurement.tobs)).filter(Measurement.date>=start).filter(Measurement.date<end).all()
    print("Start Date Requested")
    return jsonify(low_temp_results,high_temp_results,avg_temp_results)

if __name__ =="__main__":
    app.run(debug=True)