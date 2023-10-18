import http.client
import base64
import json
from datetime import datetime
import datetime
import logging
import configparser
import ssl

def logfile(filename,log):
    with open(filename ,'a') as f1:
        f1.write('%s' % str(datetime.datetime.now()) + log)
        f1.close()
    return


config = configparser.ConfigParser()
logger = logging.getLogger(__name__)
ssl._create_default_https_context = ssl._create_unverified_context
config.read("config.cfg")
debug = config['LOG']['state']

def ise_sponsor_guid():
    config.read("config.cfg")
    try:
        portalname = config["ISE"]["PORTAL"]
        host= config["ISE"]["HOST"]
        port= config["ISE"]["API_PORT"]
        api_point='/ers/config/portal'
        payload = {}
        iseuser=config["ISE"]["API_USER"]
        isepassword=config["ISE"]["API_PASS"]
        creds = str.encode(':'.join((iseuser, isepassword)))
        encodedAuth = bytes.decode(base64.b64encode(creds))
        headers = {
        'Accept': 'application/json',
        'Authorization': 'Basic ' + encodedAuth
        }
        conn = http.client.HTTPSConnection("{}:{}".format(host, port))
        conn.request("GET", api_point, headers=headers, body=payload)
        res = conn.getresponse()
        data = res.read()
        for i in json.loads(data)['SearchResult']['resources']:
            if i['description'] == portalname:
                sponsor=i['id']
                break
        iselog=' - [DEBUG] - ISE initial API connection established\n'
        print(str(datetime.datetime.now()) + iselog)
        logger.debug(iselog)
        if debug == 'True':
            logfile('ISE.log',iselog)

        return sponsor
    except:
        sponsor = ' '
        iselog=' - [ERROR] - ISE initial API connection not established\n'
        print(str(datetime.datetime.now()) + iselog)
        logger.error(iselog)
        if debug == 'True':
            logfile('ISE.log',iselog)
        
        return sponsor

print(ise_sponsor_guid())
