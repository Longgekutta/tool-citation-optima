#!/usr/bin/env python3
"""
tool-citation-optima: 冒烟与通用动词测试集 (Smoke & Universal Verbs Test Suite)
"""
import unittest
import os
import sys

# 注入项目根路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import main

class TestSmokeAndUniversalVerbs(unittest.TestCase):
    """测试 5 大通用动词与基本命令行响应"""

    def test_setup_verb(self):
        ret = main.cmd_setup()
        self.assertEqual(ret, 0)

    def test_health_verb(self):
        ret = main.cmd_health()
        self.assertIn(ret, (0, 1))

    def test_clean_verb(self):
        ret = main.cmd_clean()
        self.assertEqual(ret, 0)

    def test_scanner_instantiation(self):
        from core.scanner import ProvenanceScanner
        scanner = ProvenanceScanner(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        res = scanner.scan()
        self.assertIn("metrics", res)
        self.assertIsInstance(res["metrics"]["total_tables"], int)

    def test_auditor_instantiation(self):
        from core.auditor import ProvenanceAuditor
        auditor = ProvenanceAuditor(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        res = auditor.audit()
        self.assertGreaterEqual(res.total_score, 0)
        self.assertLessEqual(res.total_score, 100)
        self.assertIn(res.rating, ["S", "A", "B", "C", "F"])

if __name__ == "__main__":
    unittest.main()
