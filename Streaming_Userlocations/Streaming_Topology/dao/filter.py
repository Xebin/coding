__author__ = 'xebin'


from ..utils import logger
# input data list
# output validated data list, some data are converted

def filter_u_poi_visit_log(req_id, u_poi_visit_log):
    validated = []
    for visit_log in u_poi_visit_log:
        try:
            ts = __validate_convert_av_timestamp(visit_log.get('visit_time'))
            visit_log.set('visit_time', ts)

            avg_start = __validate_convert_avg_start_end(visit_log.get('avg_start'))
            avg_end = __validate_convert_avg_start_end(visit_log.get('avg_end'))
            visit_log.set('avg_start', avg_start)
            visit_log.set('avg_end', avg_end)

            validated.append(visit_log)
        except ValueError, e:
            logger.warn_wrong_visit_log(req_id, visit_log.id, e.message)

    return validated


def filter_UserLocation(req_id, user_locations):
    validated = []
    for user_location in user_locations:
        try:
            ts = __validate_convert_av_timestamp(user_location.get('timestamp'))
            user_location.set('timestamp', ts)

            validated.append(user_location)
        except ValueError, e:
            logger.warn_wrong_user_location(req_id, user_location.id, e.message)

    return validated

def filter_UserLocation_mongo(req_id, user_locations):
    validated = []
    i=0
    for user_location in user_locations:
        try:
            # ts = __validate_convert_av_timestamp(user_location.get('timestamp'))
            # print user_location['timestamp']
            ts = __validate_convert_av_timestamp(user_location['timestamp'])
            # user_location.set('timestamp', ts)
            # print 'ts:'+str(ts)
            user_location['timestamp'] = ts
            # print str(user_location)
            validated.append(user_location)
            i=i+1
        except ValueError, e:
            logger.warn_wrong_user_location(req_id, user_location['_id'], e.message)
    # print 'valid:'+str(i)
    return validated


# def data_cutoff_detection(user_location):
#     print 'data cut off detection'




def __validate_convert_av_timestamp(ts):
    ts = int (ts)
    if len(str(ts)) == 13:
        return ts
    else:
        raise ValueError('timestamp:', ts,
                         'format is not correct, '
                         'ts from AV should be in million second')


def __validate_convert_avg_start_end(ts):

    if ts == None:
        return ts

    ts = int(ts)
    if 0 < ts < 24 * 60 * 60:
        return ts
    else:
        raise ValueError('avg_start_end:', ts,
                         'format is not correct, '
                         'start end should be with in 0~86400')