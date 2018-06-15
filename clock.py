import os

from apscheduler.schedulers.blocking import BlockingScheduler
from oneforge import SYMBOLS, OneForge
from pymongo import MongoClient


def load_quotes(mongo, apikey=None):
    if apikey is None:
        oforge = OneForge()
    else:
        oforge = OneForge(apikey)
    quotes = oforge.quotes(SYMBOLS)
    mongo.tubatrade.quotes.insert_many(quotes)
    print(f"Updated {len(quotes)} quotes")


if __name__ == '__main__':
    mongouri = os.getenv('TUBATRADE_FOREX_MONGO_URI')
    client = MongoClient(mongouri)

    oneforge_key = os.getenv('ONEFORGE_APIKEY')

    sched = BlockingScheduler()
    sched.add_job(load_quotes, trigger='cron', args=[client], minute='*/2')
    sched.add_job(load_quotes, trigger='cron', args=[client, oneforge_key], minute='1-59/2')
    sched.start()
