#!/usr/bin/env python3
"""
tool-citation-optima: 雷达桥接测试集 (Radar Bridge Test Suite)
自洽独立性设计：兼容本地具备 omniscout-radar 与云端 CI 隔离沙箱环境
"""
import unittest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.radar_bridge import RadarBridge

class TestRadarBridge(unittest.TestCase):

    def test_radar_detection(self):
        radar = RadarBridge()
        # 验证返回为严格布尔类型
        self.assertIsInstance(radar.is_available(), bool)
        reports = radar.list_existing_reports()
        self.assertIsInstance(reports, list)

    def test_load_and_extract_sources(self):
        radar = RadarBridge()
        
        # 构造自洽雷达报告数据 (确保在 CI 与本地均能独立运行)
        mock_data = {
            "meta": {
                "domain_topic": "citation markdown provenance",
                "domain_anchor": "citation"
            },
            "reports": [
                {
                    "repo_name": "PleasePrompto/notebooklm-skill",
                    "url": "https://github.com/PleasePrompto/notebooklm-skill",
                    "stars": 7778,
                    "description": "Source grounded citation skill",
                    "score": 80,
                    "recommendation": "EVALUATE (深度跟进评测)"
                },
                {
                    "repo_name": "flozxwer/FreeCite",
                    "url": "https://github.com/flozxwer/FreeCite",
                    "stars": 44,
                    "description": "Open source citation parser",
                    "score": 90,
                    "recommendation": "ADOPT (放入武器库/标杆底座)"
                }
            ]
        }

        # 若本地存在真实报告，则测试真实加载；否则使用自洽数据
        reports = radar.list_existing_reports()
        if reports:
            data = radar.load_report(reports[0])
            self.assertIn("reports", data)
        else:
            data = mock_data

        sources = radar.extract_heritage_sources(data, max_items=3)
        self.assertIsInstance(sources, list)
        self.assertGreater(len(sources), 0)
        self.assertTrue(hasattr(sources[0], "name"))
        self.assertTrue(hasattr(sources[0], "url"))
        self.assertTrue(hasattr(sources[0], "core_insight"))

if __name__ == "__main__":
    unittest.main()
