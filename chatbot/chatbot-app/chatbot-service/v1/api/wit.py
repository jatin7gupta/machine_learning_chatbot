import requests
from .credentials import WIT_TOKEN
import datetime
import dateutil.parser
from .UserState import UserState
from .User import User
from .Business import Business
from .Dentist import Dentist
from .TimeSlot import TimeSlot


def parse_get_all_dentists(data):
    answer = 'Here is the list of doctors: '
    list_doctors = []
    for doc in data:
        list_doctors.append(doc['name'])

    answer = answer + ', '.join(list_doctors) + '. Choose one of the doctors'
    return answer


def parse_get_dentists(data, user:User):
    if len(data) == 1:
        answer = f'Amazing, you have selected {data[0]["name"]}. {data[0]["name"]} sees patients in our ' \
                 f'{data[0]["location"]} branch and specializes in ' \
                 f'{data[0]["specialization"]}. We can book you for tomorrow, what time do you suggest?'

        user.selected_doctor = data[0]
        user.select_doctor_stage = True
        user_state.set_user_state(user)
        return answer
    else:
        return 'I could not understand, Please select the doctors from the above list'


def convert_to_time(data):
    datetime_object = datetime.datetime.strptime(data, '%H:%M')
    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)
    tom = today + datetime.timedelta(days=1)
    tom = tom.replace(hour=datetime_object.hour)
    return tom.isoformat()[:-3]


def get_available_timeslots(data):
    answer = 'We do not have that time available, but we can book for '
    l = []
    for d in data:
        l.append(dateutil.parser.isoparse(d).strftime("%d-%b %I:%M:%p"))
    answer = answer + ', '.join(l)
    return answer


user_state = UserState()
business = Business()


def wit(expression, user: User):
    answer = ''

    try:
        result = requests.get('https://api.wit.ai/message?v=20201112&q={}'.format(expression),
                              headers={'Authorization': WIT_TOKEN})
        json_result = result.json()

        if 'intents' in json_result and len(json_result['intents']) and json_result['intents'][0]['name'] == 'greetings' \
                and not user.greetings and 'traits' in json_result and 'wit$bye' not in json_result['traits']:
            user.greetings = True
            user_state.set_user_state(user)
            answer = f'Hello {user.name}, how can I help you?'

        if 'intents' in json_result and len(json_result['intents']) and json_result['intents'][0]['name'] == 'appointment' :
            # cancel appointment
            if 'entities' in json_result and len(json_result['entities']) > 1 and 'cancel:cancel' in json_result['entities']:
                booked_reservation = TimeSlot().get_reservation({'patient': user.name})['data']
                if len(booked_reservation) > 0:

                    l = []
                    for reservation in booked_reservation:
                        l.append(dateutil.parser.isoparse(reservation['datetime']).strftime('%d-%b %I:%M:%p'))
                    answer = f'You have {len(booked_reservation)} booking. {", ".join(l)}' \
                             f' Please mention the time of the reservation which you want to cancel? '
                    user.cancel_booking = True
                    user_state.set_user_state(user)
                else:
                    answer = 'You dont have an appointment with us. Ask for an appointment!'

            # only appointment
            if 'entities' in json_result and 'cancel:cancel' not in json_result['entities'] and not user.ask_for_appointment:
                get_all_available_dentist = business.get_available_doctors()
                answer = parse_get_all_dentists(get_all_available_dentist)
                user.ask_for_appointment = True
                user.show_doctors_list = True
                user_state.set_user_state(user)

        # when doctor is selected
        if ('wit$contact:contact' in json_result['entities']  and json_result['intents'][0]['name'] == 'choose_doctor')  \
                and not user.selected_doctor \
                and not user.select_doctor_stage:
            doctor_name = json_result['entities']['wit$contact:contact'][0]['body']
            get_dentists = Dentist().get_dentist_by_name(doctor_name)
            answer = parse_get_dentists(get_dentists['data'], user)

        # when time in selected
        if 'intents' in json_result and len(json_result['intents']) and json_result['intents'][0]['name'] == 'select_timing':
            # when booking needs to be done
            if user.select_doctor_stage:
                estimated_time = json_result['entities']['wit$datetime:datetime'][0]['value'].split('T')[1][:5]
                tentative_time = convert_to_time(estimated_time)
                available_timeslots_for_doctor = business.get_available_timeslot_dentist(user.selected_doctor['id'])

                if tentative_time in available_timeslots_for_doctor:
                    booking_datetime = dateutil.parser.isoparse(tentative_time).strftime("%d-%b %I:%M:%p")
                    user.timeslot_selected = True
                    user.selected_timeslot = booking_datetime
                    user.selected_timeslot_api = tentative_time
                    answer = f'Great!, we have found the timeslot for you. ' \
                             f'Your appointment with {user.selected_doctor["name"]} at {booking_datetime} ' \
                             f'is ready to be booked, please confirm!'
                else:
                    answer = get_available_timeslots(available_timeslots_for_doctor)

            # when cancel booking needs to be done
            elif user.cancel_booking:
                estimated_time = json_result['entities']['wit$datetime:datetime'][0]['value'].split('T')[1][:5]
                tentative_time = convert_to_time(estimated_time)
                booked_reservation = TimeSlot().get_reservation({'patient': user.name, 'datetime': tentative_time})['data']
                if len(booked_reservation) == 1:
                    answer = f'Your booking at {booked_reservation[0]["datetime"]} is about to be cancelled.'  \
                             f' Please confirm? '
                    user.cancel_booking = True
                    user.cancel_booking_api = booked_reservation[0]
                    user_state.set_user_state(user)
                else:
                    answer = 'I guess you have two appointments at the same time, please contact admin staff for support.'
            else:
                answer = 'you have not selected any doctor yet! try again'

        if 'intents' in json_result and len(json_result['intents']) and json_result['intents'][0]['name'] == 'decision' :
            if 'yes' in json_result['entities']['decision:decision'][0]['value'] and user.selected_doctor and user.timeslot_selected:
                timeslot_api = TimeSlot()
                booking = timeslot_api.create_reservation(user.selected_timeslot_api,
                                                          user.selected_doctor['id'], user.name)
                if booking:
                    answer = f'Great!, Your appointment with {user.selected_doctor["name"]} at ' \
                             f'{user.selected_timeslot} has been confirmed! Your booking id is {booking["id"]}. ' \
                             f'It was nice talking to you.'
                    user.confirm_booking = True
                    user.booking_details = booking
                    user_state.set_user_state(user)
                else:
                    answer = 'There was some error in processing your request,' \
                             ' please try again with maybe different time!)'
            if 'yes' in json_result['entities']['decision:decision'][0]['value'] and user.cancel_booking and user.cancel_booking_api:
                result = TimeSlot().delete_reservation(user.cancel_booking_api['id'])
                if result:
                    answer = 'Your reservation has been cancelled.'
                    user.cancel_booking = False
                    user.cancel_booking_api = None
                    user_state.set_user_state(user)
                    user_state.delete_user_state(user)
                else:
                    answer = 'There was some error in processing your request,'

            if 'no' in json_result['entities']['decision:decision'][0]['value']:
                user_state.delete_user_state(user)
                answer = 'It was nice talking to you, have a nice day! Bye'

        if 'traits' in json_result and 'wit$bye' in json_result['traits'] and answer == '':
            user_state.delete_user_state(user)
            answer = 'bye, see you later!'
    except:
        answer = 'I do not understand, can you try again! :('
    if answer == '':
        answer = 'I do not understand, can you be a little more specific'
    return answer
