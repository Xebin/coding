__author__ = 'xebin'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import redisco
from redisco import models

# r = redis.StrictRedis(host='120.27.30.239',port='6379')
# pool = redis.ConnectionPool(host='120.27.30.239', port=6379, db=0)
# r = redis.Redis(connection_pool=pool)
#
redisco.connection_setup(host='localhost', port=6379, db=7)


class Upoi(models.Model):
    latitude= models.FloatField(required=True)
    longitude= models.FloatField(required=True)
    upoiid=models.Attribute(required=True,unique=True)
    user_id=models.Attribute(required=True)
    cluster_type=models.Attribute(required=True)
    poi_address=models.Attribute(required=True)
    created_at = models.DateTimeField(auto_now_add=True)


def insert_upois (userid,upois):
    for upoione in upois:
        upoi=Upoi(latitude=upoione.get('location').latitude,
                        longitude=upoione.get('location').longitude,
                        upoiid=upoione.id,
                        user_id=userid,
                        cluster_type=upoione.get('cluster_type'),
                        poi_address=upoione.get('poi_address')
                        )
        try:
            upoi.save()
        except Exception:
            upoi.save()

def insert_upoi(lat,lng,upoi_id,uid,clusterType,upoi_add):
        upoi=Upoi(latitude=lat,
                        longitude=lng,
                        upoiid=upoi_id,
                        user_id=uid,
                        cluster_type=clusterType,
                        poi_address=upoi_add
                        )
        upoi.save()



def get_upois_uid(uid):
    upois=Upoi.objects.filter(user_id=uid)
    return upois

def get_upois_cluster_type(clusterType):
    upois=Upoi.objects.filter(cluster_type=clusterType)
    return upois

def get_upois_By_uid_cluster_type(uid,clusterType):
    upois=Upoi.objects.filter(cluster_type=clusterType,user_id=uid)
    return upois


#
# if __name__=="__main__":
#     # from .. import config as conf
#     import leancloud
#     leancloud.init('u7jwfvuoi3to87qtkmurvxgjdm5tmzvgpooo0d8wfm0dfdko', 'w6llno78ayu4fewyvgwr6h3v7zjqpz4g262g4htrtvw7jgdg')
#
#     user_id='5624da0960b27457e89bff13'
#     upois = av_dao.get_user_u_pois(user_id,'storm_poi_based')
#     # print str(upois[0].get('location').latitude)
#
#     insert_upois(user_id,upois)
#
#     ups=get_upois(user_id)
#     for up in ups:
#         print "upoiid:"+str(up)
#         # up.delete()

