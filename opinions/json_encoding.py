from flask import current_app
from flask.json import JSONEncoder
from flask.json import JSONDecoder
import rapidjson


class CustomJSONEncoder(JSONEncoder):
    encode = rapidjson.Encoder(
        skip_invalid_keys=False,
        ensure_ascii=True,
        indent=None,
        sort_keys=False,
        number_mode=rapidjson.NM_NATIVE,
        datetime_mode=rapidjson.DM_ISO8601,
        uuid_mode=rapidjson.UM_CANONICAL)


class CustomJSONDecoder(JSONDecoder):
    decode = rapidjson.Decoder(
        number_mode=rapidjson.NM_NATIVE,
        datetime_mode=rapidjson.DM_ISO8601,
        uuid_mode=rapidjson.UM_CANONICAL)


def jsonify(json_obj):
    """
    Custom jsonify based on Flask because
    we find the behavior of `jsonify` weird
    because it doesn't match json.dumps.

    https://github.com/pallets/flask/blob/
        7fdd0df6eca5fc564443acbf9f71555f6834359a/src/flask/json/__init__.py#L306
    """
    return current_app.response_class(
        CustomJSONEncoder.encode(json_obj) + "\n",
        mimetype=current_app.config["JSONIFY_MIMETYPE"],
    )
