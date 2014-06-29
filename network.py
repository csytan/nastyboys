#!/usr/bin/env python

"""
Functions for network access, including fetching html and posting to forms

"""

import pycurl
from cStringIO import StringIO
from urllib import urlencode

def load_url (url, user_agent=None, proxy={}):
    """Attempt to load the url using pycurl and return the data, or None if unsuccessful"""

    databuffer = StringIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.FOLLOWLOCATION, 1)
    curl.setopt(pycurl.WRITEFUNCTION, databuffer.write)
    if user_agent:
        curl.setopt(pycurl.USERAGENT, user_agent)
    if proxy.has_key('host') and proxy.has_key('port'):
        curl.setopt(pycurl.PROXY, proxy['host'])
        curl.setopt(pycurl.PROXYPORT, proxy['port'])
        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
    try:
        curl.perform()
        data = databuffer.getvalue()
    except:
        data = None
    curl.close()

    return data

def post_url (url, data, user_agent=None, proxy={}):
    """Attempt to POST the data to the url using pycurl and return the reply or None if unsuccessful"""

    databuffer = StringIO()
    curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)
    curl.setopt(pycurl.POST, 1)
    curl.setopt(pycurl.POSTFIELDS, urlencode(data))
    curl.setopt(pycurl.WRITEFUNCTION, databuffer.write)
    if user_agent:
        curl.setopt(pycurl.USERAGENT, user_agent)
    if proxy.has_key('host') and proxy.has_key('port'):
        curl.setopt(pycurl.PROXY, proxy['host'])
        curl.setopt(pycurl.PROXYPORT, proxy['port'])
        curl.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_SOCKS5)
    try:
        curl.perform()
        data = databuffer.getvalue()
    except:
        data = None
    curl.close()

    return data
