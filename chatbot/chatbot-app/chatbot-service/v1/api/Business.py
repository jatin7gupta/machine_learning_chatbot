from .TimeSlot import TimeSlot
from .Dentist import Dentist

class Business:
    def __init__(self):
        self.timeslot = TimeSlot()
        self.dentist = Dentist()

    def get_available_doctors(self):
        all_dentists = self.dentist.get_dentists()
        all_timeslots = self.timeslot.get_timeslots()['data']

        available_doctors = []
        for dentist in all_dentists['data']:
            dentist_reservation = self.timeslot.get_reservation({'doctor_id': dentist['id']})['data']
            if len(dentist_reservation) < len(all_timeslots):
                available_doctors.append(dentist)
        return available_doctors

    def get_available_timeslot_dentist(self, dentist_id):
        dentist = self.dentist.get_dentists_id(dentist_id)['data']
        all_timeslots = set(self.timeslot.get_timeslots()['data'])
        dentist_reservation = self.timeslot.get_reservation({'doctor_id': dentist['id']})['data']
        set_dentist_reservation = set([e['datetime'] for e in dentist_reservation])
        result = all_timeslots - set_dentist_reservation
        return result


