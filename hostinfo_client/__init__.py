import os
import json
import sys
import requests

hostinfourl = 'http://hostinfo'
hostinfourl = 'http://localhost:8000'


##############################################################################
def get_origin(origin=None):
    if origin is not None:
        return origin
    try:
        user = os.environ['USER']
    except:
        user = 'unknown'
    origin = "{} by {}".format(sys.argv[0], user)
    return origin


##############################################################################
def hostinfo_cmd(cmd, verb, url, data={}, params={}):
    hi_url = '%s/api/%s' % (hostinfourl, url)
    r = cmd(hi_url, data=json.dumps(data), params=params)
    if r.status_code != 200:
        sys.stderr.write("Failed to {} {} ({})\n".format(verb, url, r.status_code))
        return None
    return r.json()


##############################################################################
def hostinfo_post(url=None, data={}, params={}):
    return hostinfo_cmd(requests.post, 'post', url, data=data, params=params)


##############################################################################
def hostinfo_get(url=None, data={}, params={}):
    return hostinfo_cmd(requests.get, 'get', url, data=data, params=params)


##############################################################################
def hostinfo_delete(url=None, data={}, params={}):
    return hostinfo_cmd(requests.delete, 'delete', url, data=data, params=params)

# EOF
