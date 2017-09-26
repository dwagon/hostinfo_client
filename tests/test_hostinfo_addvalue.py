#!/usr/bin/env python

import unittest
import responses
from hostinfo_client import hostinfourl

from bin import hostinfo_addvalue


##############################################################################
class TestHostinfo(unittest.TestCase):
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

    @responses.activate
    def test_badargs(self):
        responses.add(
            responses.POST, "{}/api/host/hosta/key/keya/foo".format(hostinfourl),
            json={'status': '200', 'result': 'ok'},
            status=200
            )
        rc = hostinfo_addvalue.main(['keyb', 'hosta'])
        self.assertEqual(rc, 1)
        self.assertEqual(len(responses.calls), 0)

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


##############################################################################
if __name__ == "__main__":
    unittest.main()

# EOF
