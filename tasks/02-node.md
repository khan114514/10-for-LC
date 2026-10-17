# 02 · NODE

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://openreview.net/forum?id=r1eiu2VtwH)：Neural Oblivious Decision Ensembles for Deep Learning on Tabular Data（ICLR 2020）。
- 官方源码：[Qwicen/node](https://github.com/Qwicen/node/tree/3bae6a8a63f0205683270b6d566d9cfa659403e4)，固定提交 `3bae6a8a63f0205683270b6d566d9cfa659403e4`。
- 代码许可：MIT（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**A9A 二分类；可微 oblivious tree ensemble；单阶段**。适配类型 `CLI_ADAPTER_REQUIRED`。
- 主指标：ROC-AUC，越高越好；log-loss 与分类准确率为质量门。

## 健康 Baseline

保留 ODST 软特征选择、阈值/温度、叶响应和 DenseBlock。以官方论文/配置的健康 A9A 模型为起点；禁止将其退化为单棵小树。原仓库训练示例主要是 notebook，先提取可复现 CLI，冻结树数、深度、层数和早停。

## 数据准备与切分

- A9A 官方 LIBSVM 数据：训练 32,561、测试 16,281、123 维；lib/data.py 已有 fetch_A9A。
- 保留测试集，train 内冻结分层 Dev 与行 ID。原 Dropbox split 不可用时必须显式形成新合同，不能默默更换切分。

资产入口：[入口 1](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary.html#a9a)；[入口 2](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/a9a)；[入口 3](https://www.csie.ntu.edu.tw/~cjlin/libsvmtools/datasets/binary/a9a.t).

## 代码入口与启动依据

lib.Dataset("A9A", ...) + lib.DenseBlock + lib.Trainer；需要把 notebook 训练循环提取为 CLI，尚未提供已跑通的 A9A driver。

- [lib/data.py](https://github.com/Qwicen/node/blob/3bae6a8a63f0205683270b6d566d9cfa659403e4/lib/data.py)
- [lib/arch.py](https://github.com/Qwicen/node/blob/3bae6a8a63f0205683270b6d566d9cfa659403e4/lib/arch.py)
- [lib/odst.py](https://github.com/Qwicen/node/blob/3bae6a8a63f0205683270b6d566d9cfa659403e4/lib/odst.py)
- [lib/trainer.py](https://github.com/Qwicen/node/blob/3bae6a8a63f0205683270b6d566d9cfa659403e4/lib/trainer.py)

## 三个方法改动面（作者侧候选，收益未验证）

1. ODST：结构化特征选择分布，替换软选择映射，而非只调温度。
2. 软分箱：单调门或校准阈值机制，保持可微树结构。
3. DenseBlock：跨层树输出与原始特征的选择/聚合机制。

## 制作前必须完成的适配

- 旧 numpy 的 np.int、entmax/qhoptim 等依赖先适配，B/R 共享；依赖修复不算方法增益。
- 数据感知初始化仅使用 train。禁止预初始化时混入 Dev/private。
- Trainer 保存的是自身 state_dict（含 model 命名空间）；CLI 重载必须验证同一对象和输出，checkpoint 平均策略事先冻结。

## 中等预评与开工门槛

Dataset/ODST/Trainer 的单阶段组件齐全，CLI、选优与独立重载需装配；没有预训练到下游的第二训练阶段。 单卡预检；作者提示实现显存效率有限，须记录树张量峰值，不能直接承诺低显存。

[八维评级记录](../reports/selection/node-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
