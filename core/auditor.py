#!/usr/bin/env python3
"""
tool-citation-optima: 引用与技术溯源严密审计器 (Provenance Auditor)
100% Python 原生标准库，纯客观量规计算，绝对杜绝水军无底线高分打标
"""
import os
from typing import Dict, Any, List
from core.models import CitationAuditResult, AuditDimensionScore
from core.scanner import ProvenanceScanner

class ProvenanceAuditor:
    """对项目文档的技术溯源、对标矩阵、内联引用及机器元数据进行五维客观严密审计"""

    def __init__(self, project_path: str):
        self.project_path = os.path.abspath(project_path)
        self.scanner = ProvenanceScanner(self.project_path)

    def audit(self) -> CitationAuditResult:
        """执行全量审计并产出 CitationAuditResult"""
        scan_data = self.scanner.scan()
        metrics = scan_data["metrics"]

        # 检查是否为纯空壳/水军工程 (Anti-Rubber-Stamp)
        is_empty_shell = self._check_is_empty_shell()

        # 维度 1: 思想溯源与全球对标矩阵 (Heritage & Prior Art Matrix) - 20分
        d1 = self._eval_heritage_matrix(scan_data["heritage_tables"])

        # 维度 2: 内联引用与脚注佐证 (Inline Citations & Footnotes) - 20分
        d2 = self._eval_inline_citations(scan_data["inline_citations"])

        # 维度 3: 机器可读元数据 (Machine-Readable Provenance & CFF) - 20分
        d3 = self._eval_machine_metadata(scan_data["machine_meta"])

        # 维度 4: 架构推导依据与备选舍弃 (Rationale & Alternatives/Non-Goals) - 20分
        d4 = self._eval_rationale_and_alternatives(scan_data["nongoal_sections"], scan_data["heritage_tables"])

        # 维度 5: 引用链接真实性与抗造假防腐 (Link Integrity & Anti-Watermark) - 20分
        d5 = self._eval_link_integrity(scan_data["links"], is_empty_shell)

        total_score = d1.score + d2.score + d3.score + d4.score + d5.score

        # 水军/空壳工程惩罚截断: 纯空壳项目死锁上限 45 分 (F级)
        if is_empty_shell:
            total_score = min(total_score, 45)

        # 判定评级
        if total_score >= 90:
            rating = "S"
        elif total_score >= 80:
            rating = "A"
        elif total_score >= 70:
            rating = "B"
        elif total_score >= 60:
            rating = "C"
        else:
            rating = "F"

        # 不动点收敛判定: S 级且关键要素全齐
        fixed_point_ready = (
            total_score >= 90 and
            d1.score >= 18 and
            d3.score >= 16 and
            not is_empty_shell
        )

        # 收集改进建议
        suggestions = []
        for d in [d1, d2, d3, d4, d5]:
            suggestions.extend(d.remediation_tips)

        has_heritage_matrix = len(scan_data["heritage_tables"]) > 0
        has_inline_citations = len(scan_data["inline_citations"]) > 0
        has_machine_provenance = scan_data["machine_meta"]["has_provenance_json"]
        has_citation_cff = scan_data["machine_meta"]["has_citation_cff"]
        has_alternatives_and_nongoals = len(scan_data["nongoal_sections"]) > 0

        # 计算检测到的全球溯源条目总数
        detected_sources = sum(len(t.get("rows", [])) for t in scan_data["heritage_tables"])
        if scan_data["machine_meta"]["has_provenance_json"] and scan_data["machine_meta"]["provenance_data"]:
            prov_sources = scan_data["machine_meta"]["provenance_data"].get("grounded_sources", [])
            detected_sources = max(detected_sources, len(prov_sources))

        return CitationAuditResult(
            target_path=self.project_path,
            total_score=total_score,
            rating=rating,
            fixed_point_ready=fixed_point_ready,
            dimensions={
                "heritage_matrix": d1,
                "inline_citations": d2,
                "provenance_metadata": d3,
                "rationale_and_alternatives": d4,
                "link_integrity": d5
            },
            detected_sources_count=detected_sources,
            has_heritage_matrix=has_heritage_matrix,
            has_inline_citations=has_inline_citations,
            has_machine_provenance=has_machine_provenance,
            has_citation_cff=has_citation_cff,
            has_alternatives_and_nongoals=has_alternatives_and_nongoals,
            is_rubber_stamp_detected=is_empty_shell,
            suggestions=suggestions
        )

    def _eval_heritage_matrix(self, tables: List[Dict[str, Any]]) -> AuditDimensionScore:
        """评估对标矩阵维度 (满分 20)"""
        if not tables:
            return AuditDimensionScore(
                dimension="heritage_matrix",
                score=0,
                status="FAIL",
                details="文档中未发现全球技术思想溯源与对标矩阵 (Prior Art / Heritage Matrix)",
                evidence=[],
                remediation_tips=["在 README 或 SPEC 核心章节添加《全球优秀思路与对标矩阵》，列出对标源流、核心思想、吸收要点与取舍原因。"]
            )
        
        total_rows = sum(len(t.get("rows", [])) for t in tables)
        if total_rows >= 3:
            return AuditDimensionScore(
                dimension="heritage_matrix",
                score=20,
                status="PASS",
                details=f"已建立高质量全球技术溯源矩阵，共对标 {total_rows} 项权威开源/规范/学术源流",
                evidence=[f"{t['doc']}: {len(t['rows'])} 项对标" for t in tables],
                remediation_tips=[]
            )
        elif total_rows >= 1:
            return AuditDimensionScore(
                dimension="heritage_matrix",
                score=12,
                status="WARN",
                details=f"存在初步对标矩阵，但样本条目偏少 (当前仅 {total_rows} 项)",
                evidence=[f"{t['doc']}: {len(t['rows'])} 项对标" for t in tables],
                remediation_tips=["建议通过 tool-omniscout-radar 补充检索至少 3~5 项全球业界优秀对标项目。"]
            )
        else:
            return AuditDimensionScore(
                dimension="heritage_matrix",
                score=5,
                status="FAIL",
                details="对标矩阵表格仅有空表头，无实际对标内容",
                evidence=[],
                remediation_tips=["填写真实对标项目条目，避免空表格。"]
            )

    def _eval_inline_citations(self, citations: List[Dict[str, Any]]) -> AuditDimensionScore:
        """评估内联引用与脚注维度 (满分 20)"""
        count = len(citations)
        has_defs = any(c.get("type") == "FOOTNOTE_DEF" or c.get("type") == "REF_BLOCK_ITEMS" for c in citations)
        
        if count >= 3 and has_defs:
            return AuditDimensionScore(
                dimension="inline_citations",
                score=20,
                status="PASS",
                details=f"内联引用与脚注规范完备，检测到 {count} 处精准注记与定义",
                evidence=[f"{c['doc']} ({c['type']}: {c.get('key', c.get('count', ''))})" for c in citations[:4]],
                remediation_tips=[]
            )
        elif count >= 1:
            return AuditDimensionScore(
                dimension="inline_citations",
                score=12,
                status="WARN",
                details=f"检测到 {count} 处引用标注，但缺乏完整的脚注定义或学术规范",
                evidence=[f"{c['doc']} ({c['type']})" for c in citations[:3]],
                remediation_tips=["在文档末尾补充具体的 [^key]: 对应权威来源链接或论文出处。"]
            )
        else:
            return AuditDimensionScore(
                dimension="inline_citations",
                score=0,
                status="FAIL",
                details="文档中未发现任何内联引用脚注标记 (如 [^1], [@ref])",
                evidence=[],
                remediation_tips=["对关键架构决策使用 [^id] 进行内联锚点引注。"]
            )

    def _eval_machine_metadata(self, machine_meta: Dict[str, Any]) -> AuditDimensionScore:
        """评估机器可读元数据 (满分 20: .provenance.json 12分, CITATION.cff 8分)"""
        score = 0
        evidence = []
        tips = []

        if machine_meta["has_provenance_json"]:
            score += 12
            p_data = machine_meta["provenance_data"] or {}
            sources_len = len(p_data.get("grounded_sources", []))
            evidence.append(f".provenance.json (包含 {sources_len} 项机器可读权威源)")
        else:
            tips.append("运行 'python main.py init-cff' 或 'ground' 一键生成 .provenance.json 机器溯源账本。")

        if machine_meta["has_citation_cff"]:
            score += 8
            evidence.append("CITATION.cff (符合 GitHub 官方标准软件引用格式)")
        else:
            tips.append("在项目根目录提供 CITATION.cff，激活 GitHub 官方 'Cite this repository' 按钮。")

        status = "PASS" if score == 20 else ("WARN" if score > 0 else "FAIL")
        return AuditDimensionScore(
            dimension="provenance_metadata",
            score=score,
            status=status,
            details=f"机器可读元数据得分: {score}/20",
            evidence=evidence,
            remediation_tips=tips
        )

    def _eval_rationale_and_alternatives(self, nongoals: List[Dict[str, Any]], tables: List[Dict[str, Any]]) -> AuditDimensionScore:
        """评估架构推导依据与备选舍弃维度 (满分 20)"""
        has_explicit_nongoal = len(nongoals) > 0
        has_table_alternatives = False
        
        for t in tables:
            headers = [h.lower() for h in t.get("headers", [])]
            if any(k in " ".join(headers) for k in ["取舍", "区别", "备选", "alternative", "trade-off", "why not"]):
                has_table_alternatives = True
                break

        if has_explicit_nongoal and has_table_alternatives:
            return AuditDimensionScore(
                dimension="rationale_and_alternatives",
                score=20,
                status="PASS",
                details="决策依据充分：既有显式 Non-Goals / 边界声明，又在对标矩阵中详尽阐明备选方案与舍弃理由 (Trade-offs)",
                evidence=[f"Non-Goals: {nongoals[0]['title']}", "对标矩阵包含 Trade-off 列"],
                remediation_tips=[]
            )
        elif has_explicit_nongoal or has_table_alternatives:
            score = 12
            missing = "对标取舍原因" if not has_table_alternatives else "显式 Non-Goals 章节"
            return AuditDimensionScore(
                dimension="rationale_and_alternatives",
                score=score,
                status="WARN",
                details=f"决策依据部分完备，但缺少 {missing}",
                evidence=[n['title'] for n in nongoals] if has_explicit_nongoal else ["对标矩阵含取舍说明"],
                remediation_tips=[f"补充 {missing}，使方案推导脉络无懈可击。"]
            )
        else:
            return AuditDimensionScore(
                dimension="rationale_and_alternatives",
                score=0,
                status="FAIL",
                details="缺少决策动机推导：既无 Non-Goals 说明，也无为什么不选备选方案的对比阐述",
                evidence=[],
                remediation_tips=["明确列出 Non-Goals (坚决不做的事) 和 Alternatives Considered (备选方案为何被否决)。"]
            )

    def _eval_link_integrity(self, links: List[Dict[str, Any]], is_empty_shell: bool) -> AuditDimensionScore:
        """评估链接真实性与抗造假防腐维度 (满分 20)"""
        if is_empty_shell:
            return AuditDimensionScore(
                dimension="link_integrity",
                score=0,
                status="FAIL",
                details="[Anti-Rubber-Stamp] 检测到工程为纯文档空壳/无实体代码，触犯反形式主义红线",
                evidence=["工程缺少实际可执行代码或可运行实体"],
                remediation_tips=["编写真实业务代码并保证单元测试通过，坚决杜绝只有文档没有实体的形式主义空壳。"]
            )

        valid_links = [l for l in links if not l["is_placeholder"] and not l["is_badge"]]
        placeholders = [l for l in links if l["is_placeholder"]]

        if placeholders:
            return AuditDimensionScore(
                dimension="link_integrity",
                score=5,
                status="FAIL",
                details=f"检测到 {len(placeholders)} 处伪造/占位符链接 (如 example.com / placeholder)",
                evidence=[f"{p['anchor']}: {p['url']}" for p in placeholders[:3]],
                remediation_tips=["清除占位符虚假链接，替换为真实权威的 GitHub 仓库或论文链接。"]
            )

        if len(valid_links) >= 3:
            return AuditDimensionScore(
                dimension="link_integrity",
                score=20,
                status="PASS",
                details=f"链接真实度高，检测到 {len(valid_links)} 个真实权威外链 (涵盖 GitHub/RFC/官方规范)",
                evidence=[f"{l['anchor']} -> {l['url'][:45]}..." for l in valid_links[:3]],
                remediation_tips=[]
            )
        elif len(valid_links) >= 1:
            return AuditDimensionScore(
                dimension="link_integrity",
                score=12,
                status="WARN",
                details=f"检测到 {len(valid_links)} 个有效外链，数量略显单一",
                evidence=[f"{l['anchor']} -> {l['url']}" for l in valid_links],
                remediation_tips=["建议增加引用的权威外链数 (如开源主页或官方规范文档)。"]
            )
        else:
            return AuditDimensionScore(
                dimension="link_integrity",
                score=0,
                status="FAIL",
                details="文档中未包含任何有效的外部技术权威链接",
                evidence=[],
                remediation_tips=["为对标的技术方案附带其真实有效的官方仓库或规范链接。"]
            )

    def _check_is_empty_shell(self) -> bool:
        """检查项目是否为无实质代码的纯八股空壳工程"""
        code_exts = (".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".c", ".sh", ".ps1")
        total_code_lines = 0
        code_files_count = 0

        for root, dirs, files in os.walk(self.project_path):
            dirs[:] = [d for d in dirs if d not in (".git", ".cache", "__pycache__", "node_modules", ".venv", "venv")]
            for f in files:
                if any(f.endswith(ext) for ext in code_exts):
                    # 排除简单的模版文件
                    fpath = os.path.join(root, f)
                    try:
                        with open(fpath, "r", encoding="utf-8", errors="replace") as cf:
                            lines = [l.strip() for l in cf.readlines() if l.strip() and not l.strip().startswith(("#", "//", "/*", "*"))]
                            total_code_lines += len(lines)
                            code_files_count += 1
                    except Exception:
                        pass

        # 若有效代码行小于 15 行，视为纯八股空壳
        return code_files_count == 0 or total_code_lines < 15
