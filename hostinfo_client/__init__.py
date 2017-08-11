import sys
import requests

hostinfourl = 'http://hostinfo'
hostinfourl = 'http://localhost:8000'


##############################################################################
def hostinfo_cmd(cmd, verb, url=None):
    hi_url = '%s/api/%s' % (hostinfourl, url)
    r = cmd(hi_url)
    if r.status_code != 200:
        sys.stderr.write("Failed to {} {} ({})\n".format(verb, url, r.status_code))
        return None
    return r.json()


##############################################################################
def hostinfo_post(url=None):
    return hostinfo_cmd(requests.post, 'post', url)


##############################################################################
def hostinfo_get(url=None, payload={}):
    return hostinfo_cmd(requests.get, 'get', url)


##############################################################################
def hostinfo_delete(url=None):
    return hostinfo_cmd(requests.delete, 'delete', url)

# EOF
