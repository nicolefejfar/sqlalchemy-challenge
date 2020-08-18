# Dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Database setup & reflect tables
engine = create_engine('sqlite:///Resources/hawaii.sqlite')
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

# Import & Setup Flask
from flask import Flask, jsonify
app = Flask(__name__)

# Routes
@app.route('/')
def homepage():
    '''List of available api routes.'''
    return (f'Welcome to the Hawaii weather analysis homework API!<br/><br/>'
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/yyyy-mm-dd<br/>'
        f'/api/v1.0/yyyy-mm-dd/yyyy-mm-dd')


# Convert the query results to a dictionary using date as the key and prcp as the value.
@app.route('/api/v1.0/precipitation')
def precip():
    session = Session(engine)
    '''Return precipitation for last year of data'''
    precip_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= '2016-08-23').all()
    session.close()
    precip_list = []
    for date, prcp in precip_data:
        precip_dict = {date:prcp}
        precip_list.append(precip_dict)
    return jsonify(precip_list)

# Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def station():
    session = Session(engine)
    '''Return all stations'''
    station_data = session.query(Station.station, Station.name, Station.latitude,\
        Station.longitude, Station.elevation)
    session.close()
    station_list = []
    for station, name, lat, lon, el in station_data:
        station_dict = {}
        station_dict['station'] = station 
        station_dict['name'] = name 
        station_dict['latitude'] = lat 
        station_dict['longitude'] = lon 
        station_dict['elevation'] = el
        station_list.append(station_dict)
    return jsonify(station_list)

# Query the dates and temperature observations of the most active station for the last year of data.
# Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route('/api/v1.0/tobs')
def tobs():
    session = Session(engine)
    '''Return date & temp of most active station for past year of data'''
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= '2016-08-23').all()
    session.close()
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['temperature'] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date
# When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.

@app.route('/api/v1.0/<start>')
def temp_start(start):
    session = Session(engine)
    '''Return temp min, max, avg for a given start date'''
    temp_data = session.query(func.min(Measurement.tobs),\
        func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()
    temp_list = []
    for data in temp_data:
        temp_dict = {}
        temp_dict['start_date'] = start
        temp_dict['tmin'] = data[0]
        temp_dict['tmax'] = data[1]
        temp_dict['tavg'] = data[2]
        temp_list.append(temp_dict)
    return jsonify(temp_list[0])

# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start-end range.
# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route('/api/v1.0/<start>/<end>')
def temp_range(start, end):
    session = Session(engine)
    '''Return temp min, max, avg for a given start & end date'''
    temp_data = session.query(func.min(Measurement.tobs),\
        func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    session.close()
    temp_list = []
    for data in temp_data:
        temp_dict = {}
        temp_dict['start_date'] = start
        temp_dict['end_date'] = end
        temp_dict['tmin'] = data[0]
        temp_dict['tmax'] = data[1]
        temp_dict['tavg'] = data[2]
        temp_list.append(temp_dict)
    return jsonify(temp_list[0])

# Final Flask Step
if __name__ == '__main__':
    app.run(debug=True)