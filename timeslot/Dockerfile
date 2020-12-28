From alpine:latest
RUN apk add --no-cache py-pip
RUN pip install --upgrade pip

COPY ./timeslot-app /service
WORKDIR /service

RUN apk add --no-cache tzdata
ENV TZ Australia/Sydney

RUN pip3 install -r requirements.txt

EXPOSE 5000

WORKDIR /service/timeslot-service
ENTRYPOINT ["python3"]
CMD ["__init__.py"]