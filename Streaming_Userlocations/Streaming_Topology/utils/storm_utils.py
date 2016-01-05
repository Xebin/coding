__author__ = 'root'

# def filter_userlocaltion_spout_test(ul):
#     # keys_first=["near_home_office","userRawdataId","city","radius","street","timestamp","province","processStatus"\
#     #            ,"user","street_number","district","nation","pois","location","poiProbLv2", "poiProbLv1","objectId"]
#
#     keys_first_ul_spout=["timestamp","user","pois","location","objectId"]
#     keys_second_ul=["pois"]
#     # keys_third_ul=["location","_distance"]
#     # keys_fourth_ul=["latitude","longitude"]
#
#     for key1 in keys_first_ul_spout:
#         if ul.get(key1)==None:
#             return False
#     for key2 in keys_second_ul:
#         if ul.get("pois").get("pois")==None:
#             return False
#     return True

def valid_ul_spout(ul):
    keys_ul_spout={
        "timestamp":None,
        "user":None,
        "pois":"pois",
        "location":None,
        "objectId":None
    }
    ul_valid={}
    for key1 in keys_ul_spout.keys():
        ul_valid[key1]=ul[key1]
        key2=keys_ul_spout[key1]
        if key2!=None and ul_valid[key1].get(key2)==None:
            return None
    return ul_valid

def filter_userlocaltion_spout(ul):
    keys_ul_spout={
        "user_id":None,
        "timestamp":None,
        "pois":"pois",
        "location":None,
        "objectId":None
    }
    for key1 in keys_ul_spout.keys():
        if ul.get(key1)==None:
            return None
        elif keys_ul_spout[key1]!=None:
            key2=keys_ul_spout[key1]
            if ul.get(key1).get(key2)==None:
                return None
    return ul

















