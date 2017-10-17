#!/usr/bin/env python

import unittest
import sys
import responses

from StringIO import StringIO

from hostinfo_client import hostinfourl
from bin import hostinfo


##############################################################################
class TestHostinfo(unittest.TestCase):
    def setUp(self):
        self.stdout = sys.stdout
        self.stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()

    ##########################################################################
    def tearDown(self):
        sys.stdout = self.stdout
        sys.stderr = self.stderr

    ##########################################################################
    @responses.activate
    def test_call(self):
        """ Test calling hostinfo with no arguments """
        responses.add(
            responses.GET, "{}/api/host".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}, {'hostname': 'piglet'}]},
            status=200
            )
        rc = hostinfo.main([])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 1)
        self.assertIn("deadbeef", sys.stdout.getvalue())
        self.assertIn("piglet", sys.stdout.getvalue())

    ##########################################################################
    @responses.activate
    def test_single_host(self):
        """ Test calling hostinfo with a hostname """
        responses.add(
            responses.GET, "{}/api/query/deadbeef".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}]},
            status=200
            )
        rc = hostinfo.main(['deadbeef'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 1)
        output = sys.stdout.getvalue()
        self.assertIn("deadbeef", output)

    ##########################################################################
    @responses.activate
    def test_aliases(self):
        """ Test calling hostinfo with alaises """
        responses.add(
            responses.GET, "{}/api/query/deadbeef".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}]},
            status=200
            )
        responses.add(
            responses.GET, "{}/api/host/deadbeef/alias".format(hostinfourl),
            json={"aliases": [{"alias": "livecow", "host": "deadbeef"}], "result": "ok"},
            status=200
            )
        rc = hostinfo.main(['--aliases', 'deadbeef'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 2)
        output = sys.stdout.getvalue()
        self.assertIn("deadbeef", output)
        self.assertIn("Aliases: livecow", output)

    ##########################################################################
    @responses.activate
    def test_origin_date(self):
        """ Test calling hostinfo with origin and dates """
        responses.add(
            responses.GET, "{}/api/query/deadbeef".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}]},
            status=200
            )
        responses.add(
            responses.GET, "{}/api/host/deadbeef/".format(hostinfourl),
            json={
                "host": {
                    "hostname": "deadbeef",
                    "origin": "source",
                    "createdate": "1999-12-31",
                    "modifieddate": "2000-01-01",
                    "keyvalues": {
                        "king": [
                            {
                                "value": "william",
                                "origin": "france",
                                "createdate": "1066-12-25",
                                "modifieddate": "1087-09-09"
                                }
                            ]
                        }
                    },
                "result": "ok"
                },
            status=200
            )
        rc = hostinfo.main(['--origin', '--date', '-p', 'king', 'deadbeef'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 2)
        output = sys.stdout.getvalue()
        self.assertIn("deadbeef", output)
        self.assertIn("[Origin: source]", output)
        self.assertIn("Created: 1999-12-31", output)
        self.assertIn("Modified: 2000-01-01", output)
        self.assertIn("king=william", output)
        self.assertIn("Created: 1066-12-25", output)
        self.assertIn("Modified: 1087-09-09", output)
        self.assertIn("[Origin: france]", output)

    ##########################################################################
    @responses.activate
    def test_print_val(self):
        """ Test calling hostinfo with printing a value """
        responses.add(
            responses.GET, "{}/api/query/deadbeef".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}]},
            status=200
            )
        responses.add(
            responses.GET, "{}/api/host/deadbeef/".format(hostinfourl),
            json={
                'status': '200', 'result': 'ok',
                'host': {
                    'keyvalues': {
                        'keyname': [{'key': 'keyname', 'value': 'bar'}],
                        'notherkey': [{'key': 'notherkey', 'value': 'baz'}]
                        }
                    }
                },
            status=200
            )
        rc = hostinfo.main(['-p', 'keyname', 'deadbeef'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 2)
        output = sys.stdout.getvalue()
        self.assertIn("deadbeef", output)
        self.assertIn("keyname=bar", output)
        self.assertNotIn("baz", output)

    ##########################################################################
    @responses.activate
    def test_showall(self):
        """ Test calling hostinfo with showall """
        responses.add(
            responses.GET, "{}/api/query/deadbeef".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}]},
            status=200
            )
        responses.add(
            responses.GET, "{}/api/host/deadbeef/".format(hostinfourl),
            json={
                'status': '200', 'result': 'ok',
                'host': {
                    'keyvalues': {
                        'keyname': [
                            {'key': 'keyname', 'value': 'foo'},
                            {'key': 'keyname', 'value': 'bar'}
                            ],
                        'notherkey': [{'key': 'notherkey', 'value': 'baz'}]
                        }
                    }
                },
            status=200
            )
        rc = hostinfo.main(['--showall', 'deadbeef'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 2)
        output = sys.stdout.getvalue()
        self.assertIn("deadbeef", output)
        self.assertIn("keyname: bar,foo", output)
        self.assertIn("notherkey: baz", output)

    ##########################################################################
    @responses.activate
    def test_showall_origin(self):
        """ Test calling hostinfo with showall with origin times """
        responses.add(
            responses.GET, "{}/api/query/beef.hostre".format(hostinfourl),
            json={
                'status': '200',
                'hosts': [
                    {'hostname': 'deadbeef', 'origin': 'cuisine'}
                    ]
                },
            status=200
            )
        responses.add(
            responses.GET, "{}/api/host/deadbeef/".format(hostinfourl),
            json={
                'result': 'ok',
                'host': {
                        'hostname': 'deadbeef',
                        'createdate': '2014-03-02',
                        'modifieddate': '2015-04-03',
                        'origin': 'cuisine',
                        'keyvalues': {
                            'keyname': [
                                {'key': 'keyname', 'value': 'foo', 'origin': 'alpha', 'createdate': '2016-01-02', 'modifieddate': '2016-02-03'},
                                {'key': 'keyname', 'value': 'bar', 'origin': 'beta', 'createdate': '2017-01-02', 'modifieddate': '2017-03-04'}
                                ],
                            'notherkey': [
                                {'key': 'notherkey', 'value': 'baz', 'origin': 'gamma', 'createdate': '2011-01-02', 'modifieddate': '2011-03-04'}
                                ]
                            }
                    }
                },
            status=200
            )
        rc = hostinfo.main(['--showall', '--origin', '--dates', 'beef.hostre'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 2)
        output = sys.stdout.getvalue()
        self.assertIn("deadbeef", output)
        for line in output:
            if 'deadbeef' in line:
                self.assertIn("[Origin: cuisine]", line)
                self.assertIn("Created: 2014-03-02", line)
            if 'keyname' in line:
                self.assertIn("[Origin: alpha]", line)
                self.assertIn("Created: 2017-01-02", line)
                self.assertIn("Modified: 2017-02-03", line)
        self.assertIn("keyname: bar,foo", output)
        self.assertIn("notherkey: baz", output)

    ##########################################################################
    @responses.activate
    def test_count(self):
        """ Test calling hostinfo with count"""
        responses.add(
            responses.GET, "{}/api/query/beef.hostre".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}, {'hostname': 'beeflet'}]},
            status=200
            )
        rc = hostinfo.main(['--count', 'beef.hostre'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual("2\n", sys.stdout.getvalue())

    ##########################################################################
    @responses.activate
    def test_csv(self):
        """ Test calling hostinfo CSV with no arguments """
        responses.add(
            responses.GET, "{}/api/query/beef.hostre".format(hostinfourl),
            json={'status': '200', 'result': 'ok', 'hosts': [{'hostname': 'deadbeef'}, {'hostname': 'beeflet'}]},
            status=200
            )
        rc = hostinfo.main(['--csv', 'beef.hostre'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 1)
        self.assertIn("hostname", sys.stdout.getvalue())
        self.assertIn("deadbeef", sys.stdout.getvalue())
        self.assertIn("beeflet", sys.stdout.getvalue())

    ##########################################################################
    @responses.activate
    def test_print_csv(self):
        """ Test calling hostinfo csv with printing a value """
        responses.add(
            responses.GET, "{}/api/query/beef.hostre".format(hostinfourl),
            json={
                'status': '200',
                'result': 'ok',
                'hosts': [
                    {
                        'hostname': 'deadbeef',
                        'keyvalues': {
                            'cow': [{'value': 'angus', 'key': 'cow'}],
                            'name': [{'value': 'bessy', 'key': 'name'}],
                            }
                        },
                    {
                        'hostname': 'beeflet',
                        'keyvalues': {
                            'name': [{'value': 'daisy', 'key': 'name'}],
                            }
                        }
                    ]
                },
            status=200
            )
        rc = hostinfo.main(['--csv', '-p', 'cow', 'beef.hostre'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 1)
        output = sys.stdout.getvalue()
        self.assertIn('hostname,cow', output)
        self.assertIn('deadbeef,"angus"', output)
        self.assertIn('beeflet,""', output)
        self.assertNotIn('bessy', output)


##############################################################################
if __name__ == "__main__":
    unittest.main()

# EOF
