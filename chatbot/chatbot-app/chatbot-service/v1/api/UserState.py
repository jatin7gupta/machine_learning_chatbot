from flask import current_app
from .User import User
class UserState:
    def __init__(self):
        pass

    def get_user_state(self, name):
        all_users = current_app.users
        for u in all_users:
            if u.name == name:
                return u

    def set_user_state(self, state:User):
        all_users = current_app.users
        found = None
        for index, u in enumerate(all_users):
            if u.name == state.name:
                found = index
            if found is not None:
                break
        current_app.users[found] = state

    def add_new_user(self, user):
        current_app.users.append(user)


    def delete_user_state(self, state: User):
        all_users = current_app.users
        found = None
        for index, u in enumerate(all_users):
            if u.name == state.name:
                found = index
            if found is not None:
                break
        if found is not None:
            all_users.pop(found)
            current_app.users = all_users
