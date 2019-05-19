# Email Automation
Flask server that schedules emails with sendgrid

To start the server run: 
```
docker-compose up --build
```

This will start the server and postgres db. You can now access the server on localhost:5555
To schedule emails you need to make a post request to / with a body consisting of: 

```
{
  "email": "example@gmail.com",
  "date": "2019-05-19T13:38:33.283Z",
  "data": {
    "subject": "Example subject",
    "eg": "Text in Sendgrid email template",
    ...
  }
}
```