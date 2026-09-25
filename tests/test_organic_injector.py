#!/usr/bin/env python3
"""
tool-citation-optima: 有机注入与不动点收敛测试集 (Injector & Fixed-Point Test Suite)
"""
import unittest
import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.organic_injector import OrganicInjector
from core.models import HeritageSource
from core.auditor import ProvenanceAuditor

class TestOrganicInjectorAndFixedPoint(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = self.temp_dir.name
        # 创建真实代码文件以通过真实性检测
        code_file = os.path.join(self.project_path, "main.py")
        with open(code_file, "w", encoding="utf-8") as f:
            f.write("\n".join([f"def step_{i}():\n    return '{i}'" for i in range(25)]))

        # 创建基础 README
        readme_file = os.path.join(self.project_path, "README.md")
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write("# Injected Project\n\n## 🚫 Non-Goals (坚决不做的事)\n- 形式主义空壳\n\n## 🚀 快速开始\npython main.py\n")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_non_destructive_injection(self):
        sources = [
            HeritageSource(
                name="MADR Template",
                category="STANDARD",
                url="https://adr.github.io/madr/",
                core_insight="Markdown Architectural Decision Records",
                adopted_aspects="Lean Markdown format",
                rejection_reason_or_tradeoff="100% Zero-Pip standard library",
                stars_or_citations=4200
            ),
            HeritageSource(
                name="W3C PROV-DM",
                category="SPEC",
                url="https://www.w3.org/TR/prov-dm/",
                core_insight="Provenance Data Model",
                adopted_aspects="Provenance graph metadata",
                rejection_reason_or_tradeoff="Zero external dependencies",
                stars_or_citations=1200
            )
        ]

        injector = OrganicInjector(self.project_path)
        # 第一次注入
        res1 = injector.inject_project(topic="测试主题", sources=sources)
        self.assertIn("README.md", res1["modified_files"])
        self.assertTrue(os.path.exists(os.path.join(self.project_path, ".provenance.json")))
        self.assertTrue(os.path.exists(os.path.join(self.project_path, "CITATION.cff")))

        # 检查注入后的 README 依然保留了原有内容
        with open(os.path.join(self.project_path, "README.md"), "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("## 🚫 Non-Goals", content)
        self.assertIn("## 🚀 快速开始", content)
        self.assertIn("MADR Template", content)

        # 第二次注入 (不动点检验: f(x) = x, 无文件被再次修改)
        res2 = injector.inject_project(topic="测试主题", sources=sources)
        self.assertEqual(len(res2["modified_files"]), 0)
        self.assertEqual(len(res2["created_files"]), 0)
        self.assertTrue(res2["fixed_point"])

    def test_end_to_end_fixed_point_audit(self):
        sources = [
            HeritageSource(
                name="MADR",
                category="STANDARD",
                url="https://adr.github.io/madr/",
                core_insight="Markdown ADR template",
                adopted_aspects="Prior art table",
                rejection_reason_or_tradeoff="Zero-pip",
                stars_or_citations=4200
            ),
            HeritageSource(
                name="Rust RFC",
                category="SPEC",
                url="https://github.com/rust-lang/rfcs",
                core_insight="Prior Art section",
                adopted_aspects="Alternatives comparison",
                rejection_reason_or_tradeoff="Generalized to pure python standard library",
                stars_or_citations=5800
            ),
            HeritageSource(
                name="Diataxis",
                category="STANDARD",
                url="https://diataxis.fr/",
                core_insight="Documentation framework",
                adopted_aspects="Explanation & Reference quadrant",
                rejection_reason_or_tradeoff="Self-contained",
                stars_or_citations=1900
            )
        ]

        injector = OrganicInjector(self.project_path)
        injector.inject_project(topic="架构溯源", sources=sources)

        auditor = ProvenanceAuditor(self.project_path)
        audit_res = auditor.audit()

        self.assertGreaterEqual(audit_res.total_score, 90)
        self.assertEqual(audit_res.rating, "S")
        self.assertTrue(audit_res.fixed_point_ready)

if __name__ == "__main__":
    unittest.main()
