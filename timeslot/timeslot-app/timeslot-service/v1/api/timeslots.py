# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from v1.util.read_write_file import read_from_file
from v1.api.constants import TIMESLOT_FILE
class Timeslots(Resource):

    def get(self):
        print(g.headers)
        data = read_from_file(TIMESLOT_FILE)
        return data, 200, {}