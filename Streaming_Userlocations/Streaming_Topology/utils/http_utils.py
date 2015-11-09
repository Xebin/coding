__author__ = 'xebin'

from flask import Response
import json

def response_json(result, httpCode=200):
    jsonified = json.dumps(result)
    resp = Response(response=jsonified,
                    status=httpCode,
                    mimetype="application/json")
    return resp