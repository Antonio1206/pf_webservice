from flask import Blueprint, request, jsonify
from pffun import pfwrapper
from common import settings
from xsd import xmlvalidator

v1 = Blueprint('v1', __name__, template_folder='templates')

@v1.route("/setRules/v1", methods=['POST'])
def set_rules():
    try:
        payload = request.get_data()
        xmlvalidator.validate_input(payload)
        pfwrapper.add_rules(payload)
        return ok_message()
    except Exception as e:
        print e
        return error_message(e)

@v1.route("/getRules/v1", methods=['GET'])
def get_rules():
    try:
        result = pfwrapper.get_json_rules()
        if result is not None:
            return ok_message(result)
        else:
            message = {
                'status': 200,
                'message': 'No rules',
            }
            return ok_message(message)
    except Exception as e:
        print e
        return error_message(e)

@v1.route("/flushRule/v1/<rule_id>", methods=['DELETE'])
def flush_rule(rule_id):
    try:
        pfwrapper.remove_single_rule(rule_id)
        return ok_message()
    except Exception as e:
        print e
        return error_message(e)

@v1.route("/flushRules/v1", methods=['DELETE'])
def flush_rules():
    try:
        pfwrapper.delete_rules()
        return ok_message()
    except Exception as e:
        print e
        return error_message(e)

@v1.route("/setQuick/v1", methods=['POST'])
def set_quick():
    try:
        value = request.get_data()
        settings.quick_rules = value
        return ok_message()
    except Exception as e:
        print e
        return error_message(e)

@v1.route("/getQuick/v1", methods=['GET'])
def get_quick():
    try:
        message = {
                'status': 200,
                'message': 'Quick rules: ' + settings.quick_rules,
            }
        return ok_message(message)
    except Exception as e:
        print e
        return error_message(e)

def error_message(error=None):
    message = {
            'status': 500,
            'message': 'Internal server error: ' + str(error),
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp

def ok_message(data=None):
    if data is None:
        message = {
                'status': 200,
                'message': 'OK',
        }
        resp = jsonify(message)
    else:
        resp = jsonify(data)

    resp.status_code = 200

    return resp
