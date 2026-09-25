#!/usr/bin/env python3
"""
tool-citation-optima: 扫描器测试集 (Scanner Test Suite)
"""
import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scanner import ProvenanceScanner

class TestScanner(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_path = self.temp_dir.name

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_scan_heritage_table_and_footnotes(self):
        readme_content = """# Demo Project
> Motto

## 🏛️ 技术思想溯源与全球对标矩阵 (World-Class Heritage & Prior Art)

| 权威源流 | 源流分类 | 核心思想 | 借鉴要点 | 取舍区别 |
| :--- | :--- | :--- | :--- | :--- |
| **[MADR](https://adr.github.io/madr/)** [^1] | `STANDARD` | Markdown ADR 模板 | 借鉴其简炼结构 | 不引入 Node 工具 |
| **[Rust RFC](https://github.com/rust-lang/rfcs)** [^2] | `SPEC` | 严格 Prior Art 对比 | 借鉴其对比原则 | 针对通用软件架构 |
| **[Diataxis](https://diataxis.fr/)** [^3] | `STANDARD` | 文档四分法 | 借鉴架构分层 | 增加机器账本 |

### 📚 权威引用
[^1]: MADR: https://adr.github.io/madr/
[^2]: Rust RFC: https://github.com/rust-lang/rfcs
[^3]: Diataxis: https://diataxis.fr/

## 🚫 Non-Goals (坚决不做的事)
- 坚决不做八股文形式主义空壳

## 🚀 快速开始
python main.py run
"""
        with open(os.path.join(self.project_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)

        scanner = ProvenanceScanner(self.project_path)
        scan_data = scanner.scan()

        self.assertEqual(len(scan_data["heritage_tables"]), 1)
        self.assertEqual(len(scan_data["heritage_tables"][0]["rows"]), 3)
        self.assertGreaterEqual(len(scan_data["inline_citations"]), 3)
        self.assertTrue(scan_data["metrics"]["has_nongoals"])
        self.assertGreaterEqual(len(scan_data["links"]), 3)

    def test_detect_placeholder_links(self):
        doc = "[Fake Link](http://example.com/placeholder)"
        with open(os.path.join(self.project_path, "README.md"), "w", encoding="utf-8") as f:
            f.write(doc)

        scanner = ProvenanceScanner(self.project_path)
        scan_data = scanner.scan()
        self.assertEqual(len(scan_data["links"]), 1)
        self.assertTrue(scan_data["links"][0]["is_placeholder"])

if __name__ == "__main__":
    unittest.main()
