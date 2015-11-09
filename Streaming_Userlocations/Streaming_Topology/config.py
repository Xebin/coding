__author__ = 'xebin'

import os

BASE_PATH = '/stalker/'

AV_PROD_ID = 'u7jwfvuoi3to87qtkmurvxgjdm5tmzvgpooo0d8wfm0dfdko'
AV_DEV_ID = 'm9wsdwyjnlo10b7zupagvh5wbmcdl8r91jfba1z8tov7ohv1'

AV_PROD_KEY = 'w6llno78ayu4fewyvgwr6h3v7zjqpz4g262g4htrtvw7jgdg'
AV_DEV_KEY = '3selmb59l5mrymdr6l8tkuxmk7uran2gbq3v1yes9a7oe16y'

LOGENTRIES_PROD_TOKEN = '686edabb-a540-4311-971c-82c07dccc249'
LOGENTRIES_DEV_TOKEN = 'cb115439-11d2-4bd2-9e17-bc58c3de8c47'

BUGSNAG_PROD_TOKEN = '91aa83d897021aead8efc8a2b9fd11b0'
BUGSNAG_DEV_TOKEN = '29456e5d10cb0f85a9b2f6543e5f9d86'

AV_KEY = ''
AV_ID = ''
LOGENTRIES_TOKEN = ""
BUGSNAG_TOKEN = ""
APP_ENV = ""

POI_URL = 'http://senz-parserhub.avosapps.com/pois/'
MOTION_PREDICTION = 'http://senz-senz-analyzer-motion.daoapp.io/motion_pred_ss_cosine_data/'

FIRE_BASE_URL = 'https://senz.firebaseio.com/'
FIRE_BASE_TOKEN = 'oc9zF5skwsmCdprB7CMpd7joikGUXpyBBGPbuPPd'

#test
AV_KEY = AV_PROD_KEY
AV_ID = AV_PROD_ID

LOGENTRIES_TOKEN = LOGENTRIES_DEV_TOKEN
BUGSNAG_TOKEN = BUGSNAG_DEV_TOKEN
#
#
# try:
#     APP_ENV = os.environ["APP_ENV"]
# except KeyError, key:
#     print "KeyError: There is no env var named %s" % key
#     print "The local env will be applied"
#     APP_ENV = "prod"
# finally:
#     if APP_ENV == "test":
#         AV_KEY = AV_DEV_KEY
#         AV_ID = AV_DEV_ID
#
#         LOGENTRIES_TOKEN = LOGENTRIES_DEV_TOKEN
#         BUGSNAG_TOKEN = BUGSNAG_DEV_TOKEN
#     elif APP_ENV == "prod":
#         AV_KEY = AV_PROD_KEY
#         AV_ID = AV_PROD_ID
#
#         LOGENTRIES_TOKEN = LOGENTRIES_PROD_TOKEN
#         BUGSNAG_TOKEN = BUGSNAG_PROD_TOKEN
#     elif APP_ENV == "local":
#         AV_KEY = AV_DEV_KEY
#         AV_ID = AV_DEV_ID
#
#         LOGENTRIES_TOKEN = LOGENTRIES_DEV_TOKEN
#         BUGSNAG_TOKEN = BUGSNAG_DEV_TOKEN
#
#     print 'APP_ENV:', APP_ENV
#     print 'LOGENTRIES_TOKEN:', LOGENTRIES_TOKEN
#     print 'BUGSNAG_TOKEN:', BUGSNAG_TOKEN
#
