'''
Created on 20171029

@author: zhou
'''

from .forms import QueryIPForm
from flask import render_template, session, redirect, url_for, current_app,flash, abort,request, make_response, g
from flask import Response
from . import api
from queryIP import queryip
from query_lat_long import query_lat_long

@api.route('/api/query-ip', methods=['GET', 'POST'])
def query_ip():
    form = QueryIPForm()
    if form.validate_on_submit():
        ip = form.search.data
        #return redirect('http://maps.google.com/?ip=%s' % ip)
        return redirect(url_for('.ip_detail',ip=ip))
    return render_template('api/query_ip.html',form=form)

@api.route('/api/ip-detail/<ip>')
def ip_detail(ip):
    ip = queryip(ip)
    countryName = ip['countryName']
    countryCode = ip['countryCode']
    stateProv = ip['stateProv']
    continentName = ip['continentName']
    ipAddress = ip['ipAddress']
    city = ip['city']
    continentCode = ip['continentCode']
    location = query_lat_long(countryName,countryCode)
    lat = location['locations'][0]['latitude']
    lon = location['locations'][0]['longitude']
    return render_template('api/ip_detail.html', countryName=countryName,
                           countryCode=countryCode, stateProv=stateProv,
                           continentName=continentName, ipAddress=ipAddress,
                           city=city, continentCode=continentCode,
                           lat=lat, lon=lon)
    #return render_template('api/ip_detail.html',ip=ip)
