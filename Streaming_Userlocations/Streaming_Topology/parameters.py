# coding=utf-8
# -*- coding: utf-8 -*-
from __future__ import division

#for storm upois
CLUSTER_TYPE_STORM_POI_BASED = 'storm_poi_based'
STORM_POI_SAMPLES_BUCKET_NUMBER= 10
STORM_POI_DURATION_LIMIT=2*60*60*1000 #ms
STORM_POI_DURATION_LIMIT_MIN=1*60*60*1000 #ms

STORM_POI_DIS=0.1 # km
STORM_UL_DIS_LIMIT=1

STORM_POI_USERS=['559b8bd5e4b0d4d1b1d35e88','55898213e4b0ef61557555a8','55bda7b900b0fac2af6a33de','5624da0960b27457e89bff13']




# FOR Cluster Type
CLUSTER_TYPE_POI_BASED = 'poi_based'
CLUSTER_TYPE_DENSITY_BASED = 'density_based'
CLUSTER_TYPE_STORM_POI_BASED = 'storm_poi_based'



# FOR Cluster Algorithm
U_POI_EPS = 0.001
U_POI_MIN_SAMPLES = 10
CLUSTER_MAX_SAMPLE_RATE = 6  # per hour
HOME_DURATION_THRES = 5 * 60 * 60 * 1000
OFFICE_DURATION_THRES = 5 * 60 * 60 * 1000

# FOR POI Based Cluster Algorithm
COOR_NUMBER_THRES = 10
BUCKET_DENSITY_THRES = 3
POI_BASED_DIST_THRES = 0.2  # km


# FOR AV Utility
AV_GET_ALL_EACH_STEP_LIMIT = 500
AV_SLEEP_TIME_SAFE_SAVE = 2  # sec

# FOR Cluster Manager
CLUSTER_USER_DATA_THRES = 200
CLUSTER_NEAR_POI_NUMBER = 3
CLUSTER_DATE_FORMAT = '%Y-%m-%d'
CLUSTER_DATA_TIME_SPAN = 5  # days

# FOR u_poi Manager
U_POI_DIST_THRES = 0.1  # km
POI_DIST_THRES = 0.1  # km
TIME_CLOSE_THRES = 10 * 60 * 1000  # mil sec

# FOR u_poi Algorithm
U_POI_CROSS_MIDNIGHT_RATE_THRES = 0.8
TS_DIFF_VISIT_WITHIN_3DAYS = 3 * 24 * 60 * 60 * 1000

# FOR u_poi_status Algorithm
NEAR_HOME_OFFICE_THRES = 0.8  # km
AT_HOME_OFFICE_THRES = 0.1 # km
NEAR_START_END_THRES = 0.5 * 60 * 60 # .5 hour in sec
STILL_RATE_THRES = 0.7
AT_PLACE_THRES = 0.8
HOME_OFFICE_EVENT_GAP = 0.5 * 60 * 60   # .5 hour in sec
HOME_OFFICE_STATUS_EXP = 0.5 * 60 * 60 # .5 hour in sec
RECENT_MOTION_THRES = 10 * 60 * 1000  # 10 min in million sec
RECENT_LOCATION_GAP = 10 * 60 * 1000
STATUS_CODE = ["arriving_home",
               "leaving_home",
               "arriving_office",
               "leaving_office",
               "going_home",
               "going_office",
               "user_home_office_not_yet_defined",
               "at_home",
               "at_office"
               ]

# FOR u_city
CITY_TIME_RANGE = 7 # days
UCITY_TIME_RANGE = 100 # days
UCITY_THRES = 0.6
CITY_RESAMPLE_SIZE = 10 # samples
CITY_RESAMPLE_STEP = 4 # hours
RETURN_FROM_THRES = 2 * 24 * 60 * 60 * 1000 # days in million sec

# FOR u_poi time range
TIME_CUTOFF_THRES = 2 * 60 * 60 * 1000  # no data in 2 hours will be considered as data absence
TIME_SPAN_AVG_START_END = 15  # days
TIME_CLUSTER_MAX_GAP = 2 * 60 * 60 * 1000  # 2 hours in million sec
TIME_SPAN_MIN_CLUSTER = 2  # this is particularly designed for Otaku


# FOR Crontab Requests
FAKE_TS_FOR_API_POIS = 612905400000  # in mil sec
CRONTAB_REQUEST_ID = 'cron_request_id'


# FOR Profiler
PROF_RECENT_DAY = 14  # days
PROF_RECENT_MIL_SEC = PROF_RECENT_DAY * 24 * 60 * 60 * 1000  # 14 days in million second
PROF_VISIT_FREQ_THRES = 2 / PROF_RECENT_DAY
# note this number is unique u poi visit in PROF_RECENT_DAY
PROF_WORKING_CLASS_U_POI_THRES = 5
PROF_BUSINESS_CLASS_U_POI_THRES = 7

LOCATION_STR_MAP = {
    'school': {
        'mapping_type': [
            'primary_school',
            'technical_school',
            'university',
            'kinder_garten',
            'training_institutions',
            'high_school'
        ]
    },
    'military': {
        'home_made': [
            '军区'
        ]
    },
    'business': {
        'mapping_type': [
            'business_building'
        ]
    },
    'gov': {
        'home_made': [
            '政府'
        ]
    },
    'hotel': {
        'mapping_type': [
            'hostel',
            'hotel',
            'motel',
            'economy_hotel',
            'guest_house'
        ]
    }
}

LOCATION_USER_PROFILE_MAP = {
    'school': ['student', 'teacher'],
    'military': ['military'],
    'business': ['businessman'],
    'gov': ['civil_servant'],
    'working_class': ['working_class'],
    'inactive': ['inactive_user']
}


# FOR API Response
POI = {
    'title': 'string',
    'address': 'string',
    'location': 'geo_point',
    '_distance': 'int',
    'type': 'object',
    'id': 'string',
    '_dir_desc': 'string'
}

U_POI_FIELDS = {
    'poi_title': 'string',
    'poi_address': 'string',
    'near_pois': {'array': POI},
    'poi_label': 'string',
    'poi_location': 'object',
    'poi_type': 'object',
    'location': 'geo_point'
}

BED_TIME = [23, 24, 0, 1, 2, 3, 4, 5, 6, 7]
WORK_TIME = [11, 12, 3, 4, 5, 6]
