import requests
import sys, os
import json
import logging
import logging.handlers


def shaCheck(api_key, hash):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'
    parameters = {'apikey': api_key, 'resource': hash}
    headers = {"Accept-Encoding": "gzip, deflate"}
    r = requests.post(url, headers=headers, params=parameters)
    result = r.json()
    jresult = json.dumps(result)
    return jresult


def setup_logger(level):
    logger = logging.getLogger("shaChecker_alert_logger")
    logger.propagate = False
    logger.setLevel(level)
    file_handler = logging.handlers.RotatingFileHandler(
    os.environ['SPLUNK_HOME'] + '/var/log/splunk/shaChecker_alert_logger.log', maxBytes=250000000, backupCount=5)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = setup_logger(logging.INFO)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--execute":
        payload = json.loads(sys.stdin.read())
        logger.info(payload)
        config = payload.get("configuration")
        api_ley = config.get("APIKey")
        list_id = config.get("listid")
        list_lang = config.get("listlang")
        event_result = payload.get("result")
        movie_id = event_result.get("Column1")
        data = shaCheck(api_ley, movie_id)
        file = open("/opt/splunk/etc/apps/shaChecker/bin/logdosyasi.txt", "a")
        file.write(data)
        file.close()


if __name__ == '__main__':
    main()
