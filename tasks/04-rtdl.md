# 04 · FT-Transformer

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://proceedings.neurips.cc/paper_files/paper/2021/hash/9d86d83f925f2149e9edb0ac3b49229c-Abstract.html)：Revisiting Deep Learning Models for Tabular Data（NeurIPS 2021）。
- 官方源码：[yandex-research/rtdl-revisiting-models](https://github.com/yandex-research/rtdl-revisiting-models/tree/e3ed46cac38568785289d8fa16b8cfa585bde27e)，固定提交 `e3ed46cac38568785289d8fa16b8cfa585bde27e`。
- 代码许可：Apache-2.0（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**Adult 二分类；完整 FT-Transformer；固定输入编码**。适配类型 `NATIVE_SMALL_BENCHMARK`。
- 主指标：ROC-AUC，越高越好；log-loss 和 accuracy 为质量门，Dev 选优指标同步冻结。

## 健康 Baseline

采用官方 output/adult/ft_transformer/tuned/0.toml 完整模型：d_token=352、3 层、8 头、ReGLU、batch 256、patience 16。保留类别/数值 token 和 CLS 路径，不以删注意力的弱模型作 B。实际充分训练时间需测定。

## 数据准备与切分

- 官方 data.tar.gz 中 data/adult，保存数值/类别数组、词表、缺失值规则和原 train/val/test。
- 未知类别索引、quantile 变换和标签映射只由 train 决定；不得从全部样本重拟合。

资产入口：[入口 1](https://www.dropbox.com/s/o53umyg6mn3zhxy/data.tar.gz?dl=1)；[入口 2](https://archive.ics.uci.edu/dataset/2/adult).

## 代码入口与启动依据

bin/ft_transformer.py；配置 output/adult/ft_transformer/tuned/0.toml。只采用一个冻结配置进行完整多 seed 训练，不能跑完大 sweep 后挑最差 B。

- [bin/ft_transformer.py](https://github.com/yandex-research/rtdl-revisiting-models/blob/e3ed46cac38568785289d8fa16b8cfa585bde27e/bin/ft_transformer.py)
- [lib/data.py](https://github.com/yandex-research/rtdl-revisiting-models/blob/e3ed46cac38568785289d8fa16b8cfa585bde27e/lib/data.py)
- [output/adult/ft_transformer/tuned/0.toml](https://github.com/yandex-research/rtdl-revisiting-models/blob/e3ed46cac38568785289d8fa16b8cfa585bde27e/output/adult/ft_transformer/tuned/0.toml)

## 三个方法改动面（作者侧候选，收益未验证）

1. MultiheadAttention：特征组结构或稀疏交互机制。
2. 残差更新：输入条件化的 token 门控与信息保留。
3. CLS/输出聚合：多层特征汇聚或样本自适应读出；输入编码固定，避免与数值嵌入题重合。

## 制作前必须完成的适配

- 官方评估循环会得到 test 指标；移除 Actor 训练端 test 路径，仅保留 Dev。
- 论文原比较不等于本题 AUC 合同：采用 AUC 选优前完成公开 Dev 预检，所有模型遵守同一规则。
- n_epochs=1000000000 由早停结束；验证收敛并冻结资源上限，避免无限任务或过早截断。

## 中等预评与开工门槛

单阶段表格 Transformer；完整配置、验证追踪、checkpoint 保存和重载已有实现，需拆分独立 Verifier。 单卡预检；Adult 规模小但 352 维三层模型仍需计时，不声称 30min 已通过。

[八维评级记录](../reports/selection/rtdl-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
