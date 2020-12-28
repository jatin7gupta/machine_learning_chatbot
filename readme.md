# Requirement
* Node
* Python3
* Docker



## Install frontend, type in root project:


```bash 
$ cd chatbot-ui
$ npm install
```

## Run frontend
```bash
$ npm start
```

## Install Backend:
### Install and run chatbot service, type in root project
```bash
$ cd chatbot
$ python3 -m venv ./venv
(*nix) $ source ./venv/bin/activate | (windows) venv\Scripts\activate
```

```bash
$ cd chatbot-app
$ pip3 install -r requirements.txt
$ cd chatbot-service
$ python3 __init__.py
```
Chatbot service app will run on port 5000

### Install and run denstist service, type in root project
```bash
$ cd dentist
$ docker build -t dentist:latest .
$ docker run -p 5001:5000 -t dentist:latest
```

Dentist service app will run on port 5001 for local system

### Install and run timeslot service, type in root project
```bash
$ cd timeslot
$ docker build -t timeslot:latest .
$ docker run -p 5002:5000 -t timeslot:latest
```

Timeslot service app will run on port 5002 for local system

Note: python3 may refer to python in your system

This service is dependent on WIT.AI and its token to work. You also need to train your own WIT.AI uttrances. This biolerplate project will only give you a structure to work with.
