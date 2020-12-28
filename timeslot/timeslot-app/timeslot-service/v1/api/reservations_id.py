# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from v1.api.constants import  RESERVATION_FILE
from v1.util.read_write_file import read_from_file, write_to_file


class ReservationsId(Resource):

    def delete(self, id):
        reservation_data = read_from_file(RESERVATION_FILE)['data']
        updated_reservation_data = []
        deleted = False
        for r in reservation_data:
            if id != r['id']:
                updated_reservation_data.append(r)
            else:
                deleted = True

        if deleted:
            write_to_file(RESERVATION_FILE, {'data': updated_reservation_data})
            return None, 204, None
        else:
            return None, 404