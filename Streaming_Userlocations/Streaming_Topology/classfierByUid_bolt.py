__author__ = 'xebin'
import logging
import json
import time
from pyleus.storm import SimpleBolt

from parameters import STORM_POI_USERS

log = logging.getLogger("classifierById")
null=None

class classifierByUid(SimpleBolt):
    OUTPUT_FIELDS = ["userId", "ul"]

    def process_tuple(self, tup):
        _user_id,_raw_data_str = tup.values
        # _raw_data_dict = json.loads(_raw_data_str)
        global null
        log.debug(str(_user_id)+'---get to classifier----stmp:'+str(_raw_data_str['timestamp']))
        # _user_id  = _raw_data_dict["user_id"]
        userlocation = _raw_data_str

        # TODO: filter users.
        # if _user_id in STORM_POI_USERS:
        self.emit((_user_id, userlocation))
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

