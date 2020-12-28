# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
import json
import v1
FILE = "./dentists.json"
HATEOS_VARS = [
        {
          "get": {
            "rel": "self",
            "href": "/dentists/{id}"
          }
        }
      ]
dentist_data = [
    {
        "id": 1,
        "name": "Dr Jhon Doe",
        "location": "Mascot",
        "specialization": "Orthodontics",
        "links": HATEOS_VARS
    },
    {
        "id": 2,
        "name": "Dr Ruby Lyon",
        "location": "Mascot",
        "specialization": "Paediatric Dentistry",
        "links": HATEOS_VARS
    },
    {
        "id": 3,
        "name": "Dr Ho Lin",
        "location": "Kensington",
        "specialization": "Oral Surgery",
        "links": HATEOS_VARS
    }
]


def create_app():
    app = Flask(__name__, static_folder='static')
    app.register_blueprint(
        v1.bp,
        url_prefix='/v1')
    app.dentist_data = dentist_data

    return app


if __name__ == '__main__':
    create_app().run("0.0.0.0", debug=True)