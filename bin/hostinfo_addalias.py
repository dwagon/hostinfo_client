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
from hostinfo_client import hostinfo_post


###############################################################################
def parse_args():
    description = 'Add alias to a host'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('host', help='The host to add the alias for')
    parser.add_argument('alias', help='The alias for the host')
    parser.add_argument('--origin', help='The origin of this alias')
    args = parser.parse_args()
    return args


###############################################################################
def main():
    args = parse_args()
    host = args.host.lower()
    alias = args.alias.lower()
    params = {'origin': args.origin}
    hostinfo_post('host/{}/alias/{}'.format(host, alias), params=params)
    return 0


###############################################################################
if __name__ == "__main__":
    sys.exit(main())

# EOF
