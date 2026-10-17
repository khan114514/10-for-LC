# 05 · ACM-GCN

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://proceedings.neurips.cc/paper_files/paper/2022/hash/092359ce5cf60a80e882378944bf1be4-Abstract-Conference.html)：Revisiting Heterophily For Graph Neural Networks（NeurIPS 2022）。
- 官方源码：[SitaoLuan/ACM-GNN](https://github.com/SitaoLuan/ACM-GNN/tree/75b4853f29b2ce0844283e4a64c4b1120feb295c)，固定提交 `75b4853f29b2ce0844283e4a64c4b1120feb295c`。
- 代码许可：MIT（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**Cora + Citeseer；小图监督节点分类；ACM-Pytorch 分支**。适配类型 `NATIVE_SMALL_BENCHMARK`。
- 主指标：两个图各自 accuracy，等权宏平均为主；各图最低质量门预先冻结。

## 健康 Baseline

完整 ACM-GCN 的 aggregation、diversification、identity 三通道及自适应混合；使用官方 acmgcn 分支。不得把普通 GCN 当正式 B。先冻结健康超参数与 split×初始化 seed 组合。

## 数据准备与切分

- 源码 ../data/ 的 Planetoid Cora/Citeseer；公开整个图结构和无标签特征，隐藏 private 标签。
- 训练脚本有随机切分逻辑；先生成不可变 split manifest，再固定同一 split 上的独立初始化 seed。跨 split 波动不能误标为仅初始化方差。

资产入口：[入口 1](https://github.com/SitaoLuan/ACM-GNN/tree/75b4853f29b2ce0844283e4a64c4b1120feb295c/data)；[入口 2](https://github.com/kimiyoung/planetoid/tree/master/data).

## 代码入口与启动依据

在 ACM-Pytorch 下 python train.py --model acmgcn --dataset_name cora；Citeseer 同入口。原脚本多 split 循环需要改成冻结合同，不直接作为正式 driver。

- [ACM-Pytorch/train.py](https://github.com/SitaoLuan/ACM-GNN/blob/75b4853f29b2ce0844283e4a64c4b1120feb295c/ACM-Pytorch/train.py)
- [ACM-Pytorch/arg_parser.py](https://github.com/SitaoLuan/ACM-GNN/blob/75b4853f29b2ce0844283e4a64c4b1120feb295c/ACM-Pytorch/arg_parser.py)
- [ACM-Pytorch/utils.py](https://github.com/SitaoLuan/ACM-GNN/blob/75b4853f29b2ce0844283e4a64c4b1120feb295c/ACM-Pytorch/utils.py)
- [ACM-Pytorch/models/layers.py](https://github.com/SitaoLuan/ACM-GNN/blob/75b4853f29b2ce0844283e4a64c4b1120feb295c/ACM-Pytorch/models/layers.py)

## 三个方法改动面（作者侧候选，收益未验证）

1. 三通道选择：局部结构条件化的混合门，而非单一权重扫描。
2. 高通分支：归一化/去相关的局部差分算子。
3. 跨层融合：抑制过平滑的残差或多层通道聚合。

## 制作前必须完成的适配

- train.py 的 best_val_loss 分支保存测试分数而非独立持久化 checkpoint；补真正的 best 权重保存与新进程重载。
- 私有节点标签从 Actor 环境剥离；允许 transductive 图特征并不允许读全图标签。
- 只安装所选小图 PyTorch 分支需要的依赖；如果拆除未用下载/大型图 import，先验证等价，B/R 共用。

## 中等预评与开工门槛

小图 full-batch 单阶段监督；需补持久化选优权重和独立评分，不涉及 teacher/probe 或迁移。 单卡预检；选两张小图，排除大型图和异质采样分支。

[八维评级记录](../reports/selection/acmgcn-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
