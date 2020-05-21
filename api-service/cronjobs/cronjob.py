import schedule
import time
import requests
import json
import logging

from cronjobs import Webhookvivian


def job():
    logging.info("I'm working...")


def notifyLastBlockIn24Hour():
    if Webhookvivian == "":
        logging.warnings("Can not send notification because dont know webhook")
        return

    logging.info("notifyLastBlockIn24Hour: Get data")
    params = {
        'interval': 24,
        'shard_id': -1
    }

    r = requests.get(url="http://0.0.0.0:5000/block/shard/count-block-last-time", params=params)
    data = r.json()
    print(data)

    result = "Count Blocks in 24 hours\n"
    for shardId in range(len(data['result'])):
        blocks = data['result'][shardId]
        result += "Shard %d: %d blocks \n" % (shardId, blocks)
    logging.info(result)

    response = requests.post(url=Webhookvivian,
                             data=json.dumps({'text': result}), headers={'Content-Type': 'application/json'})
    logging.info('Response: ' + str(response.text))
    logging.info('Response code: ' + str(response.status_code))
    logging.info("----------------------------")
    return


schedule.every(5).seconds.do(job)
# schedule.every(5).seconds.do(notifyLastBlockIn24Hour)
schedule.every().day.at("00:00:00").do(notifyLastBlockIn24Hour)

while True:
    schedule.run_pending()
    time.sleep(1)
