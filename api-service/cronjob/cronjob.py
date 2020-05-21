import schedule
import time
import requests
import json


def job():
    print("I'm working...")


def notifyLastBlockIn24Hour():
    print("notifyLastBlockIn24Hour: Get data")
    params = {
        'interval': 24,
        'shard_id': -1
    }

    r = requests.get(url="http://0.0.0.0:5000/block/shard/count-block-last-time", params=params)
    data = r.json()
    print(data)

    result = ""
    for shard, blocks in data['result']:
        result += "Shard %d: %d blocks \n" % (shard, blocks)
    print(result)

    response = requests.post(url="https://hooks.slack.com/services/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",
                             data=json.dumps({'text': result}), headers={'Content-Type': 'application/json'})
    print('Response: ' + str(response.text))
    print('Response code: ' + str(response.status_code))


# schedule.every(5).seconds.do(job)
schedule.every(5).seconds.do(notifyLastBlockIn24Hour)
# schedule.every().day.at("00:00:01").do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
