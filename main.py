#!/usr/bin/env python3
"""
tool-citation-optima: 全域文档引用、技术溯源与决策依据极限优化引擎
Universal CLI & 5 Universal Verbs Implementation
100% Python 原生标准库，零外部依赖，毫秒级响应
"""
import sys
import os
import json
import argparse
import time

# 确保能载入同级 core 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.models import HeritageSource
from core.scanner import ProvenanceScanner
from core.auditor import ProvenanceAuditor
from core.radar_bridge import RadarBridge
from core.generator import ProvenanceGenerator
from core.organic_injector import OrganicInjector

def cmd_setup(args=None) -> int:
    """标准动词: setup (环境验证与自检)"""
    print("🔧 [SETUP] 正在检查 Python 运行环境与依赖...")
    if sys.version_info < (3, 10):
        print(f"❌ Python 版本过低: {sys.version}, 需要 3.10+")
        return 1

    radar = RadarBridge()
    radar_status = "✅ 可用" if radar.is_available() else "⚠️ 未找到 (建议配置 D:\\github\\tool-omniscout-radar)"
    print(f"  - Python 版本: {sys.version.split()[0]} (100% 标准库，零第三方 pip 依赖)")
    print(f"  - OmniScout-Radar 状态: {radar_status}")
    print("✅ [SETUP] tool-citation-optima 环境就绪。")
    return 0

def cmd_health(args=None) -> int:
    """标准动词: health (秒级探活与自检诊断)"""
    t0 = time.perf_counter()
    project_root = os.path.dirname(os.path.abspath(__file__))
    auditor = ProvenanceAuditor(project_root)
    res = auditor.audit()
    latency_ms = (time.perf_counter() - t0) * 1000

    status_str = "OK" if res.total_score >= 80 else "WARN"
    out = {
        "status": status_str,
        "component": "tool-citation-optima",
        "score": res.total_score,
        "rating": res.rating,
        "fixed_point_ready": res.fixed_point_ready,
        "latency_ms": round(latency_ms, 2)
    }

    if args and getattr(args, "json", False):
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"STATUS: {status_str} | Component: tool-citation-optima | 得分: {res.total_score}/100 ({res.rating}) | 耗时: {latency_ms:.1f}ms")
    return 0 if status_str == "OK" else 1

def cmd_clean(args=None) -> int:
    """标准动词: clean (清理缓存与临时产物)"""
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cleaned = 0
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            if d in ("__pycache__", ".cache", ".pytest_cache"):
                dp = os.path.join(root, d)
                try:
                    import shutil
                    shutil.rmtree(dp)
                    cleaned += 1
                except Exception:
                    pass
    print(f"🧹 [CLEAN] 已清理 {cleaned} 个缓存目录。")
    return 0

def cmd_test(args=None) -> int:
    """标准动词: test (运行内部自洽单元测试)"""
    import unittest
    tests_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tests")
    loader = unittest.TestLoader()
    suite = loader.discover(tests_dir)
    runner = unittest.TextTestRunner(verbosity=2)
    res = runner.run(suite)
    return 0 if res.wasSuccessful() else 1

def cmd_audit(args) -> int:
    """子命令: audit (全面审计目标项目的引用与技术溯源完备度)"""
    target = os.path.abspath(args.path)
    auditor = ProvenanceAuditor(target)
    res = auditor.audit()

    if getattr(args, "json", False):
        print(json.dumps(res.to_dict(), ensure_ascii=False, indent=2))
        return 0

    print(f"\n========================================================")
    print(f"📊 [PROVENANCE AUDIT] 技术思想溯源与引用审计报告: {os.path.basename(target)}")
    print(f"========================================================")
    print(f"目标物理路径: {target}")
    print(f"总得分: {res.total_score} / 100 分  |  评级: {res.rating} ({res.to_dict()['rating_description']})")
    print(f"不动点收敛状态: {'✅ 是 (Fixed-Point Master)' if res.fixed_point_ready else '❌ 否 (未达收敛标杆)'}")
    print(f"检测到的全球溯源条目: {res.detected_sources_count} 项")
    print(f"水军空壳惩罚截断: {'⚠️ 触发 (纯文档无实体代码)' if res.is_rubber_stamp_detected else '✅ 未触发 (代码实体真实)'}")

    print("\n[五维量规拆解]:")
    for k, d in res.dimensions.items():
        status_icon = "🟢" if d.status == "PASS" else ("🟡" if d.status == "WARN" else "🔴")
        print(f"  {status_icon} [{d.dimension}] {d.score:2d}/{d.max_score}分 - {d.details}")
        if d.evidence:
            for ev in d.evidence:
                print(f"      + 佐证: {ev}")

    if res.suggestions:
        print("\n[精准整改建议]:")
        for idx, sug in enumerate(res.suggestions, 1):
            print(f"  {idx}. {sug}")

    print(f"========================================================\n")
    return 0 if res.total_score >= 80 else 1

def cmd_ground(args) -> int:
    """子命令: ground (联动 omniscout-radar 极限搜索并有机融合注水)"""
    target = os.path.abspath(args.path)
    topic = args.topic
    print(f"🎯 [GROUND] 正在为项目 [{os.path.basename(target)}] 启动全知雷达搜索与思想溯源...")
    print(f"  - 侦察主题: '{topic}'")

    radar = RadarBridge()
    if not radar.is_available():
        print(f"❌ 错误: 未能在本地找到 tool-omniscout-radar: {radar.radar_path}")
        return 1

    print("🚀 正在调度 tool-omniscout-radar 进行四阶段并发探针与动态量规审计...")
    radar_data = radar.trigger_radar(topic, deep=getattr(args, "deep", False))
    sources = radar.extract_heritage_sources(radar_data, max_items=args.limit)

    if not sources:
        print("⚠️ 雷达检索未发现高匹配候选项目，使用规范兜底源流。")
        sources = [
            HeritageSource(
                name="Spotify Golden Path / CNCF Backstage",
                category="INDUSTRY_STANDARD",
                url="https://backstage.io",
                core_insight="Paved Road, not a toll road (修筑柏油路，而非设卡收费)",
                adopted_aspects="开箱即用无摩擦标准模具与渐进式演进",
                rejection_reason_or_tradeoff="去除 Backstage 复杂 Node.js 框架，完全以纯标准库轻量实现"
            )
        ]

    print(f"✅ 成功从雷达提取 {len(sources)} 项全球权威对标源流。")
    injector = OrganicInjector(target)
    res = injector.inject_project(topic=topic, sources=sources, target_doc=args.doc)

    print(f"\n✨ [ORGANIC INJECTION 完成]:")
    print(f"  - 修改文件: {res['modified_files']}")
    print(f"  - 创建文件: {res['created_files']}")
    print(f"  - 不动点状态: {'✅ 已处于不动点' if res['fixed_point'] else '⚡ 已更新至新不动点'}")

    # 即刻进行出厂审计检验
    auditor = ProvenanceAuditor(target)
    audit_res = auditor.audit()
    print(f"\n[入轨后复检得分]: {audit_res.total_score} / 100 分 ({audit_res.rating}) | 不动点达成: {'✅' if audit_res.fixed_point_ready else '❌'}")
    return 0

def cmd_inject(args) -> int:
    """子命令: inject (从现有的 radar json 报告直接注水)"""
    target = os.path.abspath(args.path)
    report_path = os.path.abspath(args.report)
    if not os.path.isfile(report_path):
        print(f"❌ 报告文件不存在: {report_path}")
        return 1

    radar = RadarBridge()
    radar_data = radar.load_report(report_path)
    topic = radar_data.get("meta", {}).get("domain_topic", "通用系统架构")
    sources = radar.extract_heritage_sources(radar_data, max_items=args.limit)

    injector = OrganicInjector(target)
    res = injector.inject_project(topic=topic, sources=sources, target_doc=args.doc)
    print(f"✨ [INJECT 完成] 修改: {res['modified_files']}, 新建: {res['created_files']}")
    return 0

def cmd_init_cff(args) -> int:
    """子命令: init-cff (初始化 CITATION.cff 与 .provenance.json)"""
    target = os.path.abspath(args.path)
    name = os.path.basename(target)
    abstract = args.abstract or f"{name}: First-principles verified component."
    
    # 扫描是否有现成对标表
    scanner = ProvenanceScanner(target)
    scan_data = scanner.scan()
    
    sources = []
    for t in scan_data["heritage_tables"]:
        for row in t.get("rows", []):
            if len(row) >= 4:
                sources.append(HeritageSource(
                    name=row[0].strip("[]*`"),
                    category="OPEN_SOURCE",
                    url=f"https://github.com",
                    core_insight=row[2] if len(row) > 2 else "参考源流",
                    adopted_aspects=row[3] if len(row) > 3 else "借鉴吸收",
                    rejection_reason_or_tradeoff=row[4] if len(row) > 4 else "独立自洽"
                ))

    injector = OrganicInjector(target)
    res = injector.inject_project(topic=name, sources=sources, abstract=abstract)
    print(f"✨ [INIT-CFF 完成] 项目 [{name}] 机器元数据已初始化: {res['created_files'] + res['modified_files']}")
    return 0

def cmd_fixed_point(args) -> int:
    """子命令: fixed-point (严格数学级不动点验证)"""
    target = os.path.abspath(args.path)
    print(f"🔬 [FIXED-POINT] 正在对 [{os.path.basename(target)}] 执行不动点收敛性验真...")

    auditor = ProvenanceAuditor(target)
    r1 = auditor.audit()
    print(f"  - 初始审计状态: 得分 {r1.total_score}/100, 评级 {r1.rating}")

    # 尝试再次运行注入器
    injector = OrganicInjector(target)
    # 读取已有的 .provenance.json
    prov_file = os.path.join(target, ".provenance.json")
    if os.path.exists(prov_file):
        with open(prov_file, "r", encoding="utf-8") as f:
            prov_data = json.load(f)
        sources = [
            HeritageSource(
                name=s["name"],
                category=s.get("category", "OPEN_SOURCE"),
                url=s["url"],
                core_insight=s["core_insight"],
                adopted_aspects=s["adopted_aspects"],
                rejection_reason_or_tradeoff=s.get("tradeoff", "独立自洽")
            )
            for s in prov_data.get("grounded_sources", [])
        ]
        res = injector.inject_project(
            topic=prov_data.get("search_topic", "通用系统"),
            sources=sources
        )
        print(f"  - 二次注入增量: 修改 {res['modified_files']}, 新建 {res['created_files']}")
        is_converged = res["fixed_point"] and (len(res["modified_files"]) == 0)
    else:
        is_converged = r1.fixed_point_ready

    r2 = auditor.audit()
    print(f"  - 二次审计状态: 得分 {r2.total_score}/100, 评级 {r2.rating}")

    if r2.total_score == r1.total_score and is_converged and r2.total_score >= 90:
        print("🎉 [不动点验真成功] 系统状态完全收敛 f(x) = x，无状态漂移与扰动！")
        return 0
    else:
        print(f"⚠️ 未达成严格不动点收敛: r1={r1.total_score}, r2={r2.total_score}, converged={is_converged}")
        return 1

def cmd_self_test(args=None) -> int:
    """子命令: self-test (自身的自洽闭环自检)"""
    this_dir = os.path.dirname(os.path.abspath(__file__))
    print("🧪 [SELF-TEST] tool-citation-optima 正在执行自我审视...")
    auditor = ProvenanceAuditor(this_dir)
    res = auditor.audit()
    print(f"  - 自身溯源完备度得分: {res.total_score} / 100 ({res.rating})")
    for k, d in res.dimensions.items():
        print(f"    * {d.dimension}: {d.score}/{d.max_score} - {d.status}")
    return 0 if res.total_score >= 80 else 1

def main():
    parser = argparse.ArgumentParser(
        description="tool-citation-optima: 全域文档引用、技术溯源与决策依据极限优化引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="subcommand", help="子命令")

    # 1. audit
    p_audit = subparsers.add_parser("audit", help="全面审计目标工程的引用与技术溯源完备度")
    p_audit.add_argument("path", nargs="?", default=".", help="目标工程物理路径")
    p_audit.add_argument("--json", action="store_true", help="以 JSON 格式输出审计报告")

    # 2. ground
    p_ground = subparsers.add_parser("ground", help="联动 omniscout-radar 极限搜索并有机融合注水")
    p_ground.add_argument("path", help="目标工程物理路径")
    p_ground.add_argument("--topic", required=True, help="检索与溯源的领域主题关键词")
    p_ground.add_argument("--limit", type=int, default=4, help="注入的最优权威源数量")
    p_ground.add_argument("--doc", default=None, help="指定注入的主文档 (默认探查 README.md)")
    p_ground.add_argument("--deep", action="store_true", help="启用深度探针模式")

    # 3. inject
    p_inject = subparsers.add_parser("inject", help="从现有的 radar json 报告直接注水")
    p_inject.add_argument("path", help="目标工程物理路径")
    p_inject.add_argument("--report", required=True, help="已有的 radar 审计报告 JSON 路径")
    p_inject.add_argument("--limit", type=int, default=4, help="注入的最优权威源数量")
    p_inject.add_argument("--doc", default=None, help="指定注入的主文档")

    # 4. init-cff
    p_cff = subparsers.add_parser("init-cff", help="初始化 CITATION.cff 与 .provenance.json")
    p_cff.add_argument("path", nargs="?", default=".", help="目标工程物理路径")
    p_cff.add_argument("--abstract", default=None, help="项目摘要描述")

    # 5. fixed-point
    p_fp = subparsers.add_parser("fixed-point", help="数学级不动点验证")
    p_fp.add_argument("path", nargs="?", default=".", help="目标工程物理路径")

    # 6. self-test
    subparsers.add_parser("self-test", help="自身不动点与健康度闭环自检")

    # 7. 5 大通用动词
    subparsers.add_parser("setup", help="环境就绪检查")
    subparsers.add_parser("run", help="主线执行 (默认对当前仓库执行审计)")
    subparsers.add_parser("test", help="自洽单元测试")
    subparsers.add_parser("health", help="秒级探活诊断")
    subparsers.add_parser("clean", help="垃圾与缓存自理")

    # 若无参数传入，默认打印帮助
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # 快捷支持标准五大动词直接作为首个参数
    first_arg = sys.argv[1]
    if first_arg == "setup":
        sys.exit(cmd_setup())
    elif first_arg == "test":
        sys.exit(cmd_test())
    elif first_arg == "health":
        p = argparse.ArgumentParser()
        p.add_argument("--json", action="store_true")
        args, _ = p.parse_known_args(sys.argv[2:])
        sys.exit(cmd_health(args))
    elif first_arg == "clean":
        sys.exit(cmd_clean())
    elif first_arg == "run":
        target = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("-") else "."
        p = argparse.ArgumentParser()
        p.add_argument("--json", action="store_true")
        p.add_argument("path", nargs="?", default=target)
        args, _ = p.parse_known_args(sys.argv[2:])
        args.path = target
        sys.exit(cmd_audit(args))

    parsed_args = parser.parse_args()

    if parsed_args.subcommand == "audit":
        sys.exit(cmd_audit(parsed_args))
    elif parsed_args.subcommand == "ground":
        sys.exit(cmd_ground(parsed_args))
    elif parsed_args.subcommand == "inject":
        sys.exit(cmd_inject(parsed_args))
    elif parsed_args.subcommand == "init-cff":
        sys.exit(cmd_init_cff(parsed_args))
    elif parsed_args.subcommand == "fixed-point":
        sys.exit(cmd_fixed_point(parsed_args))
    elif parsed_args.subcommand == "self-test":
        sys.exit(cmd_self_test(parsed_args))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
