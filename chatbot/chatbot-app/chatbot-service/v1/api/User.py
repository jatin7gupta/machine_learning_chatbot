class User:
    def __init__(self, name):
        self.name = name
        self.greetings= False
        self.ask_for_appointment = False
        self.show_doctors_list= False
        self.select_doctor_stage = False
        self.selected_doctor= None
        self.select_timeslot= False
        self.timeslot_not_available_suggest_other_time= False
        self.timeslot_selected=False
        self.selected_timeslot= None
        self.selected_timeslot_api= None
        self.confirm_booking= False
        self.booking_details = None
        self.cancel_booking= False
        self.cancel_booking_api = None