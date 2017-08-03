#!/usr/bin/env python
#
# Written by Dougal Scott <dougal.scott@gmail.com>
#
#    Copyright (C) 2017 Dougal Scott
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import sys

import requests

hostinfourl = 'http://hostinfo'
hostinfourl = 'http://localhost:8000'


##############################################################################
def hostinfo_get(url=None, payload={}):
    hi_url = '%s/api/%s' % (hostinfourl, url)
    r = requests.get(hi_url, params=payload)
    if r.status_code != 200:
        sys.stderr.write("Failed to get %s (%s)\n" % (url, r.status_code))
        return None
    return r.json()


##############################################################################
def hostinfo_delete(url=None):
    hi_url = '%s/api/%s' % (hostinfourl, url)
    r = requests.delete(hi_url)
    if r.status_code != 200:
        sys.stderr.write("Failed to delete %s (%s)\n" % (url, r.status_code))
        return None
    return r.json()


###########################################################################
def parse_args():
    description = 'Delete a host'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--lethal',
        help='Actually do the delete - NO UNDO', action='store_true')
    parser.add_argument(
        'host',
        help='Name of host to delete')
    args = parser.parse_args()
    return args


###########################################################################
def main():
    args = parse_args()
    host = args.host.lower()
    data = hostinfo_get('host/{}'.format(host))
    if not data:
        sys.stderr.write("Host {} doesn't exist\n".format(host))
        return(1)

    if not args.lethal:
        sys.stderr.write("Didn't do delete as no --lethal specified\n")
        return(0)

    data = hostinfo_delete('host/{}'.format(host))
    return 0


###############################################################################
if __name__ == "__main__":
    sys.exit(main())

# EOF
