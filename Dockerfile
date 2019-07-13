FROM python:3.6-stretch

RUN mkdir /usr/src/email-scheduler

WORKDIR /usr/src/email-scheduler

COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

COPY ./server ./

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"] 