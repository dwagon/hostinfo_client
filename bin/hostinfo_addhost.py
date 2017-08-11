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

from hostinfo_client import hostinfo_post


###########################################################################
def parse_args():
    description = 'Add a new host'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='The host to add', nargs='+')
    parser.add_argument('--origin', help='The origin of this host')
    args = parser.parse_args()
    return args


############################################################################
def main():
    args = parse_args()
    for host in args.host:
        host = host.lower()
        if host[0] in ('-',):
            sys.stderr.write(
                "Host begins with a forbidden character ('{}') - not adding".format(host[0]))
            return 1
        data = hostinfo_post('host/{}'.format(host))
        if data['result'] == 'ok':
            return 0
        else:
            sys.stderr.write(data['result'])
            return 1


###############################################################################
if __name__ == "__main__":
    sys.exit(main())


# EOF
