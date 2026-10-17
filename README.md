# 10 个中等 AutoResearch 选题 · LC 交接

按最新要求重新选择十道**中等预评**训练题，采用小型公开数据、固定窗口和单阶段训练。十题在线查重全部通过，已准备作者题卡、数据入口、固定源码提交、完整 Baseline 约束、三个方法改动面及适配清单。当前为 PREPARATION_ONLY；GPU 复现、实际改善和正式双 AI 验收尚未完成。

| 编号 | 题目卡 | 发表 | 本批范围 |
|---|---|---|---|
| 01 | [DANet](tasks/01-danet.md) | AAAI 2022 | California Housing 回归；完整 DANet-20；新增小数据适配 |
| 02 | [NODE](tasks/02-node.md) | ICLR 2020 | A9A 二分类；可微 oblivious tree ensemble；单阶段 |
| 03 | [MLP-PLR 数值嵌入](tasks/03-numemb.md) | NeurIPS 2022 | California Housing；固定 MLP 主干，仅开放数值嵌入 |
| 04 | [FT-Transformer](tasks/04-rtdl.md) | NeurIPS 2021 | Adult 二分类；完整 FT-Transformer；固定输入编码 |
| 05 | [ACM-GCN](tasks/05-acmgcn.md) | NeurIPS 2022 | Cora + Citeseer；小图监督节点分类；ACM-Pytorch 分支 |
| 06 | [RevIN + SCINet](tasks/06-revins.md) | ICLR 2022 | ETTh1 多变量；输入 96，预测 48；固定 SCINet 主干 |
| 07 | [Leddam](tasks/07-leddam.md) | ICML 2024 | ETTh2 多变量；输入 96，预测 96；完整分解与双注意力 |
| 08 | [Focal Frequency Loss](tasks/08-ffl.md) | ICCV 2021 | CIFAR-10 32×32 图像重建；官方 MLP 自编码器 + FFL |
| 09 | [EvenNet](tasks/09-evennet.md) | NeurIPS 2022 | Cora + Citeseer；clean graph 节点分类；偶数阶传播 |
| 10 | [MICN](tasks/10-micn.md) | ICLR 2023 | ETTh1 多变量；输入 96，预测 96；完整多尺度卷积 |

难度按动态双轴 PE 规则计算，十题均 E=4/8、O=4/8，置信度中。30 分钟低方差实验尚未实测；若实测升级为困难，换题或重新设计，不能靠欠训练、删除核心模块或调分维持中等。DANet、FFL 是显式小数据适配，NODE 需 CLI 装配；不称为论文全部实验的复现。

## 接手顺序

1. 阅读 [共同要求](requirements/common.md)和[选题证据](reports/selection/README.md)。
2. 按题卡完成数据/依赖适配，填写 [真实预检](templates/preflight.md)，确认充分训练 B、成本、方差和方法空间后冻结合同。
3. 使用 [修正版 manager](requirements/runbook.md)。中等选题仍保留健康 B/R、10h 双轨、当前 SHA 复验、NOP、12h 稳定性和同一 ZIP 双 AI PASS。
4. 整个仓库含作者答案和审核材料，**不能挂给 Actor、放进题目镜像或作为正式提交 ZIP**。

## 工具与既有 skill 修复

- `python3 tools/verify_handoff.py`：核验十题、评级、文件哈希和原版 QA v0.3.4。
- `python3 tools/fetch_source.py revins --dest /absolute/author-only/source`：只获取固定源码，不安装/执行；目标目录必须为空。
- [Skill 审查与修复](reports/skill-review/README.md)：保留前次已修复的单侧失败恢复、成功轨迹复用校验、输入阻塞恢复、driver 路径及 reviewer 身份检查；本轮未改 manager 或固定 QA。
- [验证记录](reports/validation/README.md)：区分本轮材料检查与 2026-10-15 的 34 项 manager/Docker 验证。

前一版困难十题保留在 [6370c57](https://github.com/khan114514/10-for-LC/tree/6370c579ee299e3346ff57d0997fc1a2ed7422bf)。本轮全部换题，也未重复更早的 GAD-NR、SoftCLT、RecDCL。EvenNet/MICN 的代码分发授权仍须确认；所有数据条款另行核验。
