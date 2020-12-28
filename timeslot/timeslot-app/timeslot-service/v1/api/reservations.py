# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from v1.util.read_write_file import read_from_file, write_to_file
from v1.api.constants import TIMESLOT_FILE, RESERVATION_FILE
import hashlib
import json


class Reservations(Resource):

    def get(self):
        print(g.headers)
        print(g.args)
        reservation_data = read_from_file(RESERVATION_FILE)
        if len(g.args) == 0:
            return reservation_data, 200, {}
        else:
            reservation_data = reservation_data['data']
            return_list = []
            for r in reservation_data:
                count_match = 0
                for key, value in g.args.items():
                    if key in r and str(r[key]).lower() == str(value).lower():
                        count_match += 1
                if count_match == len(g.args):
                    return_list.append(r)

            result = {
                "data": return_list
            }
            return result, 200, {}

    def post(self):
        print(g.json)
        req = g.json
        # validation
        if 'datetime' in req\
                and 'doctor_id' in req \
                and 'patient' in req \
                and req['datetime'] in read_from_file(TIMESLOT_FILE)['data']:

            reservation_data = read_from_file(RESERVATION_FILE)['data']
            for r in reservation_data:
                if r['datetime'] == req['datetime'] and r['doctor_id'] == req['doctor_id']:
                    return None, 409
            created_reservation = {
                'datetime': req['datetime'],
                'doctor_id': req['doctor_id'],
                'patient': req['patient']
            }
            id = hashlib.shake_256(json.dumps(created_reservation).encode()).hexdigest(3)
            created_reservation['id'] = id
            reservation_data.append(created_reservation)
            write_to_file(RESERVATION_FILE, {'data': reservation_data})
            return {'data': created_reservation}, 201, None
        else:
            return None, 400