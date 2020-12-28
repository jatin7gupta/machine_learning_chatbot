from .urls import DENTIST_SERVICE_API
import requests


class Dentist:
    def __init__(self):
        self.api_url = DENTIST_SERVICE_API

    def get_dentists(self):
        return requests.get(self.api_url + 'dentists').json()

    def get_dentists_id(self, id):
        return requests.get(self.api_url + f'dentists/{id}').json()

    def get_dentist_by_name(self, doctor_name):
        payload = {'name': doctor_name}
        return requests.get(self.api_url + 'dentists', params=payload).json()


