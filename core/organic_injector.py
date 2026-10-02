#!/usr/bin/env python3
"""
tool-citation-optima: 有机融合注入器 (Organic Provenance Injector)
解决多文档格式异构性痛点，非破坏性、渐进式将溯源对标矩阵与机器元数据有机融合入轨
100% Python 原生标准库，零外部依赖
"""
import os
import re
import json
from typing import List, Dict, Any, Optional
from datetime import datetime
from core.models import HeritageSource, ProvenanceManifest
from core.generator import ProvenanceGenerator

class OrganicInjector:
    """非破坏性、格式自适应地将引用与溯源对标有机融合至目标项目中"""

    HERITAGE_SECTION_HEADER = "## 🏛️ 技术思想溯源与全球对标矩阵 (World-Class Heritage & Prior Art)"

    def __init__(self, project_path: str):
        self.project_path = os.path.abspath(project_path)

    def inject_project(
        self,
        topic: str,
        sources: List[HeritageSource],
        target_doc: Optional[str] = None,
        abstract: Optional[str] = None,
        non_goals: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """对整个项目执行全套有机入轨 (Markdown + .provenance.json + CITATION.cff)"""
        results = {
            "project_path": self.project_path,
            "modified_files": [],
            "created_files": [],
            "fixed_point": True
        }

        # 1. 确定主文档路径 (优先选择指定的 target_doc，若无则探查 README.md)
        doc_path = self._resolve_target_doc(target_doc)
        if doc_path and os.path.isfile(doc_path):
            modified = self._inject_markdown(doc_path, topic, sources)
            if modified:
                results["modified_files"].append(os.path.relpath(doc_path, self.project_path))
                results["fixed_point"] = False

            # 若目标文档不是 README.md，且项目存在 README.md，则在 README.md 中维护轻量级门面索引 (Storefront Facade)
            readme_candidates = [os.path.join(self.project_path, fname) for fname in ("README.md", "README_CN.md")]
            for rpath in readme_candidates:
                if os.path.isfile(rpath) and os.path.abspath(rpath) != os.path.abspath(doc_path):
                    facade_mod = self._inject_readme_facade(rpath, os.path.relpath(doc_path, self.project_path), topic, len(sources))
                    if facade_mod:
                        results["modified_files"].append(os.path.relpath(rpath, self.project_path))
                        results["fixed_point"] = False
                    break

        # 2. 生成/同步 .provenance.json
        prov_path = os.path.join(self.project_path, ".provenance.json")
        prov_modified = self._sync_provenance_json(prov_path, topic, sources, non_goals)
        if prov_modified:
            if os.path.exists(prov_path):
                results["modified_files"].append(".provenance.json")
            else:
                results["created_files"].append(".provenance.json")
            results["fixed_point"] = False

        # 3. 生成/同步 CITATION.cff
        cff_path = os.path.join(self.project_path, "CITATION.cff")
        project_name = os.path.basename(self.project_path)
        proj_abstract = abstract or f"{project_name}: High-performance first-principles component with verified provenance."
        cff_modified = self._sync_citation_cff(cff_path, project_name, proj_abstract)
        if cff_modified:
            if os.path.exists(cff_path):
                results["modified_files"].append("CITATION.cff")
            else:
                results["created_files"].append("CITATION.cff")
            results["fixed_point"] = False

        return results

    def _resolve_target_doc(self, target_doc: Optional[str]) -> Optional[str]:
        """解析目标文档绝对路径，若指定文件不存在则自动创建其父目录与基础骨架"""
        if target_doc:
            p = os.path.join(self.project_path, target_doc) if not os.path.isabs(target_doc) else target_doc
            if os.path.isfile(p):
                return p
            # 若指定的 target_doc 尚未存在，允许自动创建其父目录与初始文档
            parent_dir = os.path.dirname(p)
            if parent_dir:
                os.makedirs(parent_dir, exist_ok=True)
            doc_title = os.path.splitext(os.path.basename(p))[0].replace("_", " ").title()
            with open(p, "w", encoding="utf-8") as f:
                f.write(f"# {doc_title} (技术思想溯源与全球对标档案)\n\n> 本文档为项目技术思想渊源、全球权威工程对标与取舍决策的完整归档。\n\n")
            return p

        # 默认寻找 README.md 或 主规范
        for fname in ["README.md", "README_CN.md", "SPEC.md"]:
            candidate = os.path.join(self.project_path, fname)
            if os.path.isfile(candidate):
                return candidate

        return None

    def _inject_readme_facade(self, readme_path: str, target_rel_path: str, topic: str, sources_count: int) -> bool:
        """在 README.md 中维护精简门面引用索引 (Storefront Facade)，避免大表格撑爆 README"""
        with open(readme_path, "r", encoding="utf-8", errors="replace") as f:
            original_content = f.read()

        norm_target_path = target_rel_path.replace("\\", "/")
        facade_section = (
            f"{self.HERITAGE_SECTION_HEADER}\n\n"
            f"本项目秉承第一性原理与零幻觉工程原则，严格站在全球工业标杆与开源先验的肩膀上演进构建。\n\n"
            f"完整权威源流矩阵（收录 {sources_count} 项标杆）、深度机制对标、吸收借鉴点与取舍论证详见独立档案：\n"
            f"👉 **[{norm_target_path} 完整先验对标与权威引用档案]({norm_target_path})**\n\n"
            f"*(注：机器可读元数据与规范引用已同步至 `.provenance.json` 与 `CITATION.cff`)*\n"
        )

        # 场景 A: README 中已经有这个章节头
        if self.HERITAGE_SECTION_HEADER in original_content:
            # 检查是否已经是干净的门面且链接一致
            if norm_target_path in original_content and "完整先验对标与权威引用档案" in original_content:
                # 已经是门面指针，收敛达成不动点
                return False

            # 如果原本是臃肿大表格或旧链接，将其替换为紧凑的门面索引
            pattern = re.compile(
                r'## 🏛️ 技术思想溯源与全球对标矩阵[^\n]*\n[\s\S]*?(?=\n## |\Z)',
                re.MULTILINE
            )
            updated_content = pattern.sub(facade_section.strip() + "\n\n", original_content, count=1)
            if updated_content.strip() == original_content.strip():
                return False

            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            return True

        # 场景 B: README 中尚无该章节，寻找合适锚点插入
        lines = original_content.splitlines()
        insert_idx = -1
        target_anchors = ["## 快速开始", "## 核心特性", "## 架构设计", "## 设计理念", "## 哲学", "## 快速上手", "## 特性", "## 模块划分"]
        for idx, line in enumerate(lines):
            line_s = line.strip()
            if any(line_s.startswith(anchor) for anchor in target_anchors):
                insert_idx = idx
                break

        if insert_idx != -1:
            new_lines = lines[:insert_idx] + [facade_section.strip(), ""] + lines[insert_idx:]
            final_content = "\n".join(new_lines)
        else:
            license_idx = -1
            for idx, line in enumerate(lines):
                if line.strip().startswith(("## 许可证", "## License", "## 版权")):
                    license_idx = idx
                    break
            if license_idx != -1:
                new_lines = lines[:license_idx] + [facade_section.strip(), ""] + lines[license_idx:]
                final_content = "\n".join(new_lines)
            else:
                final_content = original_content.rstrip() + "\n\n" + facade_section

        if final_content.strip() == original_content.strip():
            return False

        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(final_content)
        return True

    def _inject_markdown(self, doc_path: str, topic: str, sources: List[HeritageSource]) -> bool:
        """非破坏性将对标矩阵有机植入到 Markdown 文档的最佳锚点"""
        with open(doc_path, "r", encoding="utf-8", errors="replace") as f:
            original_content = f.read()

        new_section = ProvenanceGenerator.generate_complete_provenance_section(sources, topic)

        # 场景 A: 如果文档中已经存在对标矩阵章节
        if self.HERITAGE_SECTION_HEADER in original_content:
            # 检查现有章节是否已经包含所有给定的对标源流
            already_contains_all = all(s.name in original_content for s in sources)
            if already_contains_all:
                return False  # 已收敛且包含全部源流，不动点达成

            pattern = re.compile(
                r'## 🏛️ 技术思想溯源与全球对标矩阵[^\n]*\n[\s\S]*?(?=\n## |\Z)',
                re.MULTILINE
            )
            updated_content = pattern.sub(new_section.strip() + "\n\n", original_content, count=1)
            if updated_content.strip() == original_content.strip():
                return False  # 已收敛，无需重复写入
            
            with open(doc_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            return True

        # 场景 B: 智能寻找最自然的插入锚点 (Organic Insertion Point)
        lines = original_content.splitlines()
        insert_idx = -1

        # 倒序或正序扫描最佳插入标题
        target_anchors = ["## 快速开始", "## 核心特性", "## 架构设计", "## 设计理念", "## 哲学", "## 快速上手", "## 特性", "## 模块划分"]
        for idx, line in enumerate(lines):
            line_s = line.strip()
            if any(line_s.startswith(anchor) for anchor in target_anchors):
                insert_idx = idx
                break

        if insert_idx != -1:
            new_lines = lines[:insert_idx] + [new_section.strip(), ""] + lines[insert_idx:]
            final_content = "\n".join(new_lines)
        else:
            license_idx = -1
            for idx, line in enumerate(lines):
                if line.strip().startswith(("## 许可证", "## License", "## 版权")):
                    license_idx = idx
                    break
            if license_idx != -1:
                new_lines = lines[:license_idx] + [new_section.strip(), ""] + lines[license_idx:]
                final_content = "\n".join(new_lines)
            else:
                final_content = original_content.rstrip() + "\n\n" + new_section

        if final_content.strip() == original_content.strip():
            return False

        with open(doc_path, "w", encoding="utf-8") as f:
            f.write(final_content)
        return True

    def _sync_provenance_json(
        self,
        prov_path: str,
        topic: str,
        sources: List[HeritageSource],
        non_goals: Optional[List[str]]
    ) -> bool:
        """创建或同步 .provenance.json 机器元数据账本"""
        grounded_sources = [
            {
                "name": s.name,
                "category": s.category,
                "url": s.url,
                "stars": s.stars_or_citations,
                "core_insight": s.core_insight,
                "adopted_aspects": s.adopted_aspects,
                "tradeoff": s.rejection_reason_or_tradeoff
            }
            for s in sources
        ]

        default_nongoals = non_goals or [
            "坚决杜绝引入重型第三方未审计框架与臃肿依赖",
            "坚决拒绝只有形式文档而无真实代码的空壳八股",
            "严禁破坏现有宿主机环境或私自联网泄露凭据"
        ]

        project_name = os.path.basename(self.project_path)

        # 不动点判定：若已存在且关键源流一致，不刷新 last_updated 时间戳
        if os.path.exists(prov_path):
            try:
                with open(prov_path, "r", encoding="utf-8", errors="replace") as f:
                    old_data = json.load(f)
                old_names = set(s.get("name", "").strip() for s in old_data.get("grounded_sources", []))
                new_names = set(s.name.strip() for s in sources)
                if old_data.get("project_name") == project_name and new_names.issubset(old_names):
                    return False  # 已包含全部新源流，状态收敛
            except Exception:
                pass

        manifest = ProvenanceManifest(
            project_name=project_name,
            version="1.0.0",
            last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            search_topic=topic,
            radar_query_vectors=[f"{topic} core", f"{topic} benchmark", f"{topic} spec"],
            grounded_sources=grounded_sources,
            architectural_invariants=[
                "Negative Constraints & Architecture Sovereignty",
                "Sub-15ms Startup & Verification Latency",
                "Fixed-Point Convergence f(x) = x"
            ],
            alternatives_considered=[
                {"alternative": s.name, "reason_rejected_or_adapted": s.rejection_reason_or_tradeoff}
                for s in sources
            ],
            non_goals=default_nongoals
        )

        new_content = manifest.to_json(indent=2) + "\n"

        with open(prov_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True

    def _sync_citation_cff(self, cff_path: str, project_name: str, abstract: str) -> bool:
        """创建或同步 CITATION.cff"""
        # 不动点判定：若 CITATION.cff 已经存在且包含项目名，则保持稳定
        if os.path.exists(cff_path):
            try:
                with open(cff_path, "r", encoding="utf-8", errors="replace") as f:
                    old_cff = f.read()
                if f'title: "{project_name}"' in old_cff or f'title: {project_name}' in old_cff:
                    return False  # 已经收敛
            except Exception:
                pass

        new_content = ProvenanceGenerator.generate_cff(
            project_name=project_name,
            abstract=abstract,
            repo_url=f"https://github.com/Longgekutta/{project_name}"
        )

        with open(cff_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
