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
                    'keyvalues':
                        {'keyname': [{'key': 'keyname', 'value': 'bar'}]}
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

##############################################################################
if __name__ == "__main__":
    unittest.main()

# EOF
