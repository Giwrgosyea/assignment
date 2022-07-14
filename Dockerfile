FROM python:3.9-slim

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Turn off buffering
ENV PYTHONUNBUFFERED 1

ADD . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

EXPOSE 5001

ENTRYPOINT ["sh", "/app/entrypoint.sh"]
