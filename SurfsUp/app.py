from flask import Flask, jsonify

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

# connect to database
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# home route
@app.route("/")
def home():
    return(
        f"<center><h2>Welcome to the Hawaii Climate Analysis Local API!</h2></center>"
        f"<center><h3>Select from one of the available routes:</h3></center>"
        f"<center>/api/v1.0/precipitation</center>"
        f"<center>api/v1.0/stations</center>"
        f"<center>api/v1.0/tobs</center>"
        f"<center>api/v1.0/start/end</center>"
        )

# /api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    # return the previous year's precipitation as a json
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #previousYear

    # Perform a query to retrieve the date and precipitation scores
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= previousYear).all()

    session.close()
    #dictionary with the dates as the key and precipitation (prcp) as the value
    precipitation = {date: prcp for date, prcp in results}
    # convert to a json
    return jsonify(precipitation)

# /api/v1.0/station route
@app.route("/api/v1.0/stations")
def stations():
    # show a list of stations
    # Perform a query to retrieve the names of the stations
    results = session.query(station.station).\
    session.close()

    stationList = list(np.ravel(results))

    # convert to a json and display
    return jsonify(stationList)

# /api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def temperatures():
    #return the previous year temperatures
    # Calculate the date one year from the last date in data set.
    previousYear = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    #previousYear

    #Perform a query to retrieve the temperatures from the most action station from the past year
    results = session.query(measurement.date, measurement.tobs).\
            filter(measurement.station == 'USC00519281').\
            filter(measurement.date >= previousYear).all()
    
    session.close()

    temperatureList = list(np.ravel(results))
    
    # return the list of temperatures
    return jsonify(temperatureList)

# //api/v1.0/start/end and api/v1.0/start routes
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def dateStats(start=None, end=None):

    #select statement
    selection = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    if not end:

        startDate = dt.datetime.strptime(start, "%m%d%Y")

        results = session.query(*selection).filter(measurement.date >= startDate).all()

        session.close()

        temperatureList = list(np.ravel(results))
    
        # return the list of temperatures
        return jsonify(temperatureList)
    
    else:

        startDate = dt.datetime.strptime(start, "%m%d%Y")
        endDate = dt.datetime.strptime(end, "%m%d%Y")

        results = session.query(*selection).filter(measurement.date >= startDate)\
        .filter(measurement.date >= endDate).all()
        

        session.close()







## app launcher
if __name__ == '__main__':
    app.run(debug=True)
