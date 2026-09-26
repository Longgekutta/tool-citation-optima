#!/usr/bin/env python3
"""
tool-citation-optima: 审计器测试集 (Auditor Test Suite)
"""
import unittest
import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.auditor import ProvenanceAuditor
from core.organic_injector import OrganicInjector
from core.models import HeritageSource

class TestAuditor(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_empty_shell_penalty(self):
        # 纯空壳工程：只有 README，没有任何真实代码
        readme_content = "# Shell Project\nOnly docs here.\n"
        with open(os.path.join(self.project_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

        auditor = ProvenanceAuditor(self.project_path)
        res = auditor.audit()
        self.assertTrue(res.is_rubber_stamp_detected)
        self.assertLessEqual(res.total_score, 45)
        self.assertEqual(res.rating, "F")

    def test_grounded_project_reaches_s_tier(self):
        # 真实项目：有实体代码，且有完整溯源与元数据
        code_content = "\n".join([f"def func_{i}():\n    return {i}\n" for i in range(25)])
        with open(os.path.join(self.project_path, "main.py"), "w", encoding="utf-8") as f:
            f.write(code_content)

        readme_content = """# Genuine Project
> First-principles verified.

## 🚫 Non-Goals (坚决不做的事)
- 杜绝形式主义空壳

## 🚀 快速开始
python main.py
"""
        with open(os.path.join(self.project_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

        # 注入标准对标源流
        sources = [
            HeritageSource(
                name="MADR Template",
                category="STANDARD",
                url="https://github.com/adr/madr",
                core_insight="Markdown ADR decisions",
                adopted_aspects="Lean Markdown format",
                rejection_reason_or_tradeoff="No external node runtime required",
                stars_or_citations=4200
            ),
            HeritageSource(
                name="Rust RFC Framework",
                category="SPEC",
                url="https://github.com/rust-lang/rfcs",
                core_insight="Prior Art comparison",
                adopted_aspects="Exhaustive alternatives",
                rejection_reason_or_tradeoff="Generalized to pure python standard library",
                stars_or_citations=5800
            ),
            HeritageSource(
                name="W3C PROV-DM",
                category="SPEC",
                url="https://www.w3.org/TR/prov-dm/",
                core_insight="Data provenance model",
                adopted_aspects="Entity-Activity-Agent graph",
                rejection_reason_or_tradeoff="Simplified to .provenance.json ledger",
                stars_or_citations=1200
            )
        ]

        injector = OrganicInjector(self.project_path)
        injector.inject_project(topic="文档引用与技术溯源", sources=sources)

        auditor = ProvenanceAuditor(self.project_path)
        res = auditor.audit()

        self.assertFalse(res.is_rubber_stamp_detected)
        self.assertGreaterEqual(res.total_score, 90)
        self.assertEqual(res.rating, "S")
        self.assertTrue(res.fixed_point_ready)

    def test_skeleton_unfilled_placeholder_fails_gate(self):
        # 验证骨架占位符未填写时，门禁坚决一票否决
        code_content = "\n".join([f"def func_{i}():\n    return {i}\n" for i in range(25)])
        with open(os.path.join(self.project_path, "main.py"), "w", encoding="utf-8") as f:
            f.write(code_content)

        readme_content = "# Genuine Project\n\n## 🚫 Non-Goals\n- No empty shells\n"
        with open(os.path.join(self.project_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

        # 骨架模式来源
        sources = [
            HeritageSource(
                name="SOTA Repo",
                category="OPEN_SOURCE",
                url="https://github.com/example/sota",
                core_insight="SOTA Insight",
                adopted_aspects="<!-- AI_DECISION_ADOPT: 未填写 -->",
                rejection_reason_or_tradeoff="<!-- AI_DECISION_TRADEOFF: 未填写 -->",
                stars_or_citations=5000
            )
        ]
        injector = OrganicInjector(self.project_path)
        injector.inject_project(topic="自动化对标", sources=sources)

        auditor = ProvenanceAuditor(self.project_path)
        res = auditor.audit()
        # 门禁必须拒绝通过
        self.assertEqual(res.dimensions["rationale_and_alternatives"].status, "FAIL")
        self.assertFalse(res.fixed_point_ready)

        # 修复占位符后，门禁放行
        with open(os.path.join(self.project_path, "README.md"), "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace("<!-- AI_DECISION_ADOPT: 未填写 -->", "吸收其微内核设计").replace("<!-- AI_DECISION_TRADEOFF: 未填写 -->", "不引入其重型依赖")
        with open(os.path.join(self.project_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(c)

        res2 = auditor.audit()
        self.assertEqual(res2.dimensions["rationale_and_alternatives"].status, "PASS")

if __name__ == "__main__":
    unittest.main()

