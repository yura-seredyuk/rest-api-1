from flask import Flask, jsonify, request
import sqlalchemy as db
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

client = app.test_client()

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()

from models import *

Base.metadata.create_all(bind=engine)


@app.route('/data', methods=['GET'])
def get_list():
    info = Info.query.filter().all()

    serialized = []
    for item in info:
        serialized.append({
            'id': item.id,
            'title': item.title,
            'description': item.description
        })
    return jsonify(serialized)


@app.route('/data', methods=['POST'])
def update_data():
    new_one = Info(**request.json)
    session.add(new_one)
    session.commit()
    serialized = {
        'id': new_one.id,
        'title': new_one.title,
        'description': new_one.description
    }
    return jsonify(serialized)


@app.route('/data/<int:data_id>', methods=['PUT'])
def update_item(data_id):
    item = Info.query.filter(Info.id == data_id).first()
    params = request.json
    if not item:
        return {'message':'No data with this id'}, 400
    for key, value in params.items():
        setattr(item, key, value)
    session.commit()
    serialized = {
        'id': item.id,
        'title': item.title,
        'description': item.description
    }
    return serialized


@app.route('/data/<int:data_id>', methods=['DELETE'])
def delete_item(data_id):
    item = Info.query.filter(Info.id == data_id).first()
    if not item:
        return {'message':'No data with this id'}, 400
    session.delete(item)
    session.commit()
    return '', 204

@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000')