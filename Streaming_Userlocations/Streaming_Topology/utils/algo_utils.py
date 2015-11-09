import sys
sys.path.append('/data/pycharms/test/test.storm.ueserlocation/Streaming_Userlocations/Streaming_Topology/config')
sys.path.append('/data/pycharms/test/test.storm.ueserlocation/Streaming_Userlocations/Streaming_Topology/config/parameters.py')
import random
import numpy as np
from .. import parameters as param
from geopy import distance
from ..dao import av_dao
import logger


def geo_distance_km(coor1, coor2):
    return distance.vincenty(coor1, coor2).kilometers


def near_u_poi(p1, p2, thres=param.U_POI_DIST_THRES):
    # print 'geo_distance_km:',geo_distance_km(p1, p2)
    if geo_distance_km(p1, p2) < thres:
        return True
    else:
        return False


def at_point(p1, p2, at_thres=0.1):
    if geo_distance_km(p1, p2) < at_thres:
        return True
    else:
        return False


def time_close(ts1, ts2):
    ts1 = int(ts1)
    ts2 = int(ts2)

    if str(ts1) != str(ts2) or str(ts1) != 13:
        raise ValueError('timestamp error, should be equal length and 13 digits', ts1, ts2)

    if abs(ts1 - ts2) < param.TIME_CLOSE_THRES:
        return True
    else:
        return False


def check_new_u_poi(new_list, old_list):
    result = []
    for ncoor in new_list:
        is_new = True
        for ocoor in old_list:
            if near_u_poi(ncoor, ocoor):
                is_new = False
        if is_new:
            result.append(True)
        else:
            result.append(False)
    return result


# NOTE this is a wrong way to average a coordinate cluster
# def get_cluster_centers(data, labels):
#     label_num = len(np.unique(labels))
#     centers = np.zeros((label_num, 2))
#     count = np.zeros(label_num)
#
#     result = {}
#
#     for coor, label in zip(data, labels):
#         label = str(label)
#
#         if label not in result:
#             result[label] = [0, 0]
#         centers[label] += coor
#         count[label] += 1
#
#     result = {}
#     for i in range(0, label_num):
#         result[str(i)] = centers[i] / count[i]
#
#     return result


def sample_by_timestamp(av_objects, ts_key, sample_number, sort=True):
    if sample_number >= len(av_objects):
        return av_objects
    sample = random.sample(av_objects, sample_number)
    if sort:
        sample = sorted(sample, key=lambda k: k.get(ts_key))
    return sample


def get_near_pois(req_id, uid, coordinate, near_poi_num=param.CLUSTER_NEAR_POI_NUMBER):
    near_pois, poi_req_id = av_dao.get_near_poi(user_id=uid,
                                             timestamp=param.FAKE_TS_FOR_API_POIS,
                                             coordinate=coordinate)

    # NOTE can not trust _distance, need to recalculate distance
    # sorted_by_dist = __sort_by_distance(near_pois, coordinate)
    # FUCK poi location is wrong, only thing can be trusted is _distance
    if near_pois == None or len(near_pois) == 0:
        return []

    sorted_by_dist = sorted(near_pois, key=lambda k: k['_distance'])

    logger.log_daily_cluster_poi_request(req_id, poi_req_id)

    re = sorted_by_dist[0: near_poi_num]
    if re == None or len(re) == 0:
        print 'fuck'

    return re


def __sort_by_distance(near_pois, coordinate):
    return sorted(near_pois,
                  key=lambda k:
                  geo_distance_km([k['location']['latitude'], k['location']['longitude']],
                                  coordinate)
                  )


if __name__ == '__main__':
    # x = [[1,10],[2,20],[1, 11], [3, 23]]
    # y = [1, 0, 1, 0]
    #
    # get_near_pois(req_id, uid, coordinate, near_poi_num=param.CLUSTER_NEAR_POI_NUMBER):
    coor = [39.973476, 116.302475]
    print get_near_pois('f', 'ff', coor)

    # time_close(11, 22)
