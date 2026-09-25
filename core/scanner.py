#!/usr/bin/env python3
"""
tool-citation-optima: 文档引用与技术溯源扫描器 (Documentation Provenance Scanner)
100% Python 原生标准库，纯 AST/正则轻量解析，零外部依赖，毫秒级响应
"""
import os
import re
import json
from typing import Dict, List, Any, Optional
from core.models import HeritageSource

class ProvenanceScanner:
    """全面扫描项目说明文档中的引用、溯源对标矩阵、内联脚注及元数据"""

    # 常见文档文件匹配模式
    DOC_PATTERNS = ["README.md", "README_CN.md", "ARCHITECTURE.md", "CORE_INVARIANTS.md", "PAVED_ROAD.md"]

    def __init__(self, project_path: str):
        self.project_path = os.path.abspath(project_path)

    def scan(self) -> Dict[str, Any]:
        """执行全盘扫描并返回结构化扫描结果"""
        doc_files = self._collect_doc_files()
        
        tables = []
        inline_citations = []
        links = []
        nongoal_sections = []
        doc_contents = {}

        for fpath in doc_files:
            rel_path = os.path.relpath(fpath, self.project_path)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                doc_contents[rel_path] = content
                
                # 1. 扫描对标矩阵表格
                found_tables = self._extract_heritage_tables(content, rel_path)
                tables.extend(found_tables)

                # 2. 扫描内联脚注与引用
                found_citations = self._extract_inline_citations(content, rel_path)
                inline_citations.extend(found_citations)

                # 3. 扫描提取所有外链
                found_links = self._extract_links(content, rel_path)
                links.extend(found_links)

                # 4. 扫描 Non-goals / Alternatives 结构
                found_nongoals = self._extract_nongoals_and_alternatives(content, rel_path)
                nongoal_sections.extend(found_nongoals)

            except Exception as e:
                pass

        # 5. 扫描机器可读元数据文件
        machine_meta = self._scan_machine_metadata()

        return {
            "project_path": self.project_path,
            "scanned_docs": list(doc_contents.keys()),
            "doc_contents": doc_contents,
            "heritage_tables": tables,
            "inline_citations": inline_citations,
            "links": links,
            "nongoal_sections": nongoal_sections,
            "machine_meta": machine_meta,
            "metrics": {
                "total_tables": len(tables),
                "total_table_rows": sum(len(t.get("rows", [])) for t in tables),
                "total_inline_citations": len(inline_citations),
                "total_links": len(links),
                "has_provenance_json": machine_meta["has_provenance_json"],
                "has_citation_cff": machine_meta["has_citation_cff"],
                "has_nongoals": len(nongoal_sections) > 0,
            }
        }

    def _collect_doc_files(self) -> List[str]:
        """收集项目中所有关键文档文件 (根目录常用文档 + specs/ + docs/)"""
        candidates = []
        if not os.path.exists(self.project_path):
            return candidates

        for root, dirs, files in os.walk(self.project_path):
            # 忽略 git, cache, node_modules 等目录
            dirs[:] = [d for d in dirs if d not in (".git", ".cache", "__pycache__", "node_modules", ".venv", "venv")]
            rel_dir = os.path.relpath(root, self.project_path)
            
            # 仅限根目录、specs、docs、spec 目录
            is_allowed_dir = (rel_dir == "." or rel_dir in ("specs", "docs", "spec", "decisions", "adr"))
            if not is_allowed_dir and not any(rel_dir.startswith(p) for p in ("specs", "docs", "spec", "decisions", "adr")):
                continue

            for f in files:
                if f.endswith(".md") or f.endswith(".markdown"):
                    candidates.append(os.path.join(root, f))

        return candidates

    def _extract_heritage_tables(self, content: str, doc_rel_path: str) -> List[Dict[str, Any]]:
        """从 Markdown 中提取思想溯源与全球对标矩阵表格"""
        results = []
        # 正则定位表头，寻找类似 "源流|思想|借鉴|取舍" 或 "Prior Art|Heritage|Alternatives" 的表头
        table_pattern = re.compile(
            r'(\|[^\n]+\|\n\|[\s\-:|]+\|\n(?:\|[^\n]+\|\n?)+)',
            re.MULTILINE
        )
        
        for match in table_pattern.finditer(content):
            table_text = match.group(1).strip()
            lines = [l.strip() for l in table_text.splitlines() if l.strip()]
            if len(lines) < 3:
                continue
            
            headers = [c.strip() for c in lines[0].strip("|").split("|")]
            header_str = " ".join(headers).lower()

            # 判定是否属于溯源/对标表
            is_heritage = any(k in header_str for k in [
                "源流", "对标", "思想", "借鉴", "取舍", "区别", "备选",
                "heritage", "prior art", "alternative", "origin", "benchmark", "comparison", "provenance"
            ])
            
            if is_heritage:
                rows = []
                for line in lines[2:]:
                    cols = [c.strip() for c in line.strip("|").split("|")]
                    if any(cols):
                        rows.append(cols)
                results.append({
                    "doc": doc_rel_path,
                    "headers": headers,
                    "rows": rows,
                    "raw_table": table_text
                })

        return results

    def _extract_inline_citations(self, content: str, doc_rel_path: str) -> List[Dict[str, Any]]:
        """提取内联脚注、角标引用与参考文献定义"""
        citations = []

        # 匹配脚注标记: [^1], [^madr], [^rfc1234]
        footnote_refs = re.findall(r'\[\^([a-zA-Z0-9_\-]+)\]', content)
        # 匹配脚注定义: [^1]: http://... 或 [^madr]: Title
        footnote_defs = re.findall(r'\[\^([a-zA-Z0-9_\-]+)\]:\s*([^\n]+)', content)
        
        # 匹配标准括号学术引用: [@citekey] 或 [1]
        academic_refs = re.findall(r'\[@([a-zA-Z0-9_\-]+)\]', content)

        # 匹配“技术溯源 / 引用文献”段落中的有序或无序引用列表: [1] Author, Title, URL
        ref_block_pattern = re.compile(
            r'(?:##\s*(?:技术溯源|参考文献|References|Citations|Bibliography|Prior Art)[^\n]*\n)([\s\S]*?)(?:\n##|\Z)',
            re.IGNORECASE
        )
        ref_blocks = ref_block_pattern.findall(content)
        explicit_refs_count = 0
        for block in ref_blocks:
            lines = [l.strip() for l in block.splitlines() if l.strip().startswith(("-", "*", "1.", "2.", "3.", "4.", "5.", "[", "`"))]
            explicit_refs_count += len(lines)

        for r in set(footnote_refs):
            citations.append({"type": "FOOTNOTE_REF", "key": r, "doc": doc_rel_path})
        for k, v in footnote_defs:
            citations.append({"type": "FOOTNOTE_DEF", "key": k, "value": v, "doc": doc_rel_path})
        for a in set(academic_refs):
            citations.append({"type": "ACADEMIC_REF", "key": a, "doc": doc_rel_path})

        if explicit_refs_count > 0:
            citations.append({"type": "REF_BLOCK_ITEMS", "count": explicit_refs_count, "doc": doc_rel_path})

        return citations

    def _extract_links(self, content: str, doc_rel_path: str) -> List[Dict[str, Any]]:
        """提取文档中的链接并进行有效性分类校验"""
        links = []
        raw_links = re.findall(r'\[([^\]]*)\]\((https?://[^\)\s]+)\)', content)
        
        for anchor, url in raw_links:
            # 过滤内部纯徽章或空链接
            is_placeholder = any(p in url.lower() for p in ["example.com", "placeholder", "localhost", "127.0.0.1", "test.com"])
            is_badge = any(b in url.lower() for b in ["shields.io", "badge.svg", "travis-ci", "coveralls.io"])
            is_github = "github.com" in url.lower()
            is_academic = any(a in url.lower() for a in ["doi.org", "arxiv.org", "ieee.org", "acm.org", "ietf.org"])

            links.append({
                "anchor": anchor.strip(),
                "url": url.strip(),
                "doc": doc_rel_path,
                "is_placeholder": is_placeholder,
                "is_badge": is_badge,
                "is_github": is_github,
                "is_academic": is_academic
            })

        return links

    def _extract_nongoals_and_alternatives(self, content: str, doc_rel_path: str) -> List[Dict[str, Any]]:
        """检测 Non-Goals 与 Alternatives Considered 章节"""
        sections = []
        keywords = ["non-goal", "non goals", "坚决不做", "非目标", "alternatives considered", "备选方案", "取舍", "trade-off"]
        
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            l_lower = line.lower().strip()
            if l_lower.startswith("#") and any(k in l_lower for k in keywords):
                # 抓取该段落的前后内容摘要
                snippet = "\n".join(lines[idx:min(idx + 10, len(lines))])
                sections.append({
                    "title": line.strip(),
                    "doc": doc_rel_path,
                    "line_number": idx + 1,
                    "snippet": snippet
                })

        return sections

    def _scan_machine_metadata(self) -> Dict[str, Any]:
        """扫描 .provenance.json 与 CITATION.cff 等机器可读元数据"""
        meta_info = {
            "has_provenance_json": False,
            "provenance_data": None,
            "has_citation_cff": False,
            "citation_cff_content": None,
            "provenance_path": None,
            "citation_cff_path": None
        }

        prov_path = os.path.join(self.project_path, ".provenance.json")
        if os.path.exists(prov_path):
            meta_info["has_provenance_json"] = True
            meta_info["provenance_path"] = prov_path
            try:
                with open(prov_path, "r", encoding="utf-8") as f:
                    meta_info["provenance_data"] = json.load(f)
            except Exception:
                pass

        cff_path = os.path.join(self.project_path, "CITATION.cff")
        if os.path.exists(cff_path):
            meta_info["has_citation_cff"] = True
            meta_info["citation_cff_path"] = cff_path
            try:
                with open(cff_path, "r", encoding="utf-8") as f:
                    meta_info["citation_cff_content"] = f.read()
            except Exception:
                pass

        return meta_info
