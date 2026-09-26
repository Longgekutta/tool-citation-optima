#!/usr/bin/env python3
"""
tool-citation-optima: 引用与元数据生成器 (Provenance Artifacts Generator)
100% Python 原生标准库，生成 CITATION.cff, .provenance.json, 对标矩阵与脚注
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.models import HeritageSource, ProvenanceManifest

class ProvenanceGenerator:
    """生成标准化机器可读元数据与高质量 Markdown 溯源内容"""

    @staticmethod
    def generate_cff(
        project_name: str,
        abstract: str,
        version: str = "1.0.0",
        authors: Optional[List[Dict[str, str]]] = None,
        repo_url: Optional[str] = None,
        license_str: str = "MIT",
        keywords: Optional[List[str]] = None,
        commit_hash: Optional[str] = None
    ) -> str:
        """生成符合 GitHub 与 CFF 1.2.0 官方规范的 CITATION.cff (YAML 格式)"""
        author_list = authors or [{"family-names": "Antigravity", "given-names": "Fleet"}]
        date_today = datetime.now().strftime("%Y-%m-%d")

        lines = [
            'cff-version: 1.2.0',
            f'title: "{project_name}"',
            f'message: "If you use or reference this project, please cite it using the metadata below."',
            'type: software',
            'authors:',
        ]
        for a in author_list:
            lines.append(f'  - family-names: "{a.get("family-names", "")}"')
            lines.append(f'    given-names: "{a.get("given-names", "")}"')
        
        lines.extend([
            f'version: "{version}"',
            f'date-released: "{date_today}"',
            f'license: "{license_str}"',
            f'abstract: "{abstract}"',
        ])
        if repo_url:
            lines.append(f'repository-code: "{repo_url}"')
        if commit_hash:
            lines.append(f'commit: "{commit_hash}"')
        if keywords:
            lines.append('keywords:')
            for kw in keywords:
                lines.append(f'  - "{kw}"')
        
        return "\n".join(lines) + "\n"

    @staticmethod
    def generate_provenance_json(manifest: ProvenanceManifest) -> str:
        """生成机器可读的 .provenance.json 元数据账本"""
        return manifest.to_json(indent=2)

    @staticmethod
    def generate_heritage_table(sources: List[HeritageSource]) -> str:
        """生成标准 Markdown 全球优秀思路与技术对标矩阵"""
        if not sources:
            return ""

        headers = ["权威源流 / 开源基座", "源流分类 / 架构层级", "核心思想 / 机制突破", "本项目吸收 / 借鉴要点", "超越点与取舍 (Trade-offs)"]
        header_line = "| " + " | ".join(headers) + " |"
        sep_line = "| " + " | ".join([":---" for _ in headers]) + " |"
        
        row_lines = []
        for idx, s in enumerate(sources, 1):
            stars_str = f" (⭐ {s.stars_or_citations})" if s.stars_or_citations else ""
            name_cell = f"**[{s.name}]({s.url})**{stars_str} [^{idx}]"
            tier_badge = getattr(s, 'tier_badge', '') or ''
            cat_str = f"`{s.category}`" + (f" `{tier_badge}`" if tier_badge else "")
            cat_cell = cat_str
            insight_cell = s.core_insight.replace("|", "&#124;").replace("\n", " ")
            adopted_cell = s.adopted_aspects.replace("|", "&#124;").replace("\n", " ")
            tradeoff_cell = s.rejection_reason_or_tradeoff.replace("|", "&#124;").replace("\n", " ")

            row = f"| {name_cell} | {cat_cell} | {insight_cell} | {adopted_cell} | {tradeoff_cell} |"
            row_lines.append(row)

        return "\n".join([header_line, sep_line] + row_lines)

    @staticmethod
    def generate_footnotes(sources: List[HeritageSource]) -> str:
        """生成 Markdown 标准脚注定义"""
        lines = []
        for idx, s in enumerate(sources, 1):
            stars_info = f" (Stars: {s.stars_or_citations})" if s.stars_or_citations else ""
            lines.append(f"[^{idx}]: **{s.name}**: [{s.url}]({s.url}){stars_info}. *{s.core_insight}*")
        return "\n".join(lines)

    @staticmethod
    def generate_complete_provenance_section(sources: List[HeritageSource], topic: str) -> str:
        """组装完整的思想溯源与全球对标矩阵章节"""
        table = ProvenanceGenerator.generate_heritage_table(sources)
        footnotes = ProvenanceGenerator.generate_footnotes(sources)

        return f"""## 🏛️ 技术思想溯源与全球对标矩阵 (World-Class Heritage & Prior Art)

> **第一性原理背景**：本项目在架构推导之初，通过全自主技术雷达 (`tool-omniscout-radar`) 对 **"{topic}"** 领域进行了极限检索与多维穿透，深度解构了全球工业界成熟方案与学术规范。
> 坚决杜绝“闭门造车”与“无根之木”，本着**“吸收精华、批判继承、杜绝冗余”**的原则确立了本项目的独创性基座。

{table}

### 📚 权威引用与事实锚点 (Normative Footnotes)
{footnotes}
"""
