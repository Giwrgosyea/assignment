import rq
from flask import Flask
from flask_bcrypt import Bcrypt
from redis import Redis
from rq.registry import (
    CanceledJobRegistry,
    FinishedJobRegistry,
    ScheduledJobRegistry,
    StartedJobRegistry,
)

from .config import config

flask_bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    flask_bcrypt.init_app(app)
    app.redis = Redis.from_url(app.config["REDIS_URL"])

    app.report_queue = rq.Queue("report_queue", connection=app.redis)
    app.start_registry = StartedJobRegistry(queue=app.report_queue)
    app.finish_registry = FinishedJobRegistry(queue=app.report_queue)
    app.scheduled_registry = ScheduledJobRegistry(queue=app.report_queue)
    app.canceled_registry = CanceledJobRegistry(queue=app.report_queue)
    return app
