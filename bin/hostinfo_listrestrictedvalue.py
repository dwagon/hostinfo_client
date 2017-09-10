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
# Script to list the legal values of a restricted key

import argparse
import sys

from hostinfo_client import hostinfo_get


###############################################################################
def parse_args():
    description = 'List all allowable values of a restricted key'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('key', help='Name of the key to list')
    args = parser.parse_args()
    return args


###############################################################################
def main():
    args = parse_args()
    key = args.key.lower()
    ans = hostinfo_get('rval/{}'.format(key))
    if ans is None:
        sys.stderr.write('No key {} found\n'.format(key))
        return 1
    vals = [x['value'] for x in ans['restricted']]

    print "\n".join(sorted(vals))
    return 0


###############################################################################
if __name__ == "__main__":
    sys.exit(main())


# EOF
