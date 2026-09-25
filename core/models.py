#!/usr/bin/env python3
"""
tool-citation-optima: 核心数据模型 (Data Models)
100% Python 原生标准库，零外部依赖 (Zero-Pip)
"""
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
import json

@dataclass
class HeritageSource:
    """单个技术思想溯源与对标源条目"""
    name: str                           # 项目/论文/规范名称，如 "MADR (Markdown Architectural Decision Records)"
    category: str                       # 源流类别: SPEC_RFC | OPEN_SOURCE | ACADEMIC_PAPER | INDUSTRY_STANDARD
    url: str                            # 权威链接 (GitHub/RFC/DOI/Paper)
    core_insight: str                   # 核心思想/首创机制
    adopted_aspects: str                # 本项目吸收/借鉴的具体要点
    rejection_reason_or_tradeoff: str   # 为什么不直接照搬 / 本项目的超越与取舍 (Trade-offs)
    stars_or_citations: Optional[int] = None
    author: Optional[str] = None
    version: Optional[str] = None

@dataclass
class ProvenanceManifest:
    """项目技术溯源机器可读元数据 (.provenance.json)"""
    project_name: str
    version: str
    last_updated: str
    search_topic: str
    radar_query_vectors: List[str] = field(default_factory=list)
    grounded_sources: List[Dict[str, Any]] = field(default_factory=list)
    architectural_invariants: List[str] = field(default_factory=list)
    alternatives_considered: List[Dict[str, str]] = field(default_factory=list)
    non_goals: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)

@dataclass
class AuditDimensionScore:
    """单个审计维度得分与明细"""
    dimension: str
    score: int          # 满分 20 分
    max_score: int = 20
    status: str = "PASS"  # PASS | WARN | FAIL
    details: str = ""
    evidence: List[str] = field(default_factory=list)
    remediation_tips: List[str] = field(default_factory=list)

@dataclass
class CitationAuditResult:
    """全量引用与技术溯源审计报告"""
    target_path: str
    total_score: int    # 满分 100 分
    rating: str         # S (90-100) | A (80-89) | B (70-79) | C (60-69) | F (<60)
    fixed_point_ready: bool
    dimensions: Dict[str, AuditDimensionScore] = field(default_factory=dict)
    detected_sources_count: int = 0
    has_heritage_matrix: bool = False
    has_inline_citations: bool = False
    has_machine_provenance: bool = False
    has_citation_cff: bool = False
    has_alternatives_and_nongoals: bool = False
    is_rubber_stamp_detected: bool = False
    suggestions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        res = asdict(self)
        res["rating_description"] = {
            "S": "登峰造极 (Fixed-Point Master / Fully Grounded)",
            "A": "卓越规范 (Well Documented & Provenanced)",
            "B": "基本合格 (Partial Provenance)",
            "C": "欠缺依据 (Weak Citations)",
            "F": "空中楼阁 (Unprovenanced / Empty Shell)"
        }.get(self.rating, "Unknown")
        return res
