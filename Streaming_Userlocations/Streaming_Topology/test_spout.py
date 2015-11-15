__author__ = 'xebin'
# coding=utf-8
######优化：最小公共子集（uid,timestamp,_id,localtion）########
import logging
import random
import time
import arrow
import math
from utils import time_utils
from dao import mongo_dao
from bson import ObjectId

from pyleus.storm import Spout
log = logging.getLogger("stream_upoi_finding")

USER_LOCATIONS_TEST = (
    { "_id" : "561fbd979a444e080e8b096c", "processStatus" : "senzed", "user_id" : "55898213e4b0ef61557555a8", "poiProbLv2" : { "residence" : 0.9990945381823875, "traffic_place" : 0.000905461817614202 }, "objectId" : "55ce109960b24927fc49ded4", "timestamp" : "1438734449216", "pois" : { "objectId" : "55c184a900b0d1dbf4821128", "timestamp" : "1438734449216", "pois" : [ { "title" : "红旗干桥", "address" : "山东省东营市利津县", "location" : { "latitude" : 37.5131, "__type" : "GeoPoint", "longitude" : 118.228981 }, "_distance" : 1581, "type" : { "mapping_type" : "traffic_place", "objectId" : "55cdbb7000b09887f5774539", "source" : "tencent", "createdAt" : "2015-08-14T09:57:04.122Z", "updatedAt" : "2015-08-14T09:57:04.122Z", "origin_type" : "地名地址;交通地名" }, "id" : "11074266597019933882", "_dir_desc" : "西南" }, { "title" : "利津凤凰小区", "address" : "山东省东营市利津县利一路", "location" : { "latitude" : 37.48798, "__type" : "GeoPoint", "longitude" : 118.232079 }, "_distance" : 2475.7, "type" : { "mapping_type" : "residence", "objectId" : "55cdbb3400b0de09f865d243", "source" : "tencent", "createdAt" : "2015-08-14T09:56:04.240Z", "updatedAt" : "2015-08-14T09:56:04.240Z", "origin_type" : "住宅小区" }, "id" : "15980724641018660624", "_dir_desc" : "西北" }, { "title" : "利华益第二小区", "address" : "山东省东营市利津县利一路", "location" : { "latitude" : 37.487659, "__type" : "GeoPoint", "longitude" : 118.228729 }, "_distance" : 2327.9, "type" : { "mapping_type" : "residence", "objectId" : "55cdbb3400b0de09f865d243", "source" : "tencent", "createdAt" : "2015-08-14T09:56:04.240Z", "updatedAt" : "2015-08-14T09:56:04.240Z", "origin_type" : "住宅小区" }, "id" : "2714283884619119153", "_dir_desc" : "西北" } ], "radius" : 87.72820281982422, "user" : { "username" : "00000000-555a-4ce5-ffff-ffffbe20aeb8143507509138300anonymous", "mobilePhoneVerified" : 'false', "objectId" : "55898213e4b0ef61557555a8", "emailVerified" : 'false', "updatedAt" : "2015-06-23T15:58:11.399Z", "createdAt" : "2015-06-23T15:58:11.399Z" }, "user_place" : [ ], "location" : { "latitude" : 37.511332, "__type" : "GeoPoint", "longitude" : 118.220614 } }, "poiProbLv1" : { "traffic" : 0.000905461817614202, "estate" : 0.9990945381823875 }, "radius" : 87.72820281982422, "location" : { "lat" : 37.511332, "lng" : 118.220614 }, "updatedAt" : "2015-08-14T17:00:35.165Z", "senzedAt" : { "__type" : "Date", "iso" : "2015-08-14T17:00:35.130Z" }, "isTrainingSample" : 0, "createdAt" : "2015-08-14T16:00:25.300Z", "userRawdataId" : "55c184a900b0d1dbf4821128", "province" : "山东省", "city" : "东营市", "district" : "利津县", "street_number" : "", "nation" : "中国", "street" : "利七路" }
,   { "_id" : "", "processStatus" : "senzed", "user_id" : "559b8bd5e4b0d4d1b1d35e88", "poiProbLv2" : { "residence" : 0.9803140576788372, "traffic_place" : 0.019685942321162272 }, "objectId" : "55ce18d760b2b7509936fb64", "timestamp" : "1438828728410", "pois" : { "objectId" : "55c2cf4440ac7d0a94f772d4", "timestamp" : "1438828728410", "pois" : [ { "title" : "红旗干桥", "address" : "山东省东营市利津县", "location" : { "latitude" : 37.5131, "__type" : "GeoPoint", "longitude" : 118.228981 }, "_distance" : 1793.8, "type" : { "mapping_type" : "traffic_place", "objectId" : "55cdbb7000b09887f5774539", "source" : "tencent", "createdAt" : "2015-08-14T09:57:04.122Z", "updatedAt" : "2015-08-14T09:57:04.122Z", "origin_type" : "地名地址;交通地名" }, "id" : "11074266597019933882", "_dir_desc" : "西南" }, { "title" : "利津凤凰小区", "address" : "山东省东营市利津县利一路", "location" : { "latitude" : 37.48798, "__type" : "GeoPoint", "longitude" : 118.232079 }, "_distance" : 2450.4, "type" : { "mapping_type" : "residence", "objectId" : "55cdbb3400b0de09f865d243", "source" : "tencent", "createdAt" : "2015-08-14T09:56:04.240Z", "updatedAt" : "2015-08-14T09:56:04.240Z", "origin_type" : "住宅小区" }, "id" : "15980724641018660624", "_dir_desc" : "西北" }, { "title" : "利华益第二小区", "address" : "山东省东营市利津县利一路", "location" : { "latitude" : 37.487659, "__type" : "GeoPoint", "longitude" : 118.228729 }, "_distance" : 2279.8, "type" : { "mapping_type" : "residence", "objectId" : "55cdbb3400b0de09f865d243", "source" : "tencent", "createdAt" : "2015-08-14T09:56:04.240Z", "updatedAt" : "2015-08-14T09:56:04.240Z", "origin_type" : "住宅小区" }, "id" : "2714283884619119153", "_dir_desc" : "西北" } ], "radius" : 815, "user" : { "username" : "ffffffff-c7a8-b0d2-ffff-fffffc974f2e143625723746100anonymous", "mobilePhoneVerified" : 'false', "objectId" : "559b8bd5e4b0d4d1b1d35e88", "emailVerified" : 'false', "updatedAt" : "2015-07-07T08:20:37.542Z", "createdAt" : "2015-07-07T08:20:37.542Z" }, "user_place" : [ ], "location" : { "latitude" : 37.509881, "__type" : "GeoPoint", "longitude" : 118.218972 } }, "poiProbLv1" : { "traffic" : 0.019685942321162272, "estate" : 0.9803140576788372 }, "radius" : 815, "location" : { "lat" : 37.509881, "lng" : 118.218972 }, "updatedAt" : "2015-08-14T17:00:29.822Z", "senzedAt" : { "__type" : "Date", "iso" : "2015-08-14T17:00:29.773Z" }, "isTrainingSample" : 0, "createdAt" : "2015-08-14T16:35:35.146Z", "userRawdataId" : "55c2cf4440ac7d0a94f772d4", "province" : "山东省", "city" : "东营市", "district" : "利津县", "street_number" : "", "nation" : "中国", "street" : "316省道" }
)

ul_num=0
ts_start = time_utils.ts_days_before_begin(days=4, in_mil_sec=True)
ts_end = time_utils.ts_days_before_begin(days=0, in_mil_sec=True)
uid='560388c100b09b53b59504d2'
uls=mongo_dao.get_user_location_by_uid_time('test spout',uid,ts_start,ts_end)
uls_time=sorted(uls, key=lambda k: k.get('timestamp'))

uls_num=len(uls_time)
log.debug('get  uls---length:'+str(uls_num))



def test_get_ul_by_uid_time() :#uid1,ts_start1,ts_end1):

    global ul_num
    global uls_time

    if uls_num==0:
        log.debug('no  uls !!!')
        return None
    if ul_num<uls_num:
        ul_num=ul_num+1
        log.debug('get one ul num---- : '+str(ul_num-1))
        return uls_time[ul_num-1]
    else:
        ul_num=0
        return uls_time[ul_num]
        log.debug('new loop---length ')

def gps_generator():
    radius = 10000                         #Choose your own radius
    radiusInDegrees=radius/111300
    r = radiusInDegrees
    x0 = 39.0
    y0 = 116.0

    # for i in range(1,100):                 #Choose number of Lat Long to be generated
    u = float(random.uniform(0.0, 1.0))
    v = float(random.uniform(0.0, 1.0))

    w = r * math.sqrt(u)
    t = 2 * math.pi * v
    x = w * math.cos(t)
    y = w * math.sin(t)

    x_lat  = x + x0
    y_long = y + y0

    return x_lat, y_long


class UserLocationSpout(Spout):

    OUTPUT_FIELDS = ["userId", "userLocation"]
    time.sleep(1)

    def next_tuple(self):
        userlocation = test_get_ul_by_uid_time()
        userlocation['_id']= str(userlocation['_id'])

        global uls_num
        global ul_num
        log.debug(str(userlocation['_id'])+'--uls number:'+str(uls_num)+'-------ul num:'+str(ul_num)+'----st:'+str(userlocation['timestamp']))
        _user_id= userlocation["user_id"]

        # Emit the data to any bolts which has connected to it.
        self.emit((_user_id, userlocation))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/logs/uls_streaming/spout/user_locations_spout.log',
        format="%(message)s",
        filemode='a',
    )

    UserLocationSpout().run()