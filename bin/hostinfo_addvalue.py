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

import re
import sys
import argparse

from hostinfo_client import hostinfo_post, get_origin


###############################################################################
def parse_args():
    description = 'Add a value to a hosts key'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-o', '--origin', help='The origin of this data', default=None)
    parser.add_argument('-a', '--append', help='Append to a list type key', action='store_true')
    parser.add_argument('-u', '--update', help='Replace an existing value', action='store_true')
    parser.add_argument('--readonlyupdate', help='Write to a readonly key', action='store_true')
    parser.add_argument('keyvalue', help='Name of the key/value pair to add (key=value)')
    parser.add_argument('host', help='Host(s) to add this value to', nargs='+')
    args = parser.parse_args()
    return args


###########################################################################
def main():
    args = parse_args()
    data = {'nohost': True, 'norigin': True}
    m = re.match("(?P<key>\w+)=(?P<value>.+)", args.keyvalue)
    if not m:
        sys.stderr.write("Must be specified in key=value format\n")
        return 1
    key = m.group('key').lower()
    value = m.group('value').lower()
    data['origin'] = get_origin(args.origin)
    if args.readonlyupdate:
        data['readonly'] = True
    if args.update:
        data['update'] = True
    if args.append:
        data['append'] = True
    for host in args.host:
        host = host.lower().strip()
        ans = hostinfo_post('host/{}/key/{}/{}'.format(host, key, value), data=data)
        if not ans['status'].startswith('2'):
            print(ans['error'])
            return 1
        print(ans['result'], ans['status'])
    return 0


##############################################################################
if __name__ == "__main__":
    sys.exit(main())

# EOF
