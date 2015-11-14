__author__ = 'xebin'
from pymongo import MongoClient
from ..utils import time_utils
import filter

from bson.objectid import ObjectId
from bson.dbref import DBRef
from pymongo.son_manipulator import AutoReference, NamespaceInjector

# client = MongoClient('119.254.111.40', 27017)
client = MongoClient('mongodb://root:Senz2everyone@119.254.111.40')
db = client.RefinedLog


def insert_UserLocation(data):
    result = db.UserLocation.insert_one(data)
    return result


def if_exist(class_name, objectId):
    result = db[class_name].find_one({'objectId': objectId})

    if result != None and '_id' in result.keys():
        return True
    else:
        return False


# TODO how to search by sub structure ID
def get_pointer(class_name, objectId):
    return {'objectId': objectId}


def get_user_location(id):
    return db.UserLocation.find({'objectId': id})


def get_user_location_by_time(req_id, ts_start, ts_end):
    raw = db.UserLocation.find({'timestamp': {'$gte': ts_start, '$lte': ts_end}})

    # return filter.filter_UserLocation(req_id, raw)
    return filter.filter_UserLocation_mongo(req_id, raw)


def get_user_location_by_uid_time(req_id, user_id, ts_start, ts_end):
    if user_id != None:
        # up = __get_user_pointer(user_id)
        up = get_pointer('user', user_id)
    else:
        raise Exception('user id can not be None')

    raw = db.UserLocation.find({'timestamp': {'$gt': ts_start, '$lt': ts_end},
                                'user_id': user_id})
    # print 'raw filter'
    # print str(raw.count())
    return filter.filter_UserLocation_mongo(req_id, raw)


def get_user_cities(req_id, user_id, ts_start, ts_end):
    up = get_pointer('user', user_id)

    raw = db.UserLocation.find({'timestamp': {'$gt': ts_start, '$lt': ts_end},
                                'user': up}).sort({'timestamp': -1})

    uls = filter.filter_UserLocation(req_id, raw)

    bucket = time_utils.bucket_by_date(uls)

    cities = [{'city': l[0].get('city'), 'timestamp': l[0].get('timestamp')} for l in bucket]

    return cities


def get_user_city_stats(req_id, user_id, ts_start, ts_end):
    city_set = db.UserLocation.distinct('citys')

    rt = {}
    for city in city_set:
        city_num = db.UserLocation.find({'timestamp': {'$gt': ts_start, '$lt': ts_end},
                                         'city': city}).count()
        rt[city] = city_num
    return rt


def get_user_location_by_ids(req_id, user_location_ids):
    user_locations = []

    for user_location_id in user_location_ids:
        result = db.UserLocation.find_one({'objectId': user_location_id})
        user_locations.append(result)

    return user_locations


def get_user(user_id):
    return db.User.find_one({'objectId': user_id})


def get_all_users():
    return db.User.find()


def get_user_u_pois(user_id, cluster_type):
    up = get_pointer('user', user_id)
    return db.UPoi.find({'user': up, 'cluster_type': cluster_type})


def get_u_poi(u_poi_id):
    return db.UPoi.find_one({'objectId': u_poi_id})


def get_u_poi_visit_log(user_id, ts_start=None, ts_end=None):
    up = get_pointer('user', user_id)
    conditions = [{'user', up}]

    if ts_start:
        conditions.append({'visit_time': {'$gt': ts_start}})
    if ts_end:
        conditions.append({'visit_time': {'$lt': ts_end}})
    if ts_start or ts_end:
        return db.UPoiVisitLog.find({"$and": conditions}).sort('visit_time')
    else:
        return db.UPoiVisitLog.find({"$and": conditions})


def delete_u_poi_visit_log(user_id, ts_start=None, ts_end=None):
    if ts_start == None or ts_end == None:
        raise Exception('delete_u_poi_visit_log needs a time range', ts_start, ts_end)

    up = get_pointer('user', user_id)
    db.UPoiVisitLog.remove({'timestamp': {'$gt': ts_start, '$lt': ts_end}, 'user': up})


def get_latest_visit_log(user_id, ts_start, ts_end):
    up = get_pointer('user', user_id)

    result = db.UPoiVisitLog.find({'user': up,
                                   'timestamp': {'$gt': ts_start, '$lt': ts_end}}).sort({'visit_time': -1}).limit(1)

    if result != None and len(result) > 0:
        return result[0]
    else:
        return None

def saveMarkedUserLocation(request_id,
                           user_location_id,
                           timestamp,
                           geo_point,
                           u_poi_id,
                           u_poi_visit_log_id=None):
    # upoi_pointer = __get_u_poi_pointer(u_poi_ide)
    # visitlog_pointer = __get_u_poi_pointer(u_poi_id)

    # mark user location with u poi id AVID, u poi visit id AVID, user location id MID
    # field name with id is AVID, without id is a mongo pointer
    # print user_location_id, timestamp, geo_point, u_poi_id, u_poi_visit_log_id

    data = {
        'u_poi_id': u_poi_id,
        'u_poi_visit_id': u_poi_visit_log_id,
        'user_location':DBRef('UserLocation',ObjectId(user_location_id)),
        'timestamp': timestamp,
        # TODO save location data
        # 2d sphere
        'location': geo_point
    }

    # TODO save via strongloop REST
    # host='http://119.254.111.40:3000/api/MarkedUserLocations'
    # try:
    #     save_result = requests.post(host, data=json.dumps(data))
    # except Exception, e:
    #     print 'saveMarkedUserLocation erro!'
    #     return None
    # data=json.dumps(data)
    save_result = db.MarkedUserLocation.insert_one(data)
    # print 'save maked!'
    return save_result

def deleteMarkedUserLocation(id):
    save_result = db.MarkedUserLocation.find_one_and_delete({"_id":ObjectId(id)})
    return save_result
def get_marked_user_location(id):
    db.add_son_manipulator(NamespaceInjector())
    db.add_son_manipulator(AutoReference(db))
    return db.MarkedUserLocation.find_one({"_id":ObjectId(id)})

def get_marked_UserLocation(u_poi_id, limit=100):

    return db.MarkedUserLocation.find({'u_poi_id': u_poi_id})


def get_motion(uid, stop):
    return db.UserMotion.find({'timestamp': {'$gt': stop}, 'user_id': uid})


#
# if __name__ == '__main__':
#     print 'dao'
    # set_event(1, '555e92e6e4b06e8bb85473ce', 1)
    # uid = '555e92e6e4b06e8bb85473ce'
    # print get_fb_user_home_office_status(uid)
    # update_fb_user_home_office_status(uid, 'arriving_office', 1441545781000)
