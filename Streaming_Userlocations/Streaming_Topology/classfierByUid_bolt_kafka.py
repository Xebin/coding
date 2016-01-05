__author__ = 'xebin'
import logging
from utils import storm_utils
from pyleus.storm import SimpleBolt

from parameters import STORM_POI_USERS

log = logging.getLogger("classifierById")

class classifierByUid(SimpleBolt):
    OUTPUT_FIELDS = ["userId", "ul"]

    def process_tuple(self, tup):
        _raw_data_str = tup.values[0]
        log.debug('---get to classifier--location-:'+str(_raw_data_str['location']))

        _raw_data_dict = eval(_raw_data_str['location'])#json.dumps(_raw_data_str)
        _user_id=_raw_data_dict['user_id']

        _raw_data_dict=storm_utils.filter_userlocaltion_spout(_raw_data_dict)
        #emit : no filter users
        if _raw_data_dict!=None :#and _user_id in STORM_POI_USERS:
            self.emit((_user_id, _raw_data_dict))
            log.debug('---get to classifier-emit-location-:'+str(_raw_data_dict))
        else:
            log.debug('--ul-filter---location-:'+str(_raw_data_str))



        # # TODO: filter users.
        # if _user_id in STORM_POI_USERS:
        #     self.emit((_user_id, _raw_data_dict))
        # else:
        #     log.debug('user filtered---')

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/logs/uls_streaming/bolt/classifier_bolt.log',
        format="%(message)s",
        filemode='a',
    )

    classifierByUid().run()

