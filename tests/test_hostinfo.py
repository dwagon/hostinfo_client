#!/usr/bin/env python

import unittest

import hostinfo


##############################################################################
class TestHostinfo(unittest.TestCase):
    def test_call(self):
        hostinfo.main()

# EOF
