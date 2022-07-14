# app/__init__.py

from flask import Blueprint
from flask_restx import Api

from .main.services.task.task_controller import api as task_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="FLASK RESTPLUS API BOILER-PLATE WITH JWT",
    version="1.0",
    description="a boilerplate for flask restplus web service",
)

api.add_namespace(task_ns, "")
