# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
import datetime
from v1.util.read_write_file import write_to_file
from v1.api.constants import TIMESLOT_FILE, RESERVATION_FILE
import v1


def get_datetime():
    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    tom = today + datetime.timedelta(days=1)

    ret = []
    for i in range(8):
        ret.append((tom + datetime.timedelta(hours=9+i)).isoformat()[:-3])
    return ret


def generate_data():
    dates = get_datetime()
    data = {
        'data': dates
    }
    return data


def db_init():
    data = generate_data()
    write_to_file(TIMESLOT_FILE, data)
    write_to_file(RESERVATION_FILE, {'data': []})

def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        v1.bp,
        url_prefix='/v1')
    db_init()
    return app


if __name__ == '__main__':
    create_app().run("0.0.0.0",debug=True)