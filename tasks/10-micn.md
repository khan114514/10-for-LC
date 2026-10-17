# 10 · MICN

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://openreview.net/forum?id=zt53IDUR1U)：MICN: Multi-scale Local and Global Context Modeling for Long-term Series Forecasting（ICLR 2023）。
- 官方源码：[wanghq21/MICN](https://github.com/wanghq21/MICN/tree/370c69b841d72246556ca05dd23163c560c22b5a)，固定提交 `370c69b841d72246556ca05dd23163c560c22b5a`。
- 代码许可：未发现根目录许可证；正式再分发需解决授权或独立实现。
- 范围：**ETTh1 多变量；输入 96，预测 96；完整多尺度卷积**。适配类型 `NATIVE_SMALL_BENCHMARK`。
- 主指标：训练集标准化尺度全通道 MSE，越低越好；MAE 为质量门。

## 健康 Baseline

采用官方 ETTh1 单窗口 regre 分支：conv_kernel=[12,16]、d_layers=1、d_model=512、seq_len=label_len=pred_len=96。保留多尺度分解、局部/全局卷积、反卷积和趋势回归，完整训练到 Dev 早停。

## 数据准备与切分

- ETTh1.csv；固定版本内容信息见 ett-assets.json。
- data/data_loader.py 的时间边界、变量顺序、scaler 和时间特征共同冻结；未来 decoder 数值必须置零或仅含已知历史。

资产入口：[入口 1](https://github.com/zhouhaoyi/ETDataset).

## 代码入口与启动依据

python -u run.py --model micn --mode regre --data ETTh1 --features M --freq h --conv_kernel 12 16 --d_layers 1 --d_model 512 --seq_len 96 --label_len 96 --pred_len 96；数据路径与环境仍需预检。

- [models/model.py](https://github.com/wanghq21/MICN/blob/370c69b841d72246556ca05dd23163c560c22b5a/models/model.py)
- [models/local_global.py](https://github.com/wanghq21/MICN/blob/370c69b841d72246556ca05dd23163c560c22b5a/models/local_global.py)
- [data/data_loader.py](https://github.com/wanghq21/MICN/blob/370c69b841d72246556ca05dd23163c560c22b5a/data/data_loader.py)
- [exp/exp_informer.py](https://github.com/wanghq21/MICN/blob/370c69b841d72246556ca05dd23163c560c22b5a/exp/exp_informer.py)
- [scripts/ETTh.sh](https://github.com/wanghq21/MICN/blob/370c69b841d72246556ca05dd23163c560c22b5a/scripts/ETTh.sh)
- [run.py](https://github.com/wanghq21/MICN/blob/370c69b841d72246556ca05dd23163c560c22b5a/run.py)

## 三个方法改动面（作者侧候选，收益未验证）

1. 多尺度分解：基于历史的可学习趋势/季节分离。
2. 跨尺度融合：信息依赖门控或残差混合，替换固定融合方式。
3. 局部/全局卷积：共享低秩或结构化长程算子；保留预测接口与资源约束。

## 制作前必须完成的适配

- exp_informer 训练中每轮读 test_loss；改为仅 Dev，独立 Verifier 才能读取 private。
- 显式配置设备与数据路径；源码 device 默认 cuda:0，不能与调度分配冲突。
- 未发现根目录 LICENSE；正式再分发前解决授权或独立实现并复现，不直接复制上游无许可代码。

## 中等预评与开工门槛

一次训练联合趋势回归和季节卷积，已有 checkpoint 重载；主要修复私有评测边界与设备配置。 单卡预检；一个数据集和窗口，512 维完整模型的显存/时间待测。

[八维评级记录](../reports/selection/micn-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
