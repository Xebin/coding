__author__ = 'xebin'
import logging
import json
from utils import time_utils
from pyleus.storm import SimpleBolt

from parameters import STORM_POI_DURATION_LIMIT,STORM_UL_DIS_LIMIT,STORM_POI_SAMPLES_BUCKET_NUMBER
from utils import algo_utils

log = logging.getLogger("ulsCollectorFilterBolt")

class ulsCollectorFilterBolt(SimpleBolt):
    # global  bucket
    # global ul_distance_limit
    bucket={}
    ul_distance_limit=0
    OUTPUT_FIELDS = ["userId", "uls"]

    def process_tuple(self, tup):
        userId,ul = tup.values
        ul_dict=ul#json.loads(ul)
        # log.debug('ul--to filter---: '+str(userId))
        if self.bucket.get(userId)!=None and len(self.bucket[userId])!=0:
            bucket_uid_time = sorted(self.bucket[userId], key=lambda k: k.get('timestamp'))
            ts_start=long(bucket_uid_time[0]['timestamp'])
            samples_number=len(self.bucket[userId])
            loc=dict(self.bucket[userId][0])['location']
            loc_coor=[loc['lat'],loc['lng']]
        else:
            ts_start=long(ul_dict['timestamp'])
            samples_number=0
            loc=ul_dict['location']
            loc_coor=[loc['lat'],loc['lng']]

        duration=long(ul_dict['timestamp'])-ts_start
        log.debug(' --duration-: '+str(duration)+'---samples num:--'+str(samples_number))

        #emit

        if  duration>STORM_POI_DURATION_LIMIT:
            if samples_number>STORM_POI_SAMPLES_BUCKET_NUMBER :
                userlocations=self.bucket[userId]
                self.emit((userId, userlocations))
                self.bucket[userId]=[]
                ul_distance_limit=0
                log.debug('uls-collec-filter-bolt  emit-----: '+str(userId)+'emit bucket length:'+str(len(userlocations)))
            else:
                self.bucket[userId]=[]
                log.debug('--filter --samples number-: '+str(samples_number)+'---uid--'+str(userId))
                ul_distance_limit=0

        #time limit
        if duration<STORM_POI_DURATION_LIMIT or duration==STORM_POI_DURATION_LIMIT :
            # distance limit
            new_loc_coor=[ul_dict['location']['lat'],ul_dict['location']['lng']]
            if algo_utils.near_u_poi(loc_coor,new_loc_coor) :
                if self.bucket.get(userId)==None:
                    self.bucket[userId]=[ul_dict]
                else:
                    self.bucket[userId].append(ul_dict)
                    log.debug(str(userId)+'--adding - -bucket num: '+str(len(self.bucket[userId]))+'--time--:'+str(time_utils.timestamp2local(ul['timestamp']))+'--new loc:--'+str(new_loc_coor))
            else:
                self.ul_distance_limit=self.ul_distance_limit+1
                if self.ul_distance_limit >STORM_UL_DIS_LIMIT:
                    self.bucket[userId]=[]
                    log.debug('--filter --distance limit-: '+str(self.ul_distance_limit)+'--uid:--'+str(userId))
                    self.ul_distance_limit=0

        # else:
        #     self.bucket[userId]=[]
        #     ul_distance_limit=0

        # log.debug('userid:'+str(userId)+'--;bucket nums:'+str(len(self.bucket[userId])))


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/logs/uls_streaming/bolt/colfilter_bolt.log',
        format="%(message)s",
        filemode='a',
    )

    ulsCollectorFilterBolt().run()

