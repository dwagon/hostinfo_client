#!/usr/bin/env python
# Written by Dougal Scott <dougal.scott@gmail.com>
#
#    Copyright (C) 2016 Dougal Scott
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

# from host.models import AllowedKey, HostinfoException
# from host.models import HostinfoCommand

import sys
import argparse
from hostinfo_client import hostinfo_get


###############################################################################
def parse_args():
    description = 'Report on available keys'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--type',
        help='Display just the types', dest='typeflag', action='store_true')
    parser.add_argument(
        'keylist',
        help="List of keys to display. Defaults to all", nargs='*')
    args = parser.parse_args()
    return args


###############################################################################
def main():
    args = parse_args()
    outstr = []
    data = hostinfo_get('key')
    keys = data['keys']

    if not keys:
        sys.stderr.write("No keys to show\n")
        sys.exit(1)

    for key in keys:
        if args.keylist:
            if key['key'] not in args.keylist:
                continue
        if args.typeflag:
            outstr.append("%s\t%s" % (key.key, key.get_validtype_display()))
        else:
            notes = "    "
            if key['restricted']:
                notes += "[KEY RESTRICTED]"
            if key['numeric']:
                notes += "[NUMERIC]"
            if key['readonly']:
                notes += "[KEY READ ONLY]"
            outstr.append("%s\t%s\t%s%s" % (key['key'], key['validtype'], key['desc'], notes))
    print("\n".join(outstr))
    return(0)


###############################################################################
if __name__ == "__main__":
    sys.exit(main())

# EOF
