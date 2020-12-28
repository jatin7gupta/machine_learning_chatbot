from .urls import TIMESLOT_SERVICE_API
import requests
import json


class TimeSlot:
    def __init__(self):
        self.api_url = TIMESLOT_SERVICE_API

    def get_reservation(self, args):
        payload = {}
        for key, value in args.items():
            payload[key] = value
        # if doctor_id and datetime:
        #     payload['doctor_id'] = doctor_id
        #     payload['datetime'] = datetime
        # elif doctor_id:
        #     payload['doctor_id'] = doctor_id
        # elif datetime:
        #     payload['datetime'] = datetime

        return requests.get(self.api_url + 'reservations', params=payload).json()

    def create_reservation(self, datetime, doctor_id, patient):
        body = {
            "datetime": datetime,
            "doctor_id": doctor_id,
            "patient": patient
        }
        r = requests.post(self.api_url + 'reservations', json=body)
        if r.status_code == 201:
            return r.json()['data']
        else:
            return None

    def delete_reservation(self, id):
        r = requests.delete(self.api_url + 'reservations/' + f'{id}')
        if r.status_code == 204:
            return True
        else:
            return False

    def get_timeslots(self):
        return requests.get(self.api_url + 'timeslots').json()