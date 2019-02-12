#################################################
# Import dependencies
#################################################

import numpy as np

import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session_factory = sessionmaker(bind=engine)
session = scoped_session(session_factory)
#session = session_factory()

#################################################
# Flask Setup
#################################################
climate_app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@climate_app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        f"For last two urls, enter the dates in yyyy-mm-dd format"
    )


@climate_app.route("/api/v1.0/precipitation")
def prcp():
    """Return a list of precipitation values"""
    
    
    precip=session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date > (dt.date(2017,8,23) - dt.timedelta(days=365))).\
        order_by(Measurement.date).all()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(precip))

    return jsonify(all_prcp)

@climate_app.route("/api/v1.0/stations")
def station_name():
    "Return a list of session names"
    station_results = session.query(Station).all()
    all_stations = []
    for station in station_results:
        station_dict = {}
        station_dict["name"]=station.name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@climate_app.route("/api/v1.0/tobs")
def temp():
    """Return a list of temperature values"""
    temps=session.query(Measurement.date,Measurement.tobs).\
                filter(Measurement.date > (dt.date(2017,8,23) - dt.timedelta(days=365))).\
                order_by(Measurement.date).all()
    all_temp=list(np.ravel(temps))

    return jsonify(all_temp)

@climate_app.route("/api/v1.0/<start>")

def generatestart(start = None):
        starttemp=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        t1=list(np.ravel(starttemp))

        return jsonify(t1)

@climate_app.route("/api/v1.0/<start>/<end>")

def generatestartend(start, end):
    startendtemp=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    t2=list(np.ravel(startendtemp))
    return jsonify(t2)
