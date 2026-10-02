# tool-citation-optima: 全域文档引用、技术溯源与决策依据极限优化引擎

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://python.org)
[![Zero-Pip: 100% Standard Library](https://img.shields.io/badge/Zero--Pip-100%25%20StdLib-blue.svg)](#)
[![Anti-Bureaucracy: 100% Guaranteed](https://img.shields.io/badge/Anti--Bureaucracy-100%25%20Zero--Empty--Shells-orange.svg)](#)
[![Philosophy: Verified Provenance](https://img.shields.io/badge/Philosophy-Verified%20Provenance-purple.svg)](#)
[![Tests: 100% Passing](https://img.shields.io/badge/Tests-100%25%20Passing-brightgreen.svg)](#)
[![Fixed-Point: Converged](https://img.shields.io/badge/Fixed--Point-f(x)%3Dx-success.svg)](#)

> **核心宗旨**：**让每一个项目的技术决策不再是空中楼阁，让每一次极限搜索的思想精髓都有迹可循、有机融合、真实可信。**  
> 在过去的工程演进中，我们经常在讨论中通过搜索引擎项目碰撞出大量优秀架构灵感，但落到最终文档时往往变成了“只有结论、没有来龙去脉、缺少引用依据”的无根之木。  
> `tool-citation-optima` 彻底打破这一断层：它以第一性原理连接 `tool-omniscout-radar` 极限搜索输出，自动提取全球工业界与学术界的优秀思想，并通过**非破坏性有机融合算法**将技术思想溯源对标矩阵、规范内联脚注、机器可读账本 (`.provenance.json`) 与标准学术引用 (`CITATION.cff`) 植入任何异构文档中。

---

## 🏛️ 技术思想溯源与全球对标矩阵 (World-Class Heritage & Prior Art)

本项目秉承第一性原理与零幻觉工程原则，严格站在全球工业标杆与学术先验的肩膀上演进构建。

完整权威源流矩阵（收录 6 项世界级标杆与规范）、深度机制对标、吸收借鉴点与取舍论证详见独立档案：
👉 **[完整先验对标与权威引用档案 (REFERENCES.md)](REFERENCES.md)**

*(注：机器可读元数据与规范引用已同步至 `.provenance.json` 与 `CITATION.cff`)*

---


## 🚫 Non-Goals (坚决不做的事)

为了防止项目定位漂移和膨胀为大泥球，本项目划定以下坚决不做的边界：
1. **坚决不自建重型爬虫系统**：网络搜索与全网爬取由 `tool-omniscout-radar` 全权负责，本项目专精于溯源清洗、审计、打标与文档有机注入；
2. **坚决不引入任何第三方 pip 依赖**：全流程必须依靠纯 Python 标准库（`urllib`, `argparse`, `unittest`, `json`, `re`），启动延时保证亚 15ms；
3. **坚决不破坏用户的既有文档结构**：采用“非破坏性渐进式植入”算法，如果原文档已有结构，必须智能寻找最自然的插入锚点，且必须满足不动点收敛 $f(x)=x$；
4. **坚决杜绝水军无底线打标**：对无实体代码的纯文档空壳工程直接激活反形式主义截断，评分死锁在 45 分以下（F 级不可用）。

---

## 🚀 快速开始与五大通用动词

```powershell
# 1. 环境验证与依赖检查 (setup)
python main.py setup

# 2. 极速探活与自检诊断 (health)
python main.py health

# 3. 运行全量单元测试 (test)
python main.py test

# 4. 自身不动点与合规自检 (self-test)
python main.py self-test

# 5. 垃圾与缓存自理 (clean)
python main.py clean
```

---

## ⚙️ 核心功能与使用操典

### 1. 对任意项目执行引用与溯源严密审计 (`audit`)
对标五大客观量规维度（各 20 分，满分 100 分），杜绝虚假高分：
```powershell
# 审计当前项目或指定目录
python main.py audit D:\gitee\any-project

# 输出结构化 JSON 报告 (供 CI 门禁或流水线消费)
python main.py audit D:\gitee\any-project --json
```

**五维审计量规体系**：
* 🟢 **D1. 思想溯源与全球对标矩阵 (20分)**：是否具有包含“权威源流、源流分类、核心思想、借鉴要点、取舍区别”的标准表格；
* 🟢 **D2. 内联引用与脚注佐证 (20分)**：关键架构论断是否带有 `[^id]` 等精准内联注记与定义；
* 🟢 **D3. 机器可读元数据 (20分)**：是否配置了 `.provenance.json` (12分) 与 `CITATION.cff` (8分)；
* 🟢 **D4. 架构推导依据与备选舍弃 (20分)**：是否明确定义了 Non-Goals 并详细说明了为何不直接采纳备选方案；
* 🟢 **D5. 链接真实性与抗空壳防腐 (20分)**：外链是否权威真实（无 example.com 占位符），且仓库非无代码空壳。

### 2. 联动 `tool-omniscout-radar` 极限搜索并有机融合注水 (`ground`)
一键完成“极限搜索 $\rightarrow$ 提纯对标条目 $\rightarrow$ 非破坏性注入文档 $\rightarrow$ 生成机器账本与 CFF”全流程：
```powershell
python main.py ground D:\gitee\my-new-tool --topic "分布式KV缓存一致性与高并发"
```

### 3. 从已有的雷达审计报告直接注水 (`inject`)
```powershell
python main.py inject D:\gitee\my-new-tool --report D:\gitee\tool-omniscout-radar\audits\autonomous_citation_report.json
```

### 4. 严格数学级不动点验证 (`fixed-point`)
验证系统状态在反复执行后是否严格满足 $f(x) = x$，杜绝状态漂移：
```powershell
python main.py fixed-point D:\gitee\my-new-tool
```

---

## 🧱 核心架构设计

```text
tool-citation-optima/
├── core/
│   ├── models.py           # 强类型数据模型 (HeritageSource, ProvenanceManifest, CitationAuditResult)
│   ├── scanner.py          # 纯标准库 AST/正则轻量解析器 (提取对标表格、脚注、链接、Non-Goals)
│   ├── auditor.py          # 五维客观严密审计器 (含反形式主义水军空壳惩罚截断)
│   ├── radar_bridge.py     # tool-omniscout-radar 原生桥接器 (加载报告/触发四阶段极限检索)
│   ├── organic_injector.py # 非破坏性自适应有机注入器 (智能寻找自然锚点，保证不动点收敛)
│   └── generator.py        # 标准化产物生成器 (CITATION.cff, .provenance.json, 对标矩阵, 脚注)
├── specs/
│   └── SPEC_CITATION_PROVENANCE.md # 全域文档引用与技术溯源刚性规范契约
├── tests/                  # 100% 通过的自洽自动化测试矩阵
├── main.py                 # 统一 CLI 接口与五大通用动词暴露
├── justfile / run.ps1      # 跨平台动词代理脚本
├── CITATION.cff            # 符合 GitHub 官方标准的学术引用文件
└── .provenance.json        # 机器可读的谱系追踪账本
```

---

## 📜 许可证与维护者

- **许可协议**：MIT License
- **维护者**：Antigravity Fleet Core Team
- **承诺**：永远保持纯原生标准库实现，永远保持亚 15ms 极速响应，永远拒绝形式主义空壳。
