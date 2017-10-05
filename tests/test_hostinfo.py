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
                        'nother': [{'key': 'nother', 'value': 'baz'}]
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
                        'nother': [{'key': 'nother', 'value': 'baz'}]
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
        self.assertIn("nother: baz", output)

##############################################################################
if __name__ == "__main__":
    unittest.main()

# EOF
