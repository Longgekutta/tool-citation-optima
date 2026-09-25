#!/usr/bin/env python3
"""
tool-citation-optima: 雷达桥接测试集 (Radar Bridge Test Suite)
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.radar_bridge import RadarBridge

class TestRadarBridge(unittest.TestCase):

    def test_radar_detection(self):
        radar = RadarBridge()
        self.assertTrue(radar.is_available())
        reports = radar.list_existing_reports()
        self.assertIsInstance(reports, list)
        self.assertGreater(len(reports), 0)

    def test_load_and_extract_sources(self):
        radar = RadarBridge()
        reports = radar.list_existing_reports()
        target_report = None
        for r in reports:
            if "citation" in r or "architecture" in r or "software" in r:
                target_report = r
                break
        if not target_report and reports:
            target_report = reports[0]

        self.assertIsNotNone(target_report)
        data = radar.load_report(target_report)
        self.assertIn("reports", data)

        sources = radar.extract_heritage_sources(data, max_items=3)
        self.assertIsInstance(sources, list)
        if sources:
            self.assertTrue(hasattr(sources[0], "name"))
            self.assertTrue(hasattr(sources[0], "url"))
            self.assertTrue(hasattr(sources[0], "core_insight"))

if __name__ == "__main__":
    unittest.main()
