# 06 · RevIN + SCINet

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://openreview.net/forum?id=cGDAkQo1C0p)：Reversible Instance Normalization for Accurate Time-Series Forecasting against Distribution Shift（ICLR 2022）。
- 官方源码：[ts-kim/RevIN](https://github.com/ts-kim/RevIN/tree/fee40bc6c87cb536d048bcf1c14c4ed644b875e1)，固定提交 `fee40bc6c87cb536d048bcf1c14c4ed644b875e1`。
- 代码许可：MIT（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**ETTh1 多变量；输入 96，预测 48；固定 SCINet 主干**。适配类型 `NATIVE_SMALL_BENCHMARK`。
- 主指标：训练集标准化尺度上的全通道 MSE，越低越好；MAE 为质量门。

## 健康 Baseline

完整官方 SCINet+RevIN（--ours）。采用脚本 ETTh1 I96/O48：hidden-size 4、stacks 1、levels 3、lr .009、batch 16、dropout .25；充分训练与早停实测后冻结。不能用不含 RevIN 的 SCINet 作正式评分锚点。

## 数据准备与切分

- ETDataset 的 ETTh1.csv；版本和下载内容哈希见 ett-assets.json。
- 按官方小时数据连续时间边界冻结 train/Dev/private；滑窗预测区间不能越过所属划分。历史上下文可重叠，未来标签不能参与归一化。

资产入口：[入口 1](https://github.com/zhouhaoyi/ETDataset).

## 代码入口与启动依据

官方 scripts/scinet_with_RevIN.sh 的 ETTh1 I96/O48 单条命令；执行目录 baselines/SCINet。不要直接运行整份多数据/多窗口 sweep。

- [RevIN.py](https://github.com/ts-kim/RevIN/blob/fee40bc6c87cb536d048bcf1c14c4ed644b875e1/RevIN.py)
- [baselines/SCINet/run_ETTh.py](https://github.com/ts-kim/RevIN/blob/fee40bc6c87cb536d048bcf1c14c4ed644b875e1/baselines/SCINet/run_ETTh.py)
- [baselines/SCINet/scripts/scinet_with_RevIN.sh](https://github.com/ts-kim/RevIN/blob/fee40bc6c87cb536d048bcf1c14c4ed644b875e1/baselines/SCINet/scripts/scinet_with_RevIN.sh)
- [baselines/SCINet/experiments/exp_ETTh.py](https://github.com/ts-kim/RevIN/blob/fee40bc6c87cb536d048bcf1c14c4ed644b875e1/baselines/SCINet/experiments/exp_ETTh.py)
- [baselines/SCINet/data_process/etth_data_loader.py](https://github.com/ts-kim/RevIN/blob/fee40bc6c87cb536d048bcf1c14c4ed644b875e1/baselines/SCINet/data_process/etth_data_loader.py)
- [baselines/SCINet/models/SCINet.py](https://github.com/ts-kim/RevIN/blob/fee40bc6c87cb536d048bcf1c14c4ed644b875e1/baselines/SCINet/models/SCINet.py)

## 三个方法改动面（作者侧候选，收益未验证）

1. 统计量：只用历史窗口的稳健中心/尺度估计器。
2. 仿射映射：由历史模式条件化的可逆变换，主干结构固定。
3. 尺度恢复：按预测跨度估计的历史条件化校准；不得访问未来真值。

## 制作前必须完成的适配

- 将按 batch 暂存的均值/标准差绑定到正确一次前向，避免并发/重载误配。
- 原训练循环每轮调用 test；移除私有读写，Dev 选择后由独立 Verifier 运行。
- 确认集成 SCINet 内实际 --ours 路径；不能只改根目录 RevIN.py 却未进入训练模型。

## 中等预评与开工门槛

归一化、SCINet 和反归一化在一次监督训练内完成；官方单窗口命令与 checkpoint 路径存在。 单卡预检；一个窗口、一个数据集，仍保留完整 SCINet 和 RevIN。

[八维评级记录](../reports/selection/revins-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
