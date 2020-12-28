# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, current_app

from . import Resource
from .. import schemas


class DentistsId(Resource):

    def get(self, id):
        result = {}
        for d in current_app.dentist_data:
            if d['id'] == id:
                result = {
                    'data': d
                }
        if len(result) == 0:
            return {}, 404
        return result, 200, {}