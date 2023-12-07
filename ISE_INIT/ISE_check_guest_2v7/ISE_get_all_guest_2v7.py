# ISE 2.7 compatible GET all guest user information script
import http.client
import base64
import json
import configparser
import ssl
#Declarete the default functions


def ISE_GET_user(gurl):
    # host and authentication credentials
    config.read("config.cfg")
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
    #print(res)
    return res


def ISE_GET_paged(page):
    # host and authentication credentials
    config.read("config.cfg")
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
    #print(res)
    return res

config = configparser.ConfigParser()
config.read("config.cfg")
ssl._create_default_https_context = ssl._create_unverified_context
guest_type = config["ISE"]["GUEST_TYPE"]
pages="/ers/config/guestuser/?size=100&page=1"
i=0
p=1
j=0
with open('guest.csv', 'w') as f:
    f.write('%s' % 'userName' + ',' + 'firstName' +','+'lastName'+','+'emailAddress'+','+'phoneNumber' +','+'status' + ','+'guestType'+ ','+'sponsorUserName'+'\n')
    f.close()
with open('original_data.txt' , 'w') as f:
    f.close()
with open('guest.csv', 'a') as f:
    while pages != "-":
        #print(pages)
        p=p+1
        users = json.loads(ISE_GET_paged(pages ))['SearchResult']['resources']
        #page=json.loads(ISE_GET_paged(pages))['SearchResult']
        #print(page)
        j=i
        with open('original_data.txt', 'a' , encoding='utf-8') as f1:
            for user in users:
                #print(user)
                #print(user['name'])
                gurl = '/ers/config/guestuser/' + user['id']
                guest=json.loads(ISE_GET_user(gurl))['GuestUser']
                #print(guest)
                f1.write('%s' % str(guest) + '\n')
                try:
                   sponsorUserName = guest['sponsorUserName']
                except:
                    sponsorUserName  = ''
                try:
                    userName=guest['guestInfo']['userName']
                except:
                    username = ''
                try:
                    firstName = guest['guestInfo']['firstName']
                except:
                    firstName = ''
                try:
                    lastName = guest['guestInfo']['lastName']
                except:
                    lastName = ''
                try:
                    emailAddress = guest['guestInfo']['emailAddress']
                except:
                    emailAddress = ''
                try:
                    phoneNumber = guest['guestInfo']['phoneNumber']
                except:
                    phoneNumber = ''
                datas =  userName + ',' + firstName +','+lastName+','+emailAddress+','+phoneNumber + ','+guest['status'] + ',' +guest['guestType'] + ','+sponsorUserName + '\n'
                if( guest_type == "all"):
                    #print(guest)
                    f.write('%s' % datas)
                    i=i+1
                    print(i)
                    print(datas)
                else:
                    if(guest['guestType'] == guest_type):
                        f.write('%s' % datas)
                        i=i+1
                        print(i)
                        print(datas)
        f1.close()
        

        if(i!=j):
            pages="/ers/config/guestuser/?size=100&page=" + str(p)
        else:
            pages = "-"
f.close()
print(i)