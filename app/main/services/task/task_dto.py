from flask_restx import Namespace


class TaskDto:
    api = Namespace(name="", description="Task related operations")
