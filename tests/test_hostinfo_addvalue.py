#!/usr/bin/env python

import unittest
import responses
import json
import sys

from StringIO import StringIO

from hostinfo_client import hostinfourl

from bin import hostinfo_addvalue


##############################################################################
class TestHostinfo(unittest.TestCase):
    def setUp(self):
        self.stderr = sys.stderr
        sys.stderr = StringIO()

    ##########################################################################
    def tearDown(self):
        sys.stderr = self.stderr

    ##########################################################################
    @responses.activate
    def test_call(self):
        responses.add(
            responses.POST, "{}/api/host/hosta/key/keya/foo".format(hostinfourl),
            json={'status': '200', 'result': 'ok'},
            status=200
            )
        rc = hostinfo_addvalue.main(['keya=foo', 'hosta'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 1)

    ##########################################################################
    @responses.activate
    def test_badargs(self):
        responses.add(
            responses.POST, "{}/api/host/hosta/key/keya/foo".format(hostinfourl),
            json={'status': '200', 'result': 'ok'},
            status=200
            )
        rc = hostinfo_addvalue.main(['keyb', 'hosta'])
        self.assertEqual(rc, 1)
        errout = sys.stderr.getvalue()
        self.assertIn("Must be specified in key=value format", errout)
        self.assertEqual(len(responses.calls), 0)

    ##########################################################################
    @responses.activate
    def test_readonly(self):
        responses.add(
            responses.POST, "{}/api/host/hosta/key/keyc/foo".format(hostinfourl),
            json={'status': '200', 'result': 'ok'},
            status=200
            )
        rc = hostinfo_addvalue.main(['--readonlyupdate', 'keyc=foo', 'hosta'])
        self.assertEqual(rc, 0)
        self.assertEqual(len(responses.calls), 1)
        reqdata = json.loads(responses.calls[0].request.body)
        self.assertEqual(reqdata['readonly'], True)

    ##########################################################################
    @responses.activate
    def test_origin_update(self):
        responses.add(
            responses.POST, "{}/api/host/hosta/key/keyc/foo".format(hostinfourl),
            json={'status': '200', 'result': 'ok'},
            status=200
            )
        rc = hostinfo_addvalue.main(['--origin', 'testorigin', '--update', 'keyc=foo', 'hosta'])
        reqdata = json.loads(responses.calls[0].request.body)
        self.assertEqual(reqdata['origin'], 'testorigin')
        self.assertEqual(reqdata['update'], True)
        self.assertEqual(rc, 0)


##############################################################################
if __name__ == "__main__":
    unittest.main()

# EOF
