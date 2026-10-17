# 09 · EvenNet

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://proceedings.neurips.cc/paper_files/paper/2022/hash/1e62dae07279cb09d2e87378d10dacfc-Abstract-Conference.html)：EvenNet: Ignoring Odd-Hop Neighbors Improves Robustness of Graph Neural Networks（NeurIPS 2022）。
- 官方源码：[Leirunlin/EvenNet](https://github.com/Leirunlin/EvenNet/tree/8b0477c01dd7aa3bcf00ea4a368310013978fb84)，固定提交 `8b0477c01dd7aa3bcf00ea4a368310013978fb84`。
- 代码许可：未发现根目录许可证；正式再分发需解决授权或独立实现。
- 范围：**Cora + Citeseer；clean graph 节点分类；偶数阶传播**。适配类型 `NATIVE_SMALL_BENCHMARK`。
- 主指标：两个图 accuracy 等权平均，越高越好；各图质量门冻结。仅声明 clean classification，不声称完成鲁棒攻击评测。

## 健康 Baseline

完整 EvenNet：MLP 与可学习偶数阶图滤波。采用 src/exp_common.sh 的两图配置，K=10、hidden=64、epochs=1000、early_stopping=200，具体 drop/lr 按图冻结；保留原方法核心。

## 数据准备与切分

- DatasetLoader 的 Cora/Citeseer Planetoid 数据；记录实际下载版本和节点 ID。
- 原 main_common 每 run 使用不同 split seed；正式合同显式分离 split seed 和初始化 seed，冻结全部组合，B/R 配对运行。

资产入口：[入口 1](https://github.com/kimiyoung/planetoid/tree/master/data).

## 代码入口与启动依据

src/exp_common.sh 只取 cora 与 citeseer 两条；main_common.py --net EvenNet。clean 分支仍 import attack/deeprobust，先做共享依赖适配。

- [src/main_common.py](https://github.com/Leirunlin/EvenNet/blob/8b0477c01dd7aa3bcf00ea4a368310013978fb84/src/main_common.py)
- [src/train_common.py](https://github.com/Leirunlin/EvenNet/blob/8b0477c01dd7aa3bcf00ea4a368310013978fb84/src/train_common.py)
- [src/propagate.py](https://github.com/Leirunlin/EvenNet/blob/8b0477c01dd7aa3bcf00ea4a368310013978fb84/src/propagate.py)
- [src/models.py](https://github.com/Leirunlin/EvenNet/blob/8b0477c01dd7aa3bcf00ea4a368310013978fb84/src/models.py)
- [src/parse.py](https://github.com/Leirunlin/EvenNet/blob/8b0477c01dd7aa3bcf00ea4a368310013978fb84/src/parse.py)
- [src/exp_common.sh](https://github.com/Leirunlin/EvenNet/blob/8b0477c01dd7aa3bcf00ea4a368310013978fb84/src/exp_common.sh)

## 三个方法改动面（作者侧候选，收益未验证）

1. 偶数阶系数：稳定性约束的滤波参数化，不能只扫描 K。
2. 传播通道：特征组相关的偶数阶滤波与融合。
3. 特征输出：局部输入与传播表征的自适应残差结合。

## 制作前必须完成的适配

- Exp.fit 只把 best weights 留在内存；补落盘、配置绑定和独立重载，不用内存对象冒充交付模型。
- 清理未使用攻击依赖时保证训练等价，且 B/R 共用；不在本题扩展攻击网格。
- 未发现根目录 LICENSE。这里只交接链接与原创设计；正式分发实现前解决授权或从论文独立实现，并复验健康 B。

## 中等预评与开工门槛

clean 分支单次监督训练、Dev loss 选优；需把内存 best 权重持久化，不需要对抗生成或第二模型训练。 单卡预检；两张小图，原攻击/注入实验不纳入本题范围。

[八维评级记录](../reports/selection/evennet-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
