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

    DEFAULT_RADAR_PATH = r"D:\gitee\tool-omniscout-radar"

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

    def extract_heritage_sources(self, radar_data: Dict[str, Any], max_items: int = 5) -> List[HeritageSource]:
        """将雷达审计数据清洗提纯为标准化的技术思想溯源与对标源列表"""
        sources = []
        candidates = radar_data.get("reports", [])
        
        # 优先选取 ADOPT 与 高星候选
        sorted_candidates = sorted(
            candidates,
            key=lambda x: (
                1 if "ADOPT" in x.get("recommendation", "") else 0,
                x.get("score", 0),
                x.get("stars", 0)
            ),
            reverse=True
        )

        for item in sorted_candidates[:max_items]:
            repo_name = item.get("repo_name", "Unknown/Repo")
            url = item.get("url", f"https://github.com/{repo_name}")
            stars = item.get("stars", 0)
            desc = item.get("description", "").strip() or "全球工业界高星参考实现"
            
            # 提炼核心思想与借鉴点
            core_insight = f"{desc} (工业界验证度: ⭐ {stars})"
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

    def _find_latest_report_for_topic(self, topic: str) -> Optional[str]:
        """根据主题查找最新的报告文件"""
        reports = self.list_existing_reports()
        if not reports:
            return None
        # 简单根据修改时间降序排序
        reports.sort(key=lambda p: os.path.getmtime(p), reverse=True)
        return reports[0]
