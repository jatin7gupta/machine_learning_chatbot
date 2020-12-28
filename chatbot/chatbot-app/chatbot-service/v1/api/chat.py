# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .wit import wit
from .. import schemas
from .UserState import UserState
from .User import User

class Chat(Resource):

    def get(self):
        print(g.args)
        user_states = UserState()
        user = user_states.get_user_state(g.args['user'])
        if user is None:
            user_states.add_new_user(User(g.args['user']))
            user = user_states.get_user_state(g.args['user'])

        answer = wit(g.args['expression'], user)
        return {'answer': answer}, 200, None