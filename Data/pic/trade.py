from easytrader import HTTrader
import logging


# BASE_DIR = os.path.dirname(__file__)
# LOG_PATH = BASE_DIR +'/log/data_update/'
# LOG_FILENAME = str(time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))) + '.log'
logging.basicConfig(
    # filename = LOG_PATH + LOG_FILENAME,
    # level=logging.DEBUG,
    # format="[%(asctime)s] %(name)s:%(levelname)s: %(message)s"
    format="%(levelname)s: %(message)s"
)

# user = HTTrader()
# user.read_config('me.json')
# user.autologin()


import easytrader
user = easytrader.use('ht')
user.prepare('me.json')
# user.balance

a = user.balance
b = user.position
logging.info(a)
logging.info(b)


# user.buy('162411', price=0.55, amount=100)
# user.sell('162411', price=0.55, amount=100)
# user.cancel_entrust('委托单号')
# user.token='valid token'
