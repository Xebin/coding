__author__ = 'xebin'
import logging

from pyleus.storm import SimpleBolt
import numpy as np
from parameters import STORM_POI_DURATION_LIMIT,STORM_POI_SAMPLES_BUCKET_NUMBER,CLUSTER_TYPE_STORM_POI_BASED,CLUSTER_NEAR_POI_NUMBER
from dao import av_dao,mongo_dao,redis_dao
log = logging.getLogger("new_poi_find_Bolt")
from utils.algo_utils import near_u_poi
from utils import algo_utils
class newPoisFindingBolt(SimpleBolt):

    OUTPUT_FIELDS = ["userId", "bucket"]

    def process_tuple(self, tup):
        userId,bucket = tup.values
        bucket_time = sorted(bucket, key=lambda k: k.get('timestamp'))

        ts_start=long(bucket_time[0]['timestamp'])
        ts_end=long(bucket_time[-1]['timestamp'])
        duration=ts_end-ts_start
        sample_num=len(bucket_time)
        sample_coordinates=[]
        log.debug('timebucket--get--num:'+str(len(bucket_time))+'---duration--: '+str(duration))

        if duration>STORM_POI_DURATION_LIMIT-10*60*1000 and sample_num>STORM_POI_SAMPLES_BUCKET_NUMBER :
            centers = np.zeros((2), dtype=np.float)
            count=0
            # log.debug('center find --ahead--:'+str(sample_num))

            for ul in bucket_time:
                # sample_coordinates.append(ul['location'].lat,ul['location'].lng)
                centers += (ul['location']['lat'],ul['location']['lng'])
                count=count+1
            center=centers/count
            center_uls_list=[]
            center_uls_list.append([center,bucket_time])
            log.debug('all_center--:'+str(center))

            # filter existing u_poi
            u_pois=redis_dao.get_upois(userId)
            if len(u_pois)==0:
                u_pois = av_dao.get_user_u_pois(userId, CLUSTER_TYPE_STORM_POI_BASED)
                redis_dao.insert_upois(u_pois)
            u_pois=redis_dao.get_upois(userId)

            new_center_evidences_list = self.__filter_existed_centers(center_uls_list,u_pois)

            if len(new_center_evidences_list)!=0 and new_center_evidences_list!=None:
                log.debug('new_center--:'+str(center))

                # save result
                new_u_pois_gp_uid = {}
                new_u_pois_gp_uid[userId] = self.__save_cluster_results('storm new poi',
                                                                userId,
                                                                new_center_evidences_list,
                                                                CLUSTER_TYPE_STORM_POI_BASED)
                log.debug('center find --poi--:'+str(center)+'---save...')

    def __filter_existed_centers(self,center_evidences_list,u_pois):
        filtered = []
        for center_evidence in center_evidences_list:

            is_new = True
            for upoi in u_pois:
                center = center_evidence[0]

                upoi_coor = [upoi.latitude, upoi.longitude]

                if near_u_poi(center, upoi_coor):
                    is_new = False
                    break

            if is_new:
                filtered.append(center_evidence)
        return filtered

    def __save_cluster_results(self,request_id, uid, u_poi_center_evidences_list, cluster_type):
        new_u_poi_ids = []
        for center_evidences in u_poi_center_evidences_list:

            coordinate = center_evidences[0]  # u poi coordinate

            if coordinate == None or len(coordinate) == 0:
                log.debug('--no coordinate...')

            evidences = center_evidences[1]  # user locations

            if cluster_type == 'poi_based':
                poi_title = center_evidences[2]
            elif cluster_type==CLUSTER_TYPE_STORM_POI_BASED:
                poi_title = CLUSTER_TYPE_STORM_POI_BASED
            else:
                poi_title=None


            # Save new u_poi
            upoi_evidences = {}
            # get poi -> u_poi
            # pois = algo_utils.get_near_pois(request_id, uid, coordinate, CLUSTER_NEAR_POI_NUMBER)
            pois=av_dao.get_near_pois(coordinate,evidences)
            if pois == None or len(pois) == 0:

                # print 'upoi dont have a poi coor:', coordinate, 'poi_title:', poi_title

                upoi_evidences['u_poi'] = av_dao.save_u_poi(coordinate=coordinate,
                                                     user_id=uid,
                                                     poi_label=None,
                                                     poi_type=None,
                                                     poi_title=None,
                                                     poi_address=None,
                                                     poi_coordinate=None,
                                                     near_pois=None,
                                                     cluster_type=cluster_type
                                                     )
                log.warn_no_poi_u_poi(request_id, upoi_evidences['u_poi'].id)

            else:
                poi = pois[0] # nearest poi
                poi_coordinate = [poi['location']['latitude'], poi['location']['latitude']]

                upoi_evidences['u_poi'] = av_dao.save_u_poi(coordinate=coordinate,
                                                     user_id=uid,
                                                     poi_label=poi['type']['mapping_type'],
                                                     poi_type=poi['type'],
                                                     poi_title=poi['title'],
                                                     poi_address=poi['address'],
                                                     poi_coordinate=poi_coordinate,
                                                     near_pois=pois,
                                                     cluster_type=cluster_type
                                                     )
                redis_dao.insert_upoi(poi_coordinate[0],
                                      poi_coordinate[1],
                                      upoi_evidences['u_poi'].id,
                                      uid,
                                      cluster_type,
                                      poi['address']
                                      )
            upoi_evidences['evidences'] = evidences

            # SAVE marked_UserLocation
            # mark cluster
            for user_location in upoi_evidences['evidences']:
                mongo_dao.saveMarkedUserLocation(request_id,
                                             user_location_id=user_location.get('_id'),
                                             timestamp=user_location.get('timestamp'),
                                             geo_point=user_location.get('location'),
                                             u_poi_id=upoi_evidences['u_poi'].id
                                             )

            # new_u_pois_gp_uid[uid].append(upoi_evidences['u_poi'].id)
            new_u_poi_ids.append(upoi_evidences['u_poi'].id)

        return new_u_poi_ids

if __name__ == '__main__':
    import config as conf
    import leancloud
    leancloud.init(conf.AV_ID, conf.AV_KEY)

    logging.basicConfig(
        level=logging.DEBUG,
        filename='/logs/uls_streaming/bolt/newPoisFinding_Bolt.log',
        format="%(message)s",
        filemode='a',
    )

    newPoisFindingBolt().run()

