#!/usr/bin/env python
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

import re
import sys
import argparse

from hostinfo_client import hostinfo_delete

# from host.models import HostinfoException, KeyValue, getAK
# from host.models import HostinfoCommand, getHost, ReadonlyValueException


###############################################################################
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'keyvalue',
        help='The key or keyvalue to delete (key[=value])')
    parser.add_argument(
        '--readonlyupdate',
        help='Write to a readonly key', action='store_true')
    parser.add_argument(
        'host',
        help='The host(s) to delete the value from', nargs='+')
    args = parser.parse_args()
    return args


##############################################################################
def main():
    args = parse_args()
    m = re.match("(?P<key>\w+)=(?P<value>.+)", args.keyvalue)
    if m:
        key = m.group('key').lower()
        value = m.group('value').lower()
    else:
        key = args.keyvalue.lower()
        value = ''
    for host in args.host:
        if value:
            hostinfo_delete('host/{}/key/{}/{}'.format(host, key, value))
        else:
            hostinfo_delete('host/{}/key/{}'.format(host, key))
    return 0


##############################################################################
if __name__ == "__main__":
    sys.exit(main())

# EOF
