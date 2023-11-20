import http.client
import base64
import json
import configparser
import ssl
#Declarete the default functions

config = configparser.ConfigParser()
ssl._create_default_https_context = ssl._create_unverified_context
config.read("config_board.cfg")


def ISE_GET_user(gurl):
    config.read("config_board.cfg")
    # host and authentication credentials
    host = config["ISE"]["HOST"]
    user = config["ISE"]["S_USER"]
    port= config["ISE"]["API_PORT"]
    password = config["ISE"]["S_PASSW"]
    conn = http.client.HTTPSConnection("{}:{}".format(host, port))
    creds = str.encode(':'.join((user, password)))
    encodedAuth = bytes.decode(base64.b64encode(creds))
    headers = {
    'accept': "application/json",
    'authorization': " ".join(("Basic",encodedAuth)),
    'cache-control': "no-cache",
    }
    conn.request("GET", gurl, headers=headers)
    res = conn.getresponse().read()
    return res


def ISE_GET_paged(page):
    config.read("config_board.cfg")
    # host and authentication credentials
    host = config["ISE"]["HOST"]
    user = config["ISE"]["S_USER"]
    port= config["ISE"]["API_PORT"]
    password = config["ISE"]["S_PASSW"]
    conn = http.client.HTTPSConnection("{}:{}".format(host, port))
    creds = str.encode(':'.join((user, password)))
    encodedAuth = bytes.decode(base64.b64encode(creds))
    headers = {
    'accept': "application/json",
    'authorization': " ".join(("Basic",encodedAuth)),
    'cache-control': "no-cache",
    }
    conn.request("GET", page, headers=headers)
    res = conn.getresponse().read()
    return res

pages="/ers/config/guestuser/?size=100&page=1"

while pages != "-":
    users = json.loads(ISE_GET_paged(pages))['SearchResult']['resources']
    for user in users:
        print(user)
        print(user['name'])
        gurl = '/ers/config/guestuser/' + user['id']
        print(json.loads(ISE_GET_user(gurl))['GuestUser'])
    try:
        page=json.loads(ISE_GET_paged(pages))['SearchResult']['nextPage']
        pages=page['href']
        #print(page)
    except:
        pages = "-"