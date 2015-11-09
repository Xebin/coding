__author__ = 'xebin'

from leancloud import Object, Query, GeoPoint
from ..utils import av_utils

from requests.exceptions import ReadTimeout

from .. import parameters as param
from .. import config as conf
import filter

import requests
import uuid
import json
from .. import config

from firebase import firebase
import random
from ..utils import time_utils

firebase = firebase.FirebaseApplication(config.FIRE_BASE_URL,
                                        None)
from geopy.distance import vincenty

UPoiVisitLog = Object.extend('u_poi_visit_log')
UPoi = Object.extend('u_poi')
_User = Object.extend('_User')
UserTrace = Object.extend('user_trace')
UserLocation = Object.extend('UserLocation')
UserMotion = Object.extend('UserMotion')
MarkedUserLocation = Object.extend('marked_UserLocation')
UserProfile = Object.extend('user_profile_location_analysis')

class_map = {
    'u_poi_visit_log': UPoiVisitLog,
    'u_poi': UPoi,
    'user': _User,
    'user_trace': UserTrace,
    'UserLocation': UserLocation,
    'marked_UserLocation': MarkedUserLocation,
    'user_profile_location_analysis': UserProfile
}


def __get_u_poi_pointer(u_poi_id):
    u_poi = UPoi()
    u_poi.id = u_poi_id
    return u_poi_id


def get_pointer(class_name, objectId):
    obj = class_map[class_name]()
    obj.id = objectId
    return obj


def get_user_location(id):
    query = Query(UserLocation)
    return query.get(id)


def get_user_location_by_time(req_id, ts_start, ts_end):
    query = Query(UserLocation)

    query.greater_than_or_equal_to('timestamp', ts_start)
    query.less_than_or_equal_to('timestamp', ts_end)
    raw = av_utils.get_all(query, skip=0, result=[])

    # return filter.filter_UserLocation(req_id, raw)
    return filter.filter_UserLocation_mongo(req_id, raw)


def get_user_location_by_uid_time(req_id, user_id, ts_start, ts_end):
    query = Query(UserLocation)

    if user_id != None:
        # up = __get_user_pointer(user_id)
        up = get_pointer('user', user_id)
        query.equal_to('user', up)

    query.greater_than('timestamp', ts_start)
    query.less_than('timestamp', ts_end)
    query.include('user')

    raw = av_utils.get_all(query, skip=0, result=[])

    return filter.filter_UserLocation(req_id, raw)


def get_user_cities(req_id, user_id, ts_start, ts_end):
    query = Query(UserLocation)

    up = get_pointer('user', user_id)
    query.equal_to('user', up)

    query.greater_than('timestamp', ts_start)
    query.less_than('timestamp', ts_end)
    query.descending('timestamp')

    raw = av_utils.get_all(query, skip=0, result=[])

    uls = filter.filter_UserLocation(req_id, raw)

    bucket = time_utils.bucket_by_date(uls)

    cities = [{'city': l[0].get('city'), 'timestamp': l[0].get('timestamp')} for l in bucket]

    return cities


def get_user_city_stats(req_id, user_id, ts_start, ts_end):
    query = Query(UserLocation)
    city_set = av_utils.distinct(query, 'city', [])

    rt = {}
    for city in city_set:
        sql = 'select count(city) from UserLocation where TIMESTAMP > ? and TIMESTAMP  < ? and city = ?'
        city_num = Query.do_cloud_query(sql, ts_start, ts_end, city).count

        rt[city] = city_num

    return rt


def get_user_location_by_ids(req_id, user_location_ids):
    user_locations = []

    for user_location_id in user_location_ids:
        query = Query(UserLocation)
        user_locations.append(query.get(user_location_id))

    return user_locations


def get_user(user_id):
    query = Query(_User)
    return query.get(user_id)


def get_all_users():
    query = Query(_User)
    return av_utils.get_all(query, skip=0, result=[])


def get_user_u_pois(user_id, cluster_type):
    query = Query(UPoi)
    up = get_pointer('user', user_id)
    query.equal_to('user', up)

    query.equal_to('cluster_type', cluster_type)

    return query.find()


def get_u_poi(u_poi_id):
    query = Query(UPoi)
    return query.get(u_poi_id)


def get_u_poi_visit_log(user_id, ts_start=None, ts_end=None):
    query = Query(UPoiVisitLog)
    up = get_pointer('user', user_id)
    query.equal_to('user', up)

    if ts_start:
        query.greater_than('visit_time', ts_start)
    if ts_end:
        query.less_than('visit_time', ts_end)

    if ts_start or ts_end:
        query.ascending('visit_time')

    return query.find()


def delete_u_poi_visit_log(user_id, ts_start=None, ts_end=None):
    if ts_start == None or ts_end == None:
        raise Exception('delete_u_poi_visit_log needs a time range', ts_start, ts_end)

    query = Query(UPoiVisitLog)
    up = get_pointer('user', user_id)
    query.equal_to('user', up)
    query.greater_than('visit_time', ts_start)
    query.less_than('visit_time', ts_end)

    # if len(query.find()) > 0:
    #     query.destroy_all()

    for ele in query.find():
        print ele
        ele.destroy()


def get_latest_visit_log(user_id, ts_start, ts_end):
    query = Query(UPoiVisitLog)
    query.greater_than('visit_time', ts_start)
    query.less_than('visit_time', ts_end)

    up = get_pointer('user', user_id)
    query.equal_to('user', up)

    query.descending('visit_time')
    query.limit(1)

    result = query.find()

    if result != None and len(result) > 0:
        return result[0]
    else:
        return None


def get_last_visit_log(u_poi_id):
    query = Query(UPoiVisitLog)

    upoip = get_pointer('u_poi', u_poi_id)
    query.equal_to('u_poi', upoip)

    query.descending('visit_time')
    query.limit(1)

    result = query.find()

    if result != None and len(result) > 0:
        return result[0]
    else:
        return None


def save_u_poi(coordinate, user_id, poi_label, poi_type, poi_title, poi_address, poi_coordinate, near_pois,
               cluster_type):
    u_poi = UPoi()
    # up = __get_user_pointer(user_id)
    up = get_pointer('user', user_id)
    u_poi.set('user', up)

    point = GeoPoint(latitude=coordinate[0], longitude=coordinate[1])
    u_poi.set('location', point)

    u_poi.set('poi_label', poi_label)
    u_poi.set('poi_type', poi_type)
    u_poi.set('poi_title', poi_title)
    u_poi.set('poi_address', poi_address)

    # Unfortunately, AV only allow one geopoint for one object
    if poi_coordinate != None:
        poi_point = {"latitude": poi_coordinate[0], "longitude": poi_coordinate[1]}
        u_poi.set('poi_location', poi_point)
    else:
        u_poi.set('poi_location', None)

    u_poi.set('near_pois', near_pois)

    u_poi.set('cluster_type', cluster_type)

    # u_poi.save()
    av_utils.safe_save(u_poi)
    return u_poi


def save_u_poi_visit_log(visit_time, user_id, u_poi_id, avg_start, avg_end, avg_duration,
                         this_start, this_end, this_duration, home_office_label):
    up = get_pointer('user', user_id)

    upoip = get_pointer('u_poi', u_poi_id)

    upoilog = UPoiVisitLog()
    upoilog.set('user', up)
    upoilog.set('u_poi', upoip)
    upoilog.set('visit_time', visit_time)
    upoilog.set('avg_start', avg_start)
    upoilog.set('avg_end', avg_end)
    upoilog.set('avg_duration', avg_duration)
    upoilog.set('this_start', this_start)
    upoilog.set('this_end', this_end)
    upoilog.set('this_duration', this_duration)
    upoilog.set('home_office_label', home_office_label)

    av_utils.safe_save(upoilog)
    return upoilog


def save_user_profile(uid, profile):
    up = get_pointer('user', uid)
    user_profile = UserProfile()
    user_profile.set('user', up)
    user_profile.set('user_profile', profile)

    av_utils.safe_save(user_profile)
    return user_profile


def save_marked_UserLocation(user_location_id, timestamp, geo_point, u_poi_id, u_poi_visit_log_id=None):
    # upoi_pointer = __get_u_poi_pointer(u_poi_ide)
    # visitlog_pointer = __get_u_poi_pointer(u_poi_id)
    upoi_p = get_pointer('u_poi', u_poi_id)

    marked_user_location = class_map['marked_UserLocation']()

    if u_poi_visit_log_id:
        visitlog_p = get_pointer('u_poi_visit_log', u_poi_visit_log_id)
        marked_user_location.set('u_poi_visit_log', visitlog_p)

    marked_user_location.set('u_poi', upoi_p)
    marked_user_location.set('timestamp', timestamp)

    marked_user_location.set('location', geo_point)

    user_location_p = get_pointer('UserLocation', user_location_id)
    marked_user_location.set('user_location', user_location_p)

    av_utils.safe_save(marked_user_location)
    return marked_user_location


def get_near_poi(user_id, timestamp, coordinate):
    data = {
        "locations": [
            {
                "timestamp": timestamp,
                "location": {
                    "latitude": coordinate[0],
                    "longitude": coordinate[1],
                    "__type": "GeoPoint"
                }
            }],
        "userId": user_id
    }

    request_id = str(uuid.uuid4())
    headers = {'content-type': 'application/json',
               'X-request-Id': request_id}

    r = requests.post(conf.POI_URL, data=json.dumps(data), headers=headers)

    content_dict = json.loads(r.content)

    if 'pois' not in content_dict['results']['parse_poi'][0]:
        print 'pois not in content_dict[results][parse_poi][0]'
        return [], request_id

    return content_dict['results']['parse_poi'][0]['pois'], request_id


def get_marked_UserLocation(u_poi_id, limit=100):
    upoi_p = get_pointer('u_poi', u_poi_id)

    query = Query(MarkedUserLocation)
    query.equal_to('u_poi', upoi_p)

    return query.find()


def get_user_home_office(uid):
    # find recent home / office visits
    query = Query(UPoiVisitLog)
    up = get_pointer('user', uid)
    query.equal_to('user', up)
    query.equal_to('home_office_label', 'home')
    query.descending('visit_time')
    query.include('u_poi')
    query.limit(1)

    result = query.find()
    if len(result) != 0:
        home = result[0]
    else:
        home = None

    query = Query(UPoiVisitLog)
    up = get_pointer('user', uid)
    query.equal_to('user', up)
    query.equal_to('home_office_label', 'office')
    query.descending('visit_time')
    query.include('u_poi')
    query.limit(1)

    result = query.find()
    if len(result) != 0:
        office = result[0]
    else:
        office = None

    return home, office


def get_motion(uid, stop):
    query = Query(UserMotion)
    up = get_pointer('user', uid)
    query.equal_to('user', up)

    query.greater_than('timestamp', stop)

    return query.find()


def get_motion_prediction(rawData):
    request_id = str(uuid.uuid4())
    headers = {'content-type': 'application/json',
               'X-request-Id': request_id}

    r = requests.post(conf.MOTION_PREDICTION, data=json.dumps(rawData), headers=headers)

    content_dict = json.loads(r.content)

    return content_dict, request_id


def update_fb_user_home_office_status(uid, user_status, timestamp):
    result = get_fb_user_home_office_status(uid)
    try:
        pre_event = result['content']['home_office_status']
    except KeyError:
        pre_event = None

    should_update = False
    if pre_event == None or abs(pre_event['expireTime'] - timestamp) > param.HOME_OFFICE_EVENT_GAP:
        should_update = True

    if should_update:
        firebase.patch('/notification/' + uid + '/content/home_office_status',
                       {
                           "status": user_status,
                           "timestamp": timestamp,
                           "expireTime": timestamp + param.HOME_OFFICE_STATUS_EXP
                       })

    return should_update


def get_fb_user_home_office_status(uid):
    return firebase.get('/notification/', uid)


if __name__ == '__main__':
    print 'dao'
    # set_event(1, '555e92e6e4b06e8bb85473ce', 1)
    # uid = '555e92e6e4b06e8bb85473ce'
    # print get_fb_user_home_office_status(uid)
    # update_fb_user_home_office_status(uid, 'arriving_office', 1441545781000)
