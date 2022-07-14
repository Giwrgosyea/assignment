# Line Task Receiver

This application receive london lines and reports any distruptions. Using Requests line discruptions are received. Results are stored using mongodb and mongoengine as ODM.

Each request is represented is pushed as job in Redis Task queue with a schedule timer.

""we might want to schedule a task to run at 1645 ""
Drawback here , I dont schedule cron jobs. If the user wants to schedule a job every at some point.
A possible solution could be APScheduler or AsyncScheduler.

Driven by the excersice the users is queing jobs (fetch line distruptions).

Results are stored in Dict object in Mongo. Sometimes this result empty results or not all objects are presented.So result is only for portaying results.

Build with:

- Flask
- Redis
- Rq
- Python 3.9
- Mongonengine
- Mongo
- Docker

How to run for dev

```
python3 manage.py run 
or
./entrypoint.sh
```

How to run

```
docker-compose up --build when build.
```
