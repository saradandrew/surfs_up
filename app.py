# Import datetime, NumPy, and Pandas dependencies
import datetime as dt
import numpy as np
import pandas as pd

# Add SQLAlchemy dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask dependencies
from flask import Flask, jsonify

# Set up the database
engine = create_engine("sqlite:///hawaii.sqlite")

# Relfect database into our classes
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create variable to reference each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create session link
session = Session(engine)

# Define Flask application
app = Flask(__name__)

# Define the welcome route (aka root)
@app.route("/")

# Add routing info for the other routes
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

# Build route for the precipitation analysis
@app.route("/api/v1.0/precipitation")

# Create precipitation function that calculates the date one year ago from the most recent date in the database
# Then get the date and precipitation for the previous year
# Finally, create a dictionary with the date as the key and the precipitation as the value
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

# Define stations route & route name
@app.route("/api/v1.0/stations")

# Create stations function and add query to get all of the stations in our database
# Unravel results into one-dimensional array
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Define temperature route
@app.route("/api/v1.0/tobs")

# Create temp_monthly() function
# Unravel results into one-dimensional array and convert it to a list
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Add a route and provide both a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# Create a function called stats()
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)