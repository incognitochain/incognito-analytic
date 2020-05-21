import schedule
import time
import requests
import json

from cronjobs import Webhookvivivan


def job():
    print("I'm working...")


def notifyLastBlockIn24Hour():
    if Webhookvivivan == "":
        print("Can not send notification because dont know webhook")
        return

    print("notifyLastBlockIn24Hour: Get data")
    params = {
        'interval': 24,
        'shard_id': -1
    }

    r = requests.get(url="http://0.0.0.0:5000/block/shard/count-block-last-time", params=params)
    data = r.json()
    print(data)

    result = ""
    for shardId in range(len(data['result'])):
        blocks = data['result'][shardId]
        result += "Shard %d: %d blocks \n" % (shardId, blocks)
    print(result)

    if Webhookvivivan == '':
        webhookvivivan = "https://hooks.slack.com/services/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"
    response = requests.post(url=webhookvivivan,
                             data=json.dumps({'text': result}), headers={'Content-Type': 'application/json'})
    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))
    return


# schedule.every(5).seconds.do(job)
schedule.every(5).seconds.do(notifyLastBlockIn24Hour)
# schedule.every().day.at("00:00:00").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
