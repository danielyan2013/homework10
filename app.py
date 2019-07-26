from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__Climate__)

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect = True)

Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    return (
    f"Welcome to the Home Page!<br/>"
    f"Available Routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/<start><br/>"
    f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def date2prcp(date_param):
    data = engine.execute("SELECT date, prcp FROM Measurement where date =" + date_param + ";")
    list = []
    for record in data:
        list.append(record)
    return jsonify(list)

@app.route("/api/v1.0/stations")
def stations():
    data = engine.execute("SELECT name FROM Stations;")
    list = []
    for record in data:
        list.append(record)
    return jsonify(list)

@app.route("/api/v1.0/tobs")
def tobs():
    data = engine.execute("SELECT date, tobs FROM Measurement where date >= '2016-08-23';")
    list = []
    for record in data:
        list.append(data)
    return jsonify(list)

@app.route("/api/v1.0/<start>")
def start_only(start_date):
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all())

@app.route("/api/v1.0/<start><end>")
def calc_temps(start_date, end_date):
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all())
