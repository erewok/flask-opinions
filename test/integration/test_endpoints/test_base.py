"""
test_base.py

Test base endpoints
"""
import datetime
import uuid

from opinions import json_encoding as json


def test_index(client):
    """obvious"""
    response = client.get('/')
    assert b"opinions" in response.data


def test_health(client):
    """obvious"""
    response = client.get('/health')
    assert b"ok" == response.data


def test_json(client, json_ct, config, mocklog):

    payload = {"uuid": uuid.uuid4(),
               "datetime": datetime.datetime.utcnow()}

    data = json.CustomJSONEncoder().encode(payload)
    response = client.post("/json", headers=json_ct, data=data)

    assert response.status_code == 200

    result = json.CustomJSONDecoder.decode(response.data.decode())
    assert result["status"] == "success"
    assert result["message"] == "JSON Payload encoded with rapidjson"
    assert result["version"] == config.version
    assert isinstance(result["uuid_example"], uuid.UUID)
    assert result["datetime_example"] > payload["datetime"]

    # check logging calls were as expected
    assert mocklog.method_calls
    assert mocklog.method_calls[0][0] == "info"
    assert mocklog.method_calls[0][1][0] == "JSON received"
    assert mocklog.method_calls[0][2]["uuid"] == str(payload["uuid"])
