# 07 · Leddam

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://openreview.net/forum?id=87CYNyCGOo)：Revitalizing Multivariate Time Series Forecasting: Learnable Decomposition with Inter-Series Dependencies and Intra-Series Variations Modeling（ICML 2024）。
- 官方源码：[Levi-Ackman/Leddam](https://github.com/Levi-Ackman/Leddam/tree/5a145f78f4425be73c9b0b0f0ef527730f35afbf)，固定提交 `5a145f78f4425be73c9b0b0f0ef527730f35afbf`。
- 代码许可：MIT（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**ETTh2 多变量；输入 96，预测 96；完整分解与双注意力**。适配类型 `NATIVE_SMALL_BENCHMARK`。
- 主指标：训练集标准化尺度全通道 MSE，越低越好；MAE 为质量门。

## 健康 Baseline

保留可学习分解、channel attention 和 auto-regressive attention。官方 ETTh2 脚本的 I96/O96 配置：d_model 256、n_layers 1、batch 128、lr 1e-4、dropout 0；不删除任一双注意力分支。

## 数据准备与切分

- ETTh2.csv；版本、内容哈希、列和行数见 ett-assets.json。
- 按 data_provider/data_loader.py 的小时边界冻结切分，scaler 仅 fit train；评测覆盖全部有效窗口。

资产入口：[入口 1](https://github.com/zhouhaoyi/ETDataset).

## 代码入口与启动依据

scripts/ETTh2/ETTh2.sh 仅取 pred_len=96 的一组配置；先把写死的 GPU 2 和数据目录改为可信主控参数。

- [models/Leddam.py](https://github.com/Levi-Ackman/Leddam/blob/5a145f78f4425be73c9b0b0f0ef527730f35afbf/models/Leddam.py)
- [layers/Leddam.py](https://github.com/Levi-Ackman/Leddam/blob/5a145f78f4425be73c9b0b0f0ef527730f35afbf/layers/Leddam.py)
- [scripts/ETTh2/ETTh2.sh](https://github.com/Levi-Ackman/Leddam/blob/5a145f78f4425be73c9b0b0f0ef527730f35afbf/scripts/ETTh2/ETTh2.sh)
- [exp/exp_long_term_forecasting.py](https://github.com/Levi-Ackman/Leddam/blob/5a145f78f4425be73c9b0b0f0ef527730f35afbf/exp/exp_long_term_forecasting.py)
- [data_provider/data_loader.py](https://github.com/Levi-Ackman/Leddam/blob/5a145f78f4425be73c9b0b0f0ef527730f35afbf/data_provider/data_loader.py)

## 三个方法改动面（作者侧候选，收益未验证）

1. 分解层：受约束的可学习平滑核或分布条件化分解。
2. 通道注意力：结构化变量分组与交互选择。
3. 自回归注意力：多尺度滞后聚合或状态依赖读出。

## 制作前必须完成的适配

- 每轮 test_loss 输出移到独立评测环境。
- 明确 test(setting, test=1) 重载 best checkpoint；禁止将训练最后一轮权重与 best 日志混配。
- 固定 revin 配置；本题开放分解/注意力，归一化模块冻结，与 RevIN 题保持独立接口。

## 中等预评与开工门槛

官方模型、单配置脚本和预测循环完整；分解与双注意力端到端一次训练，不需迁移。 单卡预检；7 通道与短固定窗口，排除 Electricity/Traffic 和八数据集 sweep。

[八维评级记录](../reports/selection/leddam-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
