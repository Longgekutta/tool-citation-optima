# REFERENCES: 技术思想溯源与全球对标档案 (World-Class Heritage & Prior Art)

> 本文档为 `tool-citation-optima` 技术思想渊源、全球权威工程对标与取舍决策的完整归档。

---

## 🏛️ 技术思想溯源与全球对标矩阵 (World-Class Heritage & Prior Art)

> **第一性原理背景**：本项目在架构推导之初，通过全自主技术雷达 (`tool-omniscout-radar`) 对 **"software documentation citation provenance and architectural decision records"** 领域进行了极限检索与多维穿透，深度解构了全球工业界成熟方案与学术规范。
> 坚决杜绝“闭门造车”与“无根之木”，本着**“吸收精华、批判继承、杜绝冗余”**的原则确立了本项目的独创性基座。

| 权威源流 / 开源基座 | 源流分类 | 核心思想 / 机制突破 | 本项目吸收 / 借鉴要点 | 超越点与取舍 (Trade-offs) |
| :--- | :--- | :--- | :--- | :--- |
| **[MADR (Markdown Architecture Decision Records)](https://adr.github.io/madr/)** [^1] | `INDUSTRY_STANDARD` | 提出轻量级 Markdown 决策记录格式，强调列出备选方案 (Considered Options) 与推导依据 | 吸收其精炼的对标表格与决策动因 (Decision Drivers) 结构 | 剔除其对 Node.js/npm 的外部工具链绑定，全内核 100% 采用 Python 标准库实现 |
| **[Rust RFC Process & Kubernetes KEP](https://github.com/rust-lang/rfcs)** [^2] | `SPEC_RFC` | 强制要求技术方案在合并前必须经过详尽的 Prior Art 与 Alternatives Considered 论证 | 吸收其必须回答为什么不选方案 X 的严格推导脉络 | 将语言级与大规模集群规范提炼为跨所有项目的通用轻量自动化契约 |
| **[Citation File Format (CFF)](https://citation-file-format.github.io/)** [^3] | `ACADEMIC_STANDARD` | 专为科研软件与开源工程制定的机器可读引用标准 (v1.2.0)，被 GitHub 与 Zenodo 官方原生解析渲染 | 完整支持出厂自动化生成标准 CITATION.cff | 补充了 CFF 所缺失的 AI 雷达检索词与动态量规记录，衍生出互补的 .provenance.json |
| **[W3C PROV-DM (Provenance Data Model)](https://www.w3.org/TR/prov-dm/)** [^4] | `W3C_STANDARD` | 形式化定义信息谱系实体、活动与执行主体的溯源依赖拓扑 | 吸收其谱系推导链条思想 (Project <- Activity <- Radar <- Search) | 舍弃 W3C 极其繁琐沉重的 XML/OWL 本体论，压缩为纳秒级解析的轻量 JSON 谱系账本 |
| **[Diátaxis Documentation Framework](https://diataxis.fr/)** [^5] | `INDUSTRY_STANDARD` | 软件文档四分法，将架构思考归入 Explanation 避免污染快速上手 | 吸收其分层思想，使溯源矩阵既能充当认知门面，又不干扰极速 QuickStart | 增加自适应锚点识别算法，使注入过程对异构 Markdown 格式达到非破坏性平衡 |
| **[OmniScout-Radar (全知元阵)](https://github.com/Longgekutta/tool-omniscout-radar)** [^6] | `FIRST_PARTY_RADAR` | 4 阶段全自主技术侦察 (动态本体合成 -> 双轨并发探针 -> 拓扑滚雪球采样 -> 动态金丝雀量规审计) | 充当原生底层搜索引擎与权威源流提供方，实现一键从全网雷达到文档注入的闭环 | 本工具专精于引用提纯、五维量规审计与有机融合，与雷达的全网穿透搜索形成严密正交分工 |

### 📚 权威引用与事实锚点 (Normative Footnotes)
[^1]: **MADR (Markdown Architecture Decision Records)**: [https://adr.github.io/madr/](https://adr.github.io/madr/). *提出轻量级 Markdown 决策记录格式，强调列出备选方案 (Considered Options) 与推导依据*
[^2]: **Rust RFC Process & Kubernetes KEP**: [https://github.com/rust-lang/rfcs](https://github.com/rust-lang/rfcs). *强制要求技术方案在合并前必须经过详尽的 Prior Art 与 Alternatives Considered 论证*
[^3]: **Citation File Format (CFF)**: [https://citation-file-format.github.io/](https://citation-file-format.github.io/). *专为科研软件与开源工程制定的机器可读引用标准 (v1.2.0)，被 GitHub 与 Zenodo 官方原生解析渲染*
[^4]: **W3C PROV-DM (Provenance Data Model)**: [https://www.w3.org/TR/prov-dm/](https://www.w3.org/TR/prov-dm/). *形式化定义信息谱系实体、活动与执行主体的溯源依赖拓扑*
[^5]: **Diátaxis Documentation Framework**: [https://diataxis.fr/](https://diataxis.fr/). *软件文档四分法，将架构思考归入 Explanation 避免污染快速上手*
[^6]: **OmniScout-Radar (全知元阵)**: [https://github.com/Longgekutta/tool-omniscout-radar](https://github.com/Longgekutta/tool-omniscout-radar). *4 阶段全自主技术侦察 (动态本体合成 -> 双轨并发探针 -> 拓扑滚雪球采样 -> 动态金丝雀量规审计)*
