# 10 个 AutoResearch 新选题 · LC 交接

已准备十道训练题的作者侧设计材料和修正版 `autoresearch-manager`。论文正式出处、官方源码固定提交及在线查重已核对；十题均为**困难预评**。这是选题与制作交接，尚未完成十题 GPU 复现、正式题包、Reference 改善或最终双 AI 验收。

| 编号 | 题目卡 | 正式发表 | 冻结前拟定范围 |
|---|---|---|---|
| 01 | [ConsisGAD](tasks/01-consisgad.md) | ICLR 2024 | Amazon 主任务；YelpChi 作为固定第二场景，分别冻结有限标签比例与切分 |
| 02 | [TimeSiam](tasks/02-timesiam.md) | ICML 2024 | ETTh1 + ETTh2；PatchTST 编码器；预测长度 96/192/336/720，预训练后分别微调 |
| 03 | [SimMTM](tasks/03-simmtm.md) | NeurIPS 2023 | 分类分支：SleepEEG 无标签预训练 → Epilepsy 小样本迁移；与 TF-C 使用不同方法接口 |
| 04 | [TF-C](tasks/04-tfc.md) | NeurIPS 2022 | SleepEEG 无标签预训练 → Epilepsy 小样本分类；时间与频率双编码器 |
| 05 | [GraphMAE2](tasks/05-graphmae2.md) | WWW 2023 | ogbn-arxiv mini-batch 表征学习；PubMed 仅用于 smoke，正式评分不替代 arxiv |
| 06 | [BGRL](tasks/06-bgrl.md) | ICLR 2022 | PPI inductive multi-label 节点表征学习；不以 WikiCS 替代正式任务 |
| 07 | [AFGRL](tasks/07-afgrl.md) | AAAI 2022 | WikiCS 节点聚类；固定同一图和无监督选择规则 |
| 08 | [LightGCL](tasks/08-lightgcl.md) | ICLR 2023 | Gowalla 全物品召回；冻结从 train 划出的 Dev |
| 09 | [DCCF](tasks/09-dccf.md) | SIGIR 2023 | Tmall 全物品推荐；从原 train 冻结独立 Dev |
| 10 | [AdaGCL](tasks/10-adagcl.md) | KDD 2023 | LastFM 自适应图对比推荐；Yelp 仅作为后续固定扩展，不默认并入本题 |

上一批 GAD-NR、SoftCLT、RecDCL 不在本批中。SimMTM 与 TF-C 虽共用一组迁移数据，但分别开放 masked manifold reconstruction 与时频双编码器一致性，不能制作成相同任务仅改标题。

## 接手顺序

1. 阅读 [共同制作与验收要求](requirements/common.md)、[选题证据与边界](reports/selection/README.md)。
2. 阅读每题卡，核验数据获取与授权，填 [preflight 模板](templates/preflight.md)，再冻结合同；不能跳过健康 Baseline 直接做 Reference。
3. 按 [运行交接说明](requirements/runbook.md) 使用本仓库修正的 manager；完整正式流程保留 10h 双轨、当前 SHA 复验、NOP、12h 稳定性与相同 ZIP 双 AI PASS。
4. 本仓库含论文答案和作者方法方向，**整仓不能挂给 Actor，也不能作为提交题包或 QA 的被审 ZIP**。

## 工具与验证

- `python3 tools/verify_handoff.py`：核验交接文件清单、十题完整性及未修改的 QA v0.3.4。
- `python3 tools/fetch_source.py consisgad --dest /absolute/author-only/source`：获取指定提交的官方源码；只下载，不安装或执行，目标目录必须为空。其余 id 见 `manifests/tasks.json`。
- [Skill 审查与修复](reports/skill-review/README.md)：优先修复恢复时重跑已成功 10h 轨迹的问题，也修复配置恢复、Python driver 路径和 reviewer 身份检查。
- [验证记录](reports/validation/README.md)：管理器独立复测 34 项通过，另有真实 Docker 隔离测试；模拟模型输出不代表正式研究 QA。

代码和数据授权分别核验；五个上游仓库未发现根目录许可证，已在题卡明确标注。此仓库只提供链接和自写设计材料，不转载这些上游实现。实际训练成本、资产完整性和算法改进尚须目标机实测；困难评级不能代替这一步。
