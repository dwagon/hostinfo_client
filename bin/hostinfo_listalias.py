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

import sys
import argparse

from hostinfo_client import hostinfo_get


###############################################################################
def parse_args():
    description = 'List aliases'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '-a', '--all', help='List aliases for all hosts', action='store_true')
    parser.add_argument(
        'host', help='List the aliases for this host only', nargs='?')
    args = parser.parse_args()
    return args


###############################################################################
def main():
    args = parse_args()
    if args.all or not args.host:
        ans = hostinfo_get('alias')
    else:
        ans = hostinfo_get('host/{}/alias'.format(args.host))
    aliases = ans['aliases']
    output = []
    for alias in aliases:
        output.append("%s %s" % (alias['alias'], alias['host']))
    print "\n".join(output)
    return 0


###############################################################################
if __name__ == "__main__":
    sys.exit(main())

# EOF
