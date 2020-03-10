#create list of stations
stations = [
    'USC00519281', 
    'USC00519397', 
    'USC00513117', 
    'USC00519523',
    'USC00516128',
    'USC00514830',
    'USC00511918',
    'USC00517948',
    'USC00518838']

min_max_avg = ["54","85","71.66378066378067"]

#import Flask
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base

from flask import Flask, jsonify

#set-up the sqlite database
engine = create_engine("sqlite:///hawaii.sqlite",convert_unicode=True, echo=False)

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station


#create an app
app = Flask(__name__)

#define the app
@app.route("/")
def home():
    return (
        f"Hello!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():

    session=Session(engine)

    prcp_data = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    prcp_dict = dict(np.ravel(prcp_data))
    return jsonify(prcp_dict)
    


@app.route("/api/v1.0/stations")
def weatherstations():
    return jsonify(stations)



@app.route("/api/v1.0/tobs")
def tobs():
    session=Session(engine)

    tempdata = session.query(Measurement.id, Measurement.station, Measurement.tobs).\
        filter(Measurement.date > '2016-08-22').\
         order_by(Measurement.date.desc()).all()

    session.close()

    return jsonify(tempdata)



@app.route("/api/v1.0/<start>")
def start():

    session=Session(engine)
     """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """

            return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    def calc_temps(start_date, end_date):

    return (calc_temps('2016-09-01','2017-08-23'))

@app.route("/api/v1.0/<start>/<end>")
def startend():
    return jsonify(min_max_avg)

if __name__ == "__main__":
    app.run(debug=True)
