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
from onlineusers import mark_online, get_online_users, get_user_last_activity
from flask_login import login_required
from flask_login.utils import current_user
from ..decorators import admin_required, permission_required
from check_mobile import checkMobile

@api.before_app_request
def checkmobile():
    MB = False
    if checkMobile(request):
        MB = True

@api.route('/api/query-ip', methods=['GET', 'POST'])
def query_ip():
    form = QueryIPForm()
    if form.validate_on_submit():
        ip = form.search.data
        #return redirect('http://maps.google.com/?ip=%s' % ip)
        return redirect(url_for('.ip_detail',ip=ip))
    return render_template('api/query_ip.html',form=form)

# @api.route('/api/ip-detail/<ip>')
# def ip_detail(ip):
#     ip = queryip(ip)
#     countryName = ip['countryName']
#     countryCode = ip['countryCode']
#     stateProv = ip['stateProv']
#     continentName = ip['continentName']
#     ipAddress = ip['ipAddress']
#     city = ip['city']
#     continentCode = ip['continentCode']
#     location = query_lat_long(countryName,countryCode)
#     if len(location['locations']) != 0:
#         lat = location['locations'][0]['latitude']
#         lon = location['locations'][0]['longitude']
#         return render_template('api/ip_detail.html', countryName=countryName,
#                            countryCode=countryCode, stateProv=stateProv,
#                            continentName=continentName, ipAddress=ipAddress,
#                            city=city, continentCode=continentCode,
#                            lat=lat, lon=lon)
#     return render_template('api/ip_detail.html', countryName=countryName,
#                                countryCode=countryCode, stateProv=stateProv,
#                                continentName=continentName, ipAddress=ipAddress,
#                                city=city, continentCode=continentCode,
#                            lat=0,lon=0)
    #return render_template('api/ip_detail.html',ip=ip)

@api.route('/api/ip-detail/<ip>')
def ip_detail(ip):
    ip = queryip(ip)
    ipAddress = ip['ip']
    ip_is_available = ip['valid']
    YIP = request.headers.get('X-Forwarded-For',request.remote_addr)
    if ip['valid'] == True:
        countryName = ip['country']
        countryCode = ip['country_code']
        region = ip['region']
        #continentName = ip['continent_code']
        ipAddress = ip['ip']
        city = ip['city']
        continentCode = ip['continent_code']
        lat = ip['latitude']
        lon = ip['longitude']
        # location = query_lat_long(countryName,countryCode)
        # if len(location['locations']) != 0:
    #   lat = location['locations'][0]['latitude']
    #   lon = location['locations'][0]['longitude']
        return render_template('api/ip_detail.html', countryName=countryName,
                            countryCode=countryCode, region=region,
                            ipAddress=ipAddress,ip_is_available=ip_is_available,
                            city=city, continentCode=continentCode,
                            lat=lat, lon=lon,YIP=YIP)
    return render_template('api/ip_detail.html', countryName='',
                               countryCode='', region='',
                               ipAddress=ipAddress,lat=0, lon=0,
                               city='', continentCode='',ip_is_available=ip_is_available,
                           YIP=YIP)


@api.before_app_request
def mark_current_user_online():
    if request.headers.get('X-Forwarded-For'):
        mark_online(request.headers['X-Forwarded-For'])
    else:
        mark_online(request.remote_addr)

@api.route('/api/online-user')
@login_required
@admin_required
def online_user():
    Online_user = get_online_users()
    for i in Online_user:
        location = queryip(i)
        city = location.get('city','kenya')
        return render_template('api/online_user.html', Online_user=Online_user, city=city)
    #return Response('Online User: %s' % ','.join(get_online_users()), mimetype='text/plain')
@api.route('/api/online-info')
def online_info():
    #raise Exception('test')
    apiua = request.headers
    return Response('Online Info: %s' % apiua)

@api.route('/api/check-mobile')
def check_mobile():
    if checkMobile(request):
        return 'Mobile'
    else:
        return 'PC'


