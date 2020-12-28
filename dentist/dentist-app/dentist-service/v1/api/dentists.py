# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g, current_app

from . import Resource
from .. import schemas


class Dentists(Resource):

    def get(self):
        print(g.args)
        result = {}
        arg = 'name'
        if len(g.args) > 0:
            if arg in g.args:
                for d in current_app.dentist_data:
                    if g.args[arg].lower() in d['name'].lower():
                        result = {
                            'data': [d]
                        }
            else:
                return 400
        else:
            result = {
                'data': current_app.dentist_data
            }
        return result, 200, {}