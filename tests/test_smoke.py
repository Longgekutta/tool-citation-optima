#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import main


class TestSmoke(unittest.TestCase):
    def test_health(self):
        self.assertEqual(main.health_check(), 0)

    def test_run(self):
        self.assertEqual(main.run_workload(), 0)


if __name__ == "__main__":
    unittest.main()
