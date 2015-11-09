__author__ = 'xebin'

from logentries import LogentriesHandler
import logging
from ..config import LOGENTRIES_TOKEN

import json

from flask import Flask

log = logging.getLogger('logentries')
log.setLevel(logging.INFO)
# Note if you have set up the logentries handler in Django, the following line is not necessary
log.addHandler(LogentriesHandler(LOGENTRIES_TOKEN))


def log_is_alive(req_id):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['api_name'] = 'is_alive'

    log.info(json.dumps(log_prop))


def log_check_location(req_id, uid, result):
    log_prop = {}
    log_prop['api_name'] = 'check_trace'
    log_prop['X-request-Id'] = req_id
    log_prop['user_id'] = uid
    log_prop['result'] = result

    log.info(json.dumps(log_prop))


def log_daily_cluster(req_id, new_u_poi_user, user_enough_data, user_not_enought_data, ts_start, ts_end):
    # TODO daily cluster log should be separated by user, not log all new u pois at once
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['api_name'] = 'daily_cluster'
    log_prop['new_u_poi_user'] = new_u_poi_user
    log_prop['user_enough_data'] = user_enough_data
    log_prop['user_not_enough_data'] = user_not_enought_data
    log_prop['ts_start'] = ts_start
    log_prop['ts_end'] = ts_end

    log.info(json.dumps(log_prop))


def log_daily_cluster_poi_request(daily_cluster_req_id, poi_req_id):
    log_prop = {}
    log_prop['api_name'] = 'daily_cluster'
    log_prop['X-request-Id-daily_cluster'] = daily_cluster_req_id
    log_prop['X-request-Id-poi'] = poi_req_id

    log.info(json.dumps(log_prop))


def log_daily_profile(req_id, user_profile_gb_uid):
    log_prop = {}
    log_prop['api_name'] = 'daily_profile'
    log_prop['X-request-Id'] = req_id

    log_prop['daily_profile_result'] = user_profile_gb_uid

    log.info(json.dumps(log_prop))


def log_get_u_pois(req_id, uid, u_poi_ids):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['api_name'] = 'u_pois'
    log_prop['user_id'] = uid
    log_prop['u_pois'] = u_poi_ids

    log.info(json.dumps(log_prop))


def log_get_u_pois_days_stats(req_id, uid, days, stats):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['api_name'] = 'u_pois_7days_stats'
    log_prop['user_id'] = uid
    log_prop['days'] = days
    log_prop['stats'] = stats

    log.info(json.dumps(log_prop))


def log_user_profile(req_id, uid, profile):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['user_id'] = uid
    log_prop['user_profile'] = profile

    log.info(json.dumps(log_prop))


def log_user_home_office_status_prediction(req_id, uid, user_location_id, prediction, is_updated):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['user_id'] = uid
    log_prop['user_location_id'] = user_location_id
    log_prop['prediction'] = prediction
    log_prop['is_updated'] = is_updated

    log.info(json.dumps(log_prop))


def log_get_user_travel_status(req_id, uid, result):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['user_id'] = uid
    log_prop['result'] = result

    log.info(json.dumps(log_prop))


def warn_wrong_visit_log(req_id, visit_log_id, error_msg):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['u_poi_visit_log_id'] = visit_log_id
    log_prop['exception_message'] = error_msg

    log.warn(log_prop)


def warn_wrong_user_location(req_id, user_location_id, error_msg):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['user_location_id'] = user_location_id
    log_prop['exception_message'] = error_msg

    log.warn(log_prop)


def warn_no_poi_u_poi(req_id, u_poi_id):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['u_poi_id'] = u_poi_id
    log_prop['exception_message'] = 'u poi does not have a poi'

    log.warn(log_prop)


def warn_user_home_office_absence(req_id, uid, message):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['user_id'] = uid
    log_prop['message'] = message

    log.warn(log_prop)


def warn_unknown_status(req_id, uid, user_location_id,motion_status,
                        home_visit_log_id, office_visit_log_id, conditions):
    log_prop = {}
    log_prop['X-request-Id'] = req_id

    log_prop['api_name'] = 'status'
    log_prop['user_id'] = uid
    log_prop['user_location_id'] = user_location_id
    log_prop['motion_status'] = motion_status
    log_prop['home_visit_log_id'] = home_visit_log_id
    log_prop['office_visit_log_id'] = office_visit_log_id
    log_prop['conditions'] = conditions

    log.warn(log_prop)

def warn_avg_stats_not_complete(req_id, upoiid):
    log_prop = {}
    log_prop['X-request-Id'] = req_id
    log_prop['u_poi_id'] = upoiid

    log.warn(log_prop)