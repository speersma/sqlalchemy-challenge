# Import the dependencies.

import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the tables
Base = automap_base()

# Save references to each table
Base.prepare(engine, reflect=True)

# Create our session (link) from Python to the DB
measurement = Base.classes.measurement
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def start():
    return (
        f"Mark's SQL-Alchemy Hawaii Based Weather API<br/>"
        f"Routes<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # link from python to DB
    session = Session(engine)

    # find the most recent date in the dataset
    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    print(most_recent_date)

    # find start and end date for twelve months previosu to most_recent_date
    # then pull precipitation values and date values for that preriod of time
    last_date = dt.datetime.strptime(most_recent_date[0], '%Y-%m-%d').date()
    first_date = last_date - dt.timedelta(days=365)
    last_year_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= first_date).order_by(measurement.date).all()

    # close the session
    session.close()

    # loop through query results and turn into dictionary so it is...
    #...accessible in python
    year_data_dict = {}
    for date, precip in last_year_data:
        year_data_dict[date] = precip

    return jsonify(year_data_dict)

@app.route("/api/v1.0/stations")
def station():

    # link from python to DB
    session = Session(engine)

    # pull all stations 
    station_query = session.query(station.id, station.station, station.name).all()

    # close the session
    session.close()

    # convert query results to list
    station_list = []
    for station_i in station_query:
        station_dict = {}
        station_dict["id"] = station_i[0]
        station_dict["station"] = station_i[1]
        station_dict["name"] = stat[2]

        station_list.append(station_dict)
    
    # return a JSON list of stations
    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    # query the dates and temperature of the omst active station...
    #...for the previous year of data
    most_recent_date = session.query(measurement.date).order_by(measurement.date.desc()).first()
    end_date = dt.datetime.strptime(most_recent_date[0], "%Y-%m-%d").date()
    start_date = end_date - dt.timedelta(days=365)
    last_year_data = session.query(measurement.date, measurement.tobs).filter(measurement.date >= '2017-08-23').filter(measurement.station == 'USC00519281').all()

    # close the session
    session.close()

    # convert query into list of tobs
    tobs_list = []
    for date, tobs in last_year_data:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)
