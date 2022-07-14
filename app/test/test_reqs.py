import uuid

import requests
from app.main.model.line_mode import Lines

# should also check json's respone


def test_discruption():
    for l in [
        "bakerloo",
        "central",
        "circle",
        "district",
        "hammersmith-city",
        "jubilee",
        "metropolitan",
        "northern",
        "piccadilly",
        "victoria",
        "waterloo-city",
    ]:
        response = requests.get("https://api.tfl.gov.uk/Line/" + l + "/Disruption")
        assert response.status_code == 200


def test_new_lines():
    uid = str(uuid.uuid4())
    result = Lines(
        task_id=uid,
        result={
            "$type": "Tfl.Api.Presentation.Entities.Disruption,Tfl.Api.Presentation.Entities",
            "category": "RealTime",
            "type": "lineInfo",
            "categoryDescription": "RealTime",
            "description": "Jubilee Line: Severe delays due to an earlier faulty train.Tickets will be accepted on local bus services, the Docklands Light Railway, Southeastern,C2C and Greater Anglia and Thameslink.",
            "affectedRoutes": [{"a": "b", "via": {"orin": 0}}],
            "affectedStops": [],
            "closureText": "severeDelays",
        },
    )
    assert result.task_id == uid
