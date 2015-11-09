__author__ = 'xebin'

from .. import parameters as param
from requests.exceptions import ReadTimeout
from time import sleep
from leancloud import LeanCloudError

def get_all(query, skip, result):
    limit = param.AV_GET_ALL_EACH_STEP_LIMIT

    query.limit(limit)
    query.skip(skip)

    try:
        found = query.find()
    except Exception:
        print 'get all fucked, sleep for 2 sec'
        sleep(2)
        found = query.find()

    if found and len(found) > 0:
        result.extend(found)
        print 'av_utils get_all _class_name:', query._query_class._class_name, ' now result length:', len(
            result), ' skipped:', skip
        return get_all(query, skip + limit, result)
    else:
        return result


def safe_save(obj):
    try:
        obj.save()
    except ReadTimeout:
        sleep(param.AV_SLEEP_TIME_SAFE_SAVE)
        obj.save()


def av_object_json(av_obj, av_obj_fields):
    j = {}
    for field_name in av_obj_fields.keys():
        field_type = av_obj_fields[field_name]

        if field_type == 'geo_point':
            geo_point = av_obj.get(field_name)
            geo_json = {'latitude': geo_point.latitude, 'longitude': geo_point.longitude}
            j[field_name] = geo_json
        #
        elif type(field_type) == dict and field_type.keys()[0] == 'array':

            array_type = field_type[field_type.keys()[0]]
            array = av_obj.get(field_name)

            array_j = [av_object_json(ele, array_type) for ele in array]

            if len(array_j) > 0:
                j[field_name] = array_j
            else:
                j[field_name] = array
        else:
            j[field_name] = av_obj.get(field_name)

    return j


# NOTE, existing elements can not exceed 128 otherwise this will crash
# POINTER as existing element is ok
def distinct(query, distinct_field, existing_elements):
    query.not_contained_in(distinct_field, existing_elements)

    query.limit(1)
    try:
        result = query.find()
    except KeyError, e:
        if len(existing_elements) >= 128:
            raise Exception('AVOS bug, existing_elements can not exceed 128')
        else:
            raise e

    if result == None or len(result) == 0:
        return existing_elements

    for ele in result:
        existing_elements.append(ele.get(distinct_field))

    distinct(query, distinct_field, existing_elements)


if __name__ == '__main__':
    import leancloud
    import config as conf

    leancloud.init(conf.AV_ID, conf.AV_KEY)

    # get distinct user ids from AV
    from leancloud import Query, Object

    # up = Object.extend('_User')

    query = Query(Object.extend('UserLocation'))
    res = distinct(query, 'user', [], )

    print res
