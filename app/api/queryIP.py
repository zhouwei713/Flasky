'''
Created on 20171028

@author: zhou
'''

import sys, urllib, urllib2, json

def queryip(ip):
    url = 'http://api.db-ip.com/v2/134f97b646b750bb40d074c9164620e8c86cbebb/'
    URL = url + ip
    req = urllib2.Request(URL)
    resp = urllib2.urlopen(req)
    content = resp.read()
    r = json.loads(content)
    # a = type(content)
    # b = type(r)
    #print  r, r['city']
    return r

# if __name__=='__main__':
#     queryip('103.235.46.39')
