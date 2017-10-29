'''
Created on 20171029

@author: zhou
'''

import urllib2, urllib, json, sys

def query_lat_long(addr,ccode):
    url = 'https://geocody.expeditedaddons.com/?api_key=48GYZWE17301O9CVDX59T6HUSPLAN8FR6I42KMQ32B705J'
    addr = addr
    ccode = ccode
    URL = url +  '&address=' + addr + '&country_code=' + ccode
    req = urllib2.Request(URL)
    resp = urllib2.urlopen(req)
    content = resp.read()
    r = json.loads(content)
    #a = r['locations'][0]['country']
    #print a, type(a)
    return r

# if __name__=='__main__':
#     query_lat_long('kenya','KE')
