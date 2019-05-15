FROM python:stretch

RUN mkdir /usr/src/email-scheduler

WORKDIR /usr/src/email-scheduler

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0"] 