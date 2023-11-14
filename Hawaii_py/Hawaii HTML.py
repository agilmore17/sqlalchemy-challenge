# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
St = Base.classes.station
Meas = Base.classes.measurement


# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
start_date = '2016-08-23'

@app.route("/")
def welcome():
    return(
        f"<p>Welcome to my Weather API</p>"
        f"<p>Available Paths:</p>"
        f"/api/v1.0/precipitation <br/> Returns a JSON of precipitation data for the dates between 8/23/16 and 8/23/17<br/><br/>"
        f"/api/v1.0/stations <br/> Returns a JSON list of stations from the dataset <br/><br/>"
        f"/api/v1.0/tobs <br/> Returns a JSON list of temperature observations for the dates between 8/23/16 and 8/23/17 <br/><br/>"
        f"/api/v1.0/<date> <br/> Returns a JSON list of the minimum temperature, average temperature, and max temperature for the dates between the given start date and 8/23/2017 <br/><br/>"
        f"/api/v1.0/<start_date>/<end_date> <br/>Returns a JSON list of the minimum temperature, average temperature, and max temperature for the dates between the given start date and end date<br/><br/>"
    )

#precipitation 

@app.route("/api/v1.0/precipitation")
def precipitation():
    annualprecip = session.query(Meas.date, Meas.prcp).filter(Meas.date >= start_date).group_by(Meas.date).all()
    
    precip = {date: prcp for date, prcp in annualprecip}
    
    return jsonify(precip)

#stations

@app.route("/api/v1.0/stations")
def stations():
    output = session.query(St.station, St.name).all()
    stations = list(np.ravel(output))
    return jsonify(stations)

#tobs

@app.route("/api/v1.0/tobs")
def tobs():
    tobs = session.query(Meas.date, Meas.station, Meas.tobs).filter(Meas.date >= start_date).all()
    
    tobs_ravel = list(np.ravel(tobs))
    
    return jsonify(tobs_ravel)

#start date

@app.route('/api/v1.0/<date>')
def startdate(date):
    temp_results = session.query(func.min(Meas.tobs), func.avg(Meas.tobs), func.max(Meas.tobs)).filter(Meas.date >=date).all()
    
    temp_ravel = list(np.ravel(temp_results))
    return jsonify(temp_ravel)

#between dates

@app.route('/api/v1.0/<start_date>/<end_date>')
def sd_ed(start,end):
    range_temp_results = session.query(func.min(Meas.tobs), func.avg(Meas.tobs), func.max(Meas.tobs)).filter(Meas.date >= start).filter(Meas.date <=end).all()
    
    range_ravel = list(np.ravel(range_temp_results))
    
    jsonify(range_ravel)

if __name__ == "__main__":
    app.run(debug=True)