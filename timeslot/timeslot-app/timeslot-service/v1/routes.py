# -*- coding: utf-8 -*-

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###
from __future__ import absolute_import

from .api.reservations import Reservations
from .api.reservations_id import ReservationsId
from .api.timeslots import Timeslots


routes = [
    dict(resource=Reservations, urls=['/reservations'], endpoint='reservations'),
    dict(resource=ReservationsId, urls=['/reservations/<id>'], endpoint='reservations_id'),
    dict(resource=Timeslots, urls=['/timeslots'], endpoint='timeslots'),
]