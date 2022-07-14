from datetime import datetime, timedelta

import requests
from app.main.utils.decorator import mongodb_access
from app.main.utils.key_fixer import key_fix, original_key_fix
from flask import current_app
from flask.json import loads
from mongoengine.errors import DoesNotExist
from rq.job import Job

from ...log.logger import Logger

my_logger = Logger(__name__)
logger = my_logger.get_logger()


def line_request(scheduled_time: datetime, lines: str, job_name: str) -> None:
    """Line request , some times this request returns []

    Args:
        scheduled_time (datetime): scheduled time
        lines (str): which lines here support anything , no prior check here
        job_name (str): name of the job to be queried from db
    """
    try:
        logger.info("Task Running... %s %s %s", scheduled_time, lines, job_name)
        response = requests.get("https://api.tfl.gov.uk/Line/" + lines + "/Disruption")
        execution_time = datetime.now()
        logger.info("Response %s:", response.json())
        if response.json() == []:
            response = None
        else:
            response = key_fix(response.json()[0])
        store_line_task(job_name, response, execution_time)
    except Exception as ex:
        raise ex


def check_valid_dates(scheduled_time: str) -> dict:
    # check if date is valid
    try:

        start = datetime.strptime(scheduled_time, "%Y-%m-%dT%H:%M:%S")
        if start < datetime.now():
            response_object = {
                "exception": "Date is less than now time,this will never be excecuted"
            }
            return response_object, 500
        else:
            response_object = {"start": start}
            return response_object, 200
    except Exception as ex:
        response_object = {"exception": str(ex)}
        return response_object, 500


@mongodb_access
def store_line_task(job_id: str, data: dict, execution_time: datetime):
    ## store lines in db
    from app.main.model.line_mode import Lines

    try:
        Lines(task_id=job_id, result=data, executed=execution_time).save()
    except Exception as ex:
        raise ex


@mongodb_access
def retrieve_specific_completed_task(job_id: str) -> dict:
    from app.main.model.line_mode import Lines

    try:
        task = Lines.objects.get(task_id=job_id)
        response_object = loads(Lines.objects(task_id=job_id).first().to_json())
        del response_object["_id"]
        response_object["result"] = original_key_fix(response_object["result"])

        return response_object, 200
    except DoesNotExist:
        response_object = {
            "exception": DoesNotExist("Result Doesnt exist for job:" + job_id)
        }
        return response_object, 400
    except Exception as ex:
        response_object = {"exception": str(ex)}
        return response_object, 500


@mongodb_access
def retrieve_all_tasks() -> dict:
    from app.main.model.line_mode import Lines

    try:
        response_object = loads(Lines.objects.all().to_json())

        all_tasks = dict()
        for i in response_object:
            all_tasks[i["task_id"]] = dict()
            all_tasks[i["task_id"]]["result"] = i["result"]

        # scheduled tasks dont have result yet
        for k in current_app.scheduled_registry.get_job_ids():
            all_tasks[k] = []

        return all_tasks, 200
    except DoesNotExist as dn:
        response_object = {"exception": str(dn)}
        return response_object, 400
    except Exception as ex:
        response_object = {"exception": str(ex)}
        return response_object, 500


def find_diff(scheduled_date: datetime) -> int:
    ## helper to schedule job
    try:
        if scheduled_date < datetime.now():
            response_object = {"exception": "Scheduled date cant be less now"}
            return response_object, 500
        else:
            return int((scheduled_date - datetime.now()).total_seconds()), 200
    except Exception as ex:
        response_object = {"exception": str(ex)}
        return response_object, 500
