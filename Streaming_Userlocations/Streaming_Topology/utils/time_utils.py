# -*- coding: utf-8 -*-

__author__ = 'wuzhifan'

import time, datetime
from .. import parameters as param
import copy
from pytz import timezone

import os
os.environ['TZ'] = 'Asia/Hong_Kong'
time.tzset()


ISO_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_FORMAT = '%Y-%m-%d'

def st_now():
    return datetime.datetime.now()

def ts_now():
    return time.mktime(st_now().timetuple())

def locol_utc_offset():
    now_stamp = time.time()
    local_time = datetime.datetime.fromtimestamp(now_stamp)
    utc_time = datetime.datetime.utcfromtimestamp(now_stamp)
    return local_time - utc_time


LOCAL_UTC_OFFSET = locol_utc_offset()


def utc2local(utc_st):
    '''convert utc datetime to local datetime

    :param utc_st: datetime.datetime type
    :return:
    '''
    local_st = utc_st + LOCAL_UTC_OFFSET
    return local_st


def local2utc(local_st):
    '''convert local datetime to utc datetime

    :param local_st: datetime.datetime type
    :return:
    '''
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st


def secFromBeginningOfDay(timestamp):
    # NOTE timestamp is not local time
    # the Beginning of your day is local day

    local_st = timestamp2local(timestamp)

    hour = local_st.hour
    minute = local_st.minute
    return hour * 60 * 60 + minute * 60





def timestamp2local(timestamp):
    timestamp = int(timestamp)

    str_ts = str(timestamp)

    if len(str_ts) == 13:
        timestamp /= 1000

    utc_st = datetime.datetime.utcfromtimestamp(timestamp)

    return utc2local(utc_st)


def is_weekday(timestamp):
    # 0 monday, ..., 5 saturday 6 sunday
    dt = timestamp2local(timestamp)
    if dt.weekday() in range(0, 5):
        return True
    else:
        return False

def ts_days_before_begin(days, in_mil_sec=False):
    days_before = datetime.datetime.now() - datetime.timedelta(days=days)

    days_before = days_before.replace(hour=0)
    days_before = days_before.replace(minute=0)
    days_before = days_before.replace(second=0)

    days_before_ts = time.mktime(days_before.timetuple())

    if not in_mil_sec:
        return int(days_before_ts)
    else:
        return int(days_before_ts * 1000)

def ts_days_before_end(days, in_mil_sec=False):
    days_before = datetime.datetime.now() - datetime.timedelta(days=days)

    days_before = days_before.replace(hour=23)
    days_before = days_before.replace(minute=59)
    days_before = days_before.replace(second=59)

    days_before_ts = time.mktime(days_before.timetuple())

    if not in_mil_sec:
        return int(days_before_ts)
    else:
        return int(days_before_ts * 1000)


def ts_yesterday_begin(in_mil_sec=False):
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(hour = 0)
    yesterday = yesterday.replace(minute = 0)
    yesterday = yesterday.replace(second = 0)

    print 'tuple:', yesterday.timetuple()
    yesterday_ts = time.mktime(yesterday.timetuple())
    if not in_mil_sec:
        return int(yesterday_ts)
    else:
        return int(yesterday_ts * 1000)



def ts_yesterday_end(in_mil_sec):

    today = datetime.datetime.today()
    ts_today = time.mktime(today.timetuple())

    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    ts_yesterday = time.mktime(yesterday.timetuple())

    yesterday = yesterday.replace(hour = 23)
    yesterday = yesterday.replace(minute = 59)
    yesterday = yesterday.replace(second = 59)

    yesterday_ts = time.mktime(yesterday.timetuple())

    if not in_mil_sec:
        return int(yesterday_ts)
    else:
        return int(yesterday_ts * 1000)

def ts_date_end(ts):
    local_st = timestamp2local(ts)
    local_end = copy.copy(local_st)

    local_end = local_end.replace(hour = 23)
    local_end = local_end.replace(minute = 59)
    local_end = local_end.replace(second = 59)

    local_end_ts = time.mktime(local_end.timetuple())

    return local_end_ts

def ts2date_str(ts):
    local_st = timestamp2local(ts)
    return local_st.strftime(param.CLUSTER_DATE_FORMAT)


def bucket_by_date(avo):

    bucket = {}

    for ele in avo:
        ts = ele.get('timestamp')
        date_str = ts2date_str(ts)

        if date_str not in bucket:
            bucket[date_str] = []

        bucket[date_str].append(ele)

    return bucket

if __name__ == '__main__':
    # print ts_yesterday_begin(True)
    # print ts_yesterday_end(True)
    # print is_weekday(1441332578000)
    print ts_now()