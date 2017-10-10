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

import argparse
import sys

from hostinfo_client import hostinfo_get


###############################################################################
def parse_args(argv):
    description = 'Retrieve details from hostinfo database'
    epilog = """
     Criteria:
        var=val\tMatch hosts that have a val equal to var (or var.eq.val)
        var!=val\tMatch hosts that have a val unequal to var (or var.ne.val)
        var~val\tMatch hosts that have a var containing the string val (or var.ss.val)
        var<val\tMatch hosts that have a val less than var (or var.lt.val)
        var>val\tMatch hosts that have a val greater than var (or var.gt.val)
        var.defined\tMatch hosts that have a val set
        var.undefined\tMatch hosts that don't have a val set
        str.hostre\tMatch hosts that have str in their name
        hostname\tMatch hosts that have the name hostname
    """
    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument(
        '--showall',
        help='Print everything known about the matching hosts',
        action='store_true')
    parser.add_argument(
        '--origin',
        help='Print out origin of data',
        action='store_true')
    parser.add_argument(
        '--aliases',
        help='Print out all aliases of matching host',
        action='store_true')
    parser.add_argument(
        '--times',
        '--dates',
        help='Print out create and modification times of data',
        dest='times', action='store_true')
    parser.add_argument(
        '--noheader',
        help="Don't print headers in CSV format", dest='header',
        action='store_false', default=True)
    parser.add_argument(
        '--valuereport', help="Print out frequencies of values", nargs=1)
    parser.add_argument(
        '--host', help="For this specific host", nargs=1)
    parser.add_argument(
        '--csv', help="Print data in CSV format", action='store_true')
    parser.add_argument(
        '--xml', help="Print data in XML format", action='store_true')
    parser.add_argument(
        '--json', help="Print data in JSON format", action='store_true')
    parser.add_argument(
        '--sep', help="Use <str> as a value separator.", nargs=1, default=', ')
    parser.add_argument(
        '--hsep', help="Use <str> as a host separator.", nargs=1, default='\n')
    parser.add_argument(
        '--count', help="Return the number of matching hosts",
        action='store_true')
    parser.add_argument(
        '-p',
        help="Print values of key for matching hosts", action='append',
        dest='printout', default=[])
    parser.add_argument('criteria', nargs='*')
    args = parser.parse_args(argv)
    return args


###########################################################################
def Display(matches, args):
    """ Display the list of hosts that matched the criteria """
    # Sort the hosts alphabetically
    if args.valuereport:
        return DisplayValuereport(matches, args)
    elif args.csv:
        return DisplayCSV(matches, args)
    elif args.xml:
        return DisplayXML(matches, args)
    elif args.json:
        return DisplayJson(matches, args)
    elif args.showall:
        return DisplayShowall(matches, args)
    elif args.count:
        return DisplayCount(matches, args)
    else:
        return DisplayNormal(matches, args)


###########################################################################
def DisplayCount(matches, args):
    """ Display a count of matching hosts
    """
    return "{}\n".format(len(matches))


###########################################################################
def DisplayValuereport(matches, args):
    """ Display a report about the values a key has and how many hosts have
    that particular value
    """
#   from collections import defaultdict
#    # TODO: Migrate to using calcKeylistVals
#    outstr = ""
#    values = defaultdict(int)
#    hostids = set()   # hostids that match the criteria
#    key = getAK(args.valuereport[0])
#    total = len(matches)
#    if total == 0:
#        return ""
#    nummatch = 0
#    kvlist = KeyValue.objects.filter(
#        keyid__key=args.valuereport[0]).values_list('hostid', 'value', 'numvalue')
#
#    for hostid, value, numvalue in kvlist:
#        hostids.add(hostid)
#        if key.numericFlag and numvalue is not None:
#            values[numvalue] += 1
#        else:
#            values[value] += 1
#    nummatch = len(hostids)     # Number of hosts that match
#    numundef = total-len(hostids)
#
#    tmpvalues = []
#    for k, v in values.items():
#        p = 100.0*v/nummatch
#        tmpvalues.append((k, v, p))
#
#    tmpvalues.sort()
#
#    outstr += "%s set: %d %0.2f%%\n" % (args.valuereport[0], nummatch, 100.0 * nummatch / total)
#    outstr += "%s unset: %d %0.2f%%\n" % (args.valuereport[0], numundef, 100.0 * numundef / total)
#    outstr += "\n"
#    for k, v, p in tmpvalues:
#        outstr += "%s %d %0.2f%%\n" % (k, v, p)
#    return outstr


###########################################################################
def DisplayShowall(matches, args):
    """Display all the known information about the matched hosts
    """
    outputs = []
    for host in matches:
        outputs.append(gen_host(host, args))
    return "\n".join(outputs)


###########################################################################
def gen_host(host, args):
    outstr = ""
    output = []
    data = getHost(host['hostname'], origin=args.origin, times=args.times)

    # Generate the output string for each key/value pair
    for key in sorted(data['keyvalues'].keys()):
        dkk = data['keyvalues'][key]
        values = sorted([v['value'] for v in dkk])
        if args.origin:
            originstr = "\t[Origin: {}]".format(dkk['origin'])
        else:
            originstr = ""

        if args.times:
            timestr = "\t[Created: {} Modified: {}]".format(dkk['createdate'], dkk['modifieddate'])
        else:
            timestr = ""
        output.append("    %s: %-15s%s%s" % (key, args.sep[0].join(values), originstr, timestr))
    output.sort()

    # Generate the output for the hostname
    if args.origin:
        originstr = "\t[Origin: {}]".format(data['origin'])
    else:
        originstr = ""
    if args.times:
        timestr = "\t[Created: %s Modified: %s]" % (data['createdate'], data['modifieddate'])
    else:
        timestr = ""

    # Output the pregenerated output
    output.insert(0, "%s%s%s" % (host['hostname'], originstr, timestr))

    if args.aliases:
        output.insert(0, "    [Aliases: %s]" % (", ".join(getAliases(host['hostname'], args))))

    outstr += "\n".join(output)
    return outstr


###########################################################################
def getAliases(hostname, args):
    """ Return a list of the aliases that host has """
    url = 'host/{}/alias'.format(hostname)
    data = hostinfo_get(url)
    aliases = [_['alias'] for _ in data['aliases']]
    return aliases


###########################################################################
def DisplayXML(matches, args):
    """Display hosts and other printables in XML format
    """
#    from xml.sax.saxutils import escape, quoteattr
#   import time
#    outstr = ""
#
#    if args.showall:
#        columns = [k.key for k in AllowedKey.objects.all()]
#        columns.sort()
#    else:
#        columns = printout[:]
#
#    outstr += "<hostinfo>\n"
#    outstr += '  <query date="%s">%s</query>\n' % (time.ctime(), escape(" ".join(sys.argv)))
#    for key in columns:
#        k = getAK(key)
#        outstr += "  <key>\n"
#        outstr += "    <name>%s</name>\n" % escape(key)
#        outstr += "    <type>%s</type>\n" % k.get_validtype_display()
#        outstr += "    <readonlyFlag>%s</readonlyFlag>\n" % k.readonlyFlag
#        outstr += "    <auditFlag>%s</auditFlag>\n" % k.auditFlag
#        outstr += "    <numericFlag>%s</numericFlag>\n" % k.numericFlag
#        outstr += "    <docpage>%s</docpage>\n" % k.docpage
#        outstr += "    <desc>%s</desc>\n" % k.desc
#        if k.restrictedFlag:
#            outstr += "    <restricted>\n"
#            rvlist = RestrictedValue.objects.filter(keyid__key=key)
#            for rv in rvlist:
#                outstr += "        <value>%s</value>\n" % escape(rv.value)
#            outstr += "    </restricted>\n"
#        outstr += "  </key>\n"
#
#    for host in matches:
#        if args.aliases:
#            aliaslist = getAliases(_hostcache[host].hostname)
#        if args.origin:
#            hostorigin = ' origin="%s" ' % _hostcache[host].origin
#        else:
#            hostorigin = ''
#        if args.times:
#            hostdates = ' modified="%s" created="%s" ' % (_hostcache[host].modifieddate, _hostcache[host].createdate)
#        else:
#            hostdates = ''
#        outstr += '  <host docpage="%s" %s%s>\n' % (_hostcache[host].docpage, hostorigin, hostdates)
#        outstr += "    <hostname>%s</hostname>\n" % escape(_hostcache[host].hostname)
#        if args.aliases and aliaslist:
#            outstr += "    <aliaslist>\n"
#            for alias in aliaslist:
#                outstr += "      <alias>%s</alias>\n" % escape(alias)
#            outstr += "    </aliaslist>\n"
#        outstr += "    <data>\n"
#        for p in columns:
#            if host not in cache[p] or len(cache[p][host]) == 0:
#                pass
#            else:
#                for c in cache[p][host]:
#                    outstr += '      <confitem key="%s"' % p
#                    if args.origin:
#                        outstr += ' origin=%s' % quoteattr(c['origin'])
#                    if args.times:
#                        outstr += ' modified="%s" created="%s"' % (c['modifieddate'], c['createdate'])
#                    outstr += '>%s</confitem>\n' % escape(c['value'])
#
#        outstr += "    </data>\n"
#        outstr += "  </host>\n"
#    outstr += "</hostinfo>\n"
#    return outstr


###########################################################################
def DisplayJson(matches, args):
    """ Display hosts and other printables in JSON format
    """
#    import json
#    if args.showall:
#        columns = [k.key for k in AllowedKey.objects.all()]
#        columns.sort()
#    else:
#        columns = printout[:]
#
#    data = {}
#    for host in matches:
#        hname = _hostcache[host].hostname
#        data[hname] = {}
#        for p in columns:
#            if host not in cache[p] or len(cache[p][host]) == 0:
#                pass
#            else:
#                data[hname][p] = []
#                for c in cache[p][host]:
#                    data[hname][p].append(c['value'])
#
#    return json.dumps(data)


###########################################################################
def DisplayCSV(matches, args):
    """Display hosts and other printables in CSV format
    """
    output = []
    if args.showall:
        columns = []
        data = hostinfo_get('key')
        for k in data['keys']:
            columns.append(k['key'])
        columns.sort()
    else:
        columns = args.printout[:]

    if args.header:
        output.append("hostname{}{}".format(args.sep[0], args.sep[0].join(columns)))

    for host in matches:
        outline = "{}".format(host['hostname'])
        for p in columns:
            outline += args.sep[0]
            if p in host['keyvalues']:
                vals = sorted(host['keyvalues'][p], key=lambda x: x['value'])
            else:
                vals = ''
            outline += '"{}"'.format(args.sep[0].join([c['value'] for c in vals]))

        output.append(outline)
    return "{}\n".format("\n".join(output))


###########################################################################
def DisplayNormal(matches, args):
    """ Display hosts and other printables to stdout in human readable format
    """
    outstr = ""

    for host in matches:
        output = "{}\t".format(host['hostname'])
        if args.aliases:
            output += "[Aliases: {}]".format(", ".join(getAliases(host['hostname'], args)))
        if args.printout or args.origin or args.times:
            data = getHost(host['hostname'], origin=args.origin, times=args.times, keys=args.printout)

        # Generate the output for the hostname
        if args.origin:
            output += "[Origin: {}]\t".format(data['origin'])
        if args.times:
            output += "[Created: {} Modified: {}]\t".format(data['createdate'], data['modifieddate'])

        for p in args.printout:
            val = ""
            try:
                kvs = data['keyvalues'][p]
            except KeyError:
                output += ""
            else:
                for kv in sorted(kvs, key=lambda x: x['value']):
                    val += kv['value']
                    if args.origin:
                        val += "[Origin: %s]" % kv['origin']
                    if args.times:
                        val += "[Created: {}, Modified: {}]".format(kv['createdate'], kv['modifieddate'])
                    val += args.sep[0]
                output += "{}={}\t".format(p, val[:-1])

        outstr += "{}{}".format(output.rstrip(), args.hsep[0])
    if outstr and not outstr.endswith('\n'):
        outstr = '{}{}'.format(outstr[:-1], '\n')
    return outstr


##############################################################################
def getHost(hostname, origin=False, times=False, keys=['*']):
    url = 'host/{}/'.format(hostname)
    options = {'keys': keys}
    if times:
        options['show_dates'] = times
    if origin:
        options['show_origin'] = origin
    data = hostinfo_get(url, params=options)
    return data['host']


##############################################################################
def main(argv):
    args = parse_args(argv)
    if args.host:
        data = hostinfo_get('host/{}'.format(args.host[0]))
        data['hosts'] = data['host']
    else:
        if args.criteria:
            crit = "/".join(args.criteria)
            data = hostinfo_get('query/{}'.format(crit))
        else:
            data = hostinfo_get('host')
    output = Display(data['hosts'], args)
    if len(data['hosts']):
        retval = 0
    else:
        retval = 1
    sys.stdout.write("{}".format(output))
    return retval


##############################################################################
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

# EOF
