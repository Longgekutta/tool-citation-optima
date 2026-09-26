#!/usr/bin/env python3
"""
tool-citation-optima: 全知雷达桥接模块 (OmniScout-Radar Bridge)
100% Python 原生标准库，联动 tool-omniscout-radar 进行极限检索并提纯权威溯源输入
"""
import os
import sys
import json
import subprocess
from typing import List, Dict, Any, Optional
from core.models import HeritageSource

class RadarBridge:
    """与 D:\\gitee\\tool-omniscout-radar 深度联动的桥接器"""

    # 优先检测环境配置、D:\github 同级目录或当前上级目录
    _peer_radar = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "tool-omniscout-radar"))
    DEFAULT_RADAR_PATH = os.environ.get("RADAR_PATH") or (_peer_radar if os.path.isdir(_peer_radar) else r"D:\github\tool-omniscout-radar")

    def __init__(self, radar_path: Optional[str] = None):
        self.radar_path = os.path.abspath(radar_path or self.DEFAULT_RADAR_PATH)
        self.audits_dir = os.path.join(self.radar_path, "audits")

    def is_available(self) -> bool:
        """检查 omniscout-radar 是否物理就绪"""
        return os.path.isdir(self.radar_path) and os.path.isfile(os.path.join(self.radar_path, "main.py"))

    def list_existing_reports(self) -> List[str]:
        """列出雷达已产出的所有审计档案"""
        if not os.path.isdir(self.audits_dir):
            return []
        reports = []
        for f in os.listdir(self.audits_dir):
            if f.endswith(".json") and f.startswith("autonomous_"):
                reports.append(os.path.join(self.audits_dir, f))
        return sorted(reports)

    def load_report(self, report_path: str) -> Dict[str, Any]:
        """加载并解析指定的雷达审计报告"""
        with open(report_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def trigger_radar(self, topic: str, deep: bool = False, timeout: int = 30) -> Dict[str, Any]:
        """调用 tool-omniscout-radar 执行全自主 4 阶段极限技术侦察"""
        if not self.is_available():
            raise FileNotFoundError(f"未找到 tool-omniscout-radar: {self.radar_path}")

        main_py = os.path.join(self.radar_path, "main.py")
        cmd = [sys.executable, main_py, "radar", topic]
        if deep:
            cmd.append("--deep")

        # 跨平台执行雷达检索
        env = dict(os.environ)
        env["PYTHONUTF8"] = "1"
        env["PYTHONIOENCODING"] = "utf-8"

        proc = subprocess.run(
            cmd,
            cwd=self.radar_path,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env
        )

        if proc.returncode != 0 and not proc.stdout:
            raise RuntimeError(f"OmniScout-Radar 运行失败: {proc.stderr}")

        # 尝试定位最新生成的审计报告
        latest_report = self._find_latest_report_for_topic(topic)
        if latest_report:
            return self.load_report(latest_report)

        # 兜底返回结构化摘要
        return {
            "meta": {"domain_topic": topic},
            "reports": [],
            "raw_output": proc.stdout
        }

    def extract_heritage_sources(self, radar_data: Dict[str, Any], max_items: int = 5, skeleton_mode: bool = False) -> List[HeritageSource]:
        """将雷达审计数据清洗提纯为标准化的技术思想溯源与对标源列表"""
        sources = []
        candidates = radar_data.get("reports", [])
        
        def _safe_num(val, default=0):
            if isinstance(val, (int, float)):
                return float(val)
            if isinstance(val, str):
                cleaned = val.replace(",", "").replace("+", "").strip().lower()
                if cleaned.endswith("k"):
                    try: return float(cleaned[:-1]) * 1000.0
                    except Exception: return float(default)
                if cleaned.endswith("m"):
                    try: return float(cleaned[:-1]) * 1000000.0
                    except Exception: return float(default)
                try: return float(cleaned)
                except Exception: return float(default)
            return float(default)

        # 优先选取 ADOPT 与 高星候选
        sorted_candidates = sorted(
            candidates,
            key=lambda x: (
                1 if "ADOPT" in str(x.get("recommendation", "")) else 0,
                _safe_num(x.get("score", 0)),
                _safe_num(x.get("stars", 0))
            ),
            reverse=True
        )

        for item in sorted_candidates[:max_items]:
            repo_name = item.get("repo_name", "Unknown/Repo")
            url = item.get("url", f"https://github.com/{repo_name}")
            stars = item.get("stars", 0)
            desc = item.get("description", "").strip() or "全球工业界高星参考实现"
            
            # 提炼核心思想与事实
            core_insight = f"{desc} (工业界验证度: ⭐ {stars})"
            if skeleton_mode:
                adopted = f"<!-- AI_DECISION_ADOPT: 阐明本项目针对 [{repo_name}] 吸收借鉴的核心机理与创新算子 -->"
                tradeoff = f"<!-- AI_DECISION_TRADEOFF: 阐述为何不直接全盘引入 [{repo_name}] 的取舍与差异 (Non-Goals) -->"
            else:
                adopted = f"吸收其架构解耦经验与针对该领域的针对性验证量规 (得分: {item.get('score', 80)})"
                tradeoff = "坚决拒绝第三方重型依赖，完全以 Python 原生标准库重构，追求 <15ms 启动与不动点自洽"

            sources.append(HeritageSource(
                name=repo_name,
                category="OPEN_SOURCE",
                url=url,
                core_insight=core_insight,
                adopted_aspects=adopted,
                rejection_reason_or_tradeoff=tradeoff,
                stars_or_citations=stars
            ))

        return sources

    def prune_audit_cache(self, keep_latest: int = 20) -> int:
        """修剪雷达审计目录，防止审计日志与历史文档爆炸 (保留最近 keep_latest 份)"""
        reports = self.list_existing_reports()
        if len(reports) <= keep_latest:
            return 0
        reports.sort(key=lambda p: os.path.getmtime(p))
        to_delete = reports[:-keep_latest]
        deleted = 0
        for p in to_delete:
            try:
                os.remove(p)
                deleted += 1
            except Exception:
                pass
        return deleted

    def _find_latest_report_for_topic(self, topic: str) -> Optional[str]:
        """根据主题查找最新的报告文件"""
        reports = self.list_existing_reports()
        if not reports:
            return None
        # 简单根据修改时间降序排序
        reports.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return reports[0]

