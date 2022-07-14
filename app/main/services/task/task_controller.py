import uuid
from datetime import datetime, timedelta

from flask import current_app
from flask_restx import Resource, abort, reqparse
from rq.exceptions import NoSuchJobError

from ...log.logger import Logger
from .task_dto import TaskDto
from .task_service import *

my_logger = Logger(__name__)
logger = my_logger.get_logger()
api = TaskDto.api

parser = reqparse.RequestParser()
parser.add_argument(
    "lines", type=str, help="line1,line2,line3,...", default=None, required=True
)
parser.add_argument(
    "scheduler_time",
    type=str,
    help="Format - YYYY-MM-DDTHH:MM:SS",
    default=None,
    required=False,
)

update_parser = reqparse.RequestParser()

update_parser.add_argument(
    "scheduler_time",
    type=str,
    help="Format - YYYY-MM-DDTHH:MM:SS",
    default=None,
    required=True,
)
update_parser.add_argument(
    "lines", type=str, help="line1,line2,line3,...", default=None, required=False
)
retriever_parser = reqparse.RequestParser()

retriever_parser.add_argument(
    "task_id",
    type=str,
    help="UUID",
    default=None,
    required=False,
)


@api.response(400, "Does Not Exist")
@api.response(200, "Success")
@api.response(500, "Error")
@api.route("/tasks")
class TaskView(Resource):
    """Used for Line Reports"""

    @api.doc("view_task_all")
    def get(self):
        ## search for results

        response = retrieve_all_tasks()

        if response[1] == 200:
            return response[0]
        else:
            abort(response[1], response[0])

    @api.doc("list_of_data_with_dates_as_str")
    @api.expect(parser)
    def post(self):
        args = parser.parse_args()
        job_ids = str(uuid.uuid4())
        if args["scheduler_time"] == None:
            rq_job = current_app.report_queue.enqueue_at(
                datetime.now(),
                line_request,
                scheduled_time=datetime.now(),
                lines=args["lines"],
                job_name=job_ids,
                job_timeout=600,
                result_ttl=0,
                job_id=job_ids,
            )

        else:
            s_time = check_valid_dates(args["scheduler_time"])
            if int(s_time[1]) != 200:
                abort(s_time[1], s_time[0])
            response = find_diff(s_time[0]["start"])
            if response[1] == 200:
                rq_job = current_app.report_queue.enqueue_at(
                    datetime.now() + timedelta(seconds=response[0]),
                    line_request,
                    scheduled_time=datetime.now() + timedelta(seconds=response[0]),
                    lines=args["lines"],
                    job_name=job_ids,
                    job_timeout=600,
                    result_ttl=0,
                    job_id=job_ids,
                )
                logger.info(
                    "will run at: %s", datetime.now() + timedelta(seconds=response[0])
                )

            else:
                abort(response[1], response[0])
        return "Report JOB:" + str(rq_job)


@api.response(500, "Error")
@api.response(400, "Does Not Exist")
@api.response(200, "Success")
@api.route("/tasks/<task_id>")
class SingleTaskView(Resource):
    """Used for Line Reports"""

    @api.doc("view_task")
    @api.expect(retriever_parser)
    def get(self, task_id):
        ## search for results
        # args = retriever_parser.parse_args()

        response = retrieve_specific_completed_task(task_id)
        if response[1] == 200:
            return response[0]
        else:
            abort(response[1], response[0])

    @api.doc("update_task")
    @api.expect(update_parser)
    def patch(self, task_id):

        args = update_parser.parse_args()
        # check if time is valid
        s_time = check_valid_dates(args["scheduler_time"])
        if int(s_time[1]) != 200:
            abort(s_time[1], s_time[0])
        ## check if task exists
        try:
            job = Job.fetch(task_id, connection=current_app.redis)
            current_app.scheduled_registry.remove(job.id)
        except NoSuchJobError as ns:
            abort(400, {"exception:": str(ns)})
        # update_task(task_id, args["scheduler_time"], new_task_id)
        response = find_diff(s_time[0]["start"])
        if response[1] == 200:
            if args["lines"] is None:
                new_rq_job = current_app.report_queue.enqueue_at(
                    datetime.now() + timedelta(seconds=response[0]),
                    line_request,
                    scheduled_time=datetime.now() + timedelta(seconds=response[0]),
                    lines=job.kwargs["lines"],
                    job_name=job.id,
                    job_timeout=600,
                    result_ttl=0,
                    job_id=job.id,
                )
            else:
                new_rq_job = current_app.report_queue.enqueue_at(
                    datetime.now() + timedelta(seconds=response[0]),
                    line_request,
                    scheduled_time=datetime.now() + timedelta(seconds=response[0]),
                    lines=args["lines"],
                    job_name=job.id,
                    job_timeout=600,
                    result_ttl=0,
                    job_id=job.id,
                )
            logger.info(
                "will run at: %s", datetime.now() + timedelta(seconds=response[0])
            )

            return "Report JOB:" + str(new_rq_job)
        else:
            abort(response[1], response[0])
