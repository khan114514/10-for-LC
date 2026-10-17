# 01 · DANet

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://ojs.aaai.org/index.php/AAAI/article/view/20309)：DANets: Deep Abstract Networks for Tabular Data Classification and Regression（AAAI 2022）。
- 官方源码：[WhatAShot/DANet](https://github.com/WhatAShot/DANet/tree/b007c57121ec9082f6ef19ec7465d9df70767c26)，固定提交 `b007c57121ec9082f6ef19ec7465d9df70767c26`。
- 代码许可：MIT（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**California Housing 回归；完整 DANet-20；新增小数据适配**。适配类型 `NEW_DATASET_ADAPTER_REQUIRED`。
- 主指标：原目标单位 RMSE，越低越好；MAE 为质量门。

## 健康 Baseline

保留 LearnableLocality、AbstractLayer、原始特征 shortcut 和完整 DANet-20。官方默认 max_epochs=4000、patience=1500；不能照搬巨大 batch 到小数据后少更新。先用公开 Dev 确认充分训练与 ghost batch 行为，再冻结 B/R 共用预算。

## 数据准备与切分

- California Housing：20,640 样本、8 个数值特征；使用 sklearn 官方 fetch_california_housing 数据定义，原始文件与处理数组分别计算哈希。
- 这是论文方法在新小数据上的自命题，不是论文七数据集原表复现。拟固定 60/20/20 随机切分，保存行 ID；只在 train 拟合分位数变换与目标标准化。

资产入口：[入口 1](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html).

## 代码入口与启动依据

main.py 的 -c/--config、-g/--gpu_id；尚无 California 配置或 loader，先编写共享适配器，不提供可直接跑通的猜测命令。

- [main.py](https://github.com/WhatAShot/DANet/blob/b007c57121ec9082f6ef19ec7465d9df70767c26/main.py)
- [config/default.py](https://github.com/WhatAShot/DANet/blob/b007c57121ec9082f6ef19ec7465d9df70767c26/config/default.py)
- [model/DANet.py](https://github.com/WhatAShot/DANet/blob/b007c57121ec9082f6ef19ec7465d9df70767c26/model/DANet.py)
- [data/dataset.py](https://github.com/WhatAShot/DANet/blob/b007c57121ec9082f6ef19ec7465d9df70767c26/data/dataset.py)
- [abstract_model.py](https://github.com/WhatAShot/DANet/blob/b007c57121ec9082f6ef19ec7465d9df70767c26/abstract_model.py)

## 三个方法改动面（作者侧候选，收益未验证）

1. LearnableLocality：设计输入条件化的稀疏特征分组，而非只调组数 k。
2. AbstractLayer：改组内特征组合与门控函数，保持接口维度和预算可比。
3. BasicBlock：改原始特征与深层表示的残差融合机制。

## 制作前必须完成的适配

- 添加 California loader 和回归配置；当前通用默认配置没有回归分支所需全部字段，必须逐项补齐。
- 完整保存变换器、目标均值/标准差、模型结构和选中权重；新进程回归评分恢复原单位。
- 小数据更容易过拟合；先审健康 B 的曲线和改善余量，不能通过删除层或压低训练轮次制造增益。

## 中等预评与开工门槛

单阶段监督回归，main.py 已有验证选优与预测调用；新增 loader/配置和独立重载尚未完成。 单卡预检；DANet-20 的总收敛时间待测，旧配置长 patience 是优先风险。

[八维评级记录](../reports/selection/danet-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
