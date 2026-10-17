# 03 · MLP-PLR 数值嵌入

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://proceedings.neurips.cc/paper_files/paper/2022/hash/9e9f0ffc3d836836ca96cbf8fe14b105-Abstract-Conference.html)：On Embeddings for Numerical Features in Tabular Deep Learning（NeurIPS 2022）。
- 官方源码：[yandex-research/rtdl-num-embeddings](https://github.com/yandex-research/rtdl-num-embeddings/tree/a8fc25025c83f2321c63ff127a3bcef83bb1bfb5)，固定提交 `a8fc25025c83f2321c63ff127a3bcef83bb1bfb5`。
- 代码许可：MIT（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**California Housing；固定 MLP 主干，仅开放数值嵌入**。适配类型 `NATIVE_SMALL_BENCHMARK`。
- 主指标：原目标单位 RMSE，越低越好；MAE 与有限值检查为质量门。

## 健康 Baseline

使用完整 MLP-PLR，不用裸 MLP 作评分锚点。官方 California 配置为 positional→linear→relu、76 维嵌入、MLP [916]、batch 256、patience 16。n_epochs=inf 表示依赖早停，需在真实收敛预检后增加公平资源上限，不能任意截断。

## 数据准备与切分

- 官方 README 的 data.tar 含 data/california，保留官方 train/val/test 与目标缩放信息。
- 数值归一化/分箱仅拟合 train；不要把本题切分与 DANet 新适配切分混为一份论文分数。

资产入口：[入口 1](https://www.dropbox.com/s/r0ef3ij3wl049gl/data.tar?dl=1)；[入口 2](https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_california_housing.html).

## 代码入口与启动依据

bin/train4.py；配置 exp/mlp-plr/california/0_evaluation/0.toml。先按该提交 README 设置项目环境，再在独立输出目录运行；不启动整个 HPO/ensemble sweep。

- [bin/train4.py](https://github.com/yandex-research/rtdl-num-embeddings/blob/a8fc25025c83f2321c63ff127a3bcef83bb1bfb5/bin/train4.py)
- [lib/deep.py](https://github.com/yandex-research/rtdl-num-embeddings/blob/a8fc25025c83f2321c63ff127a3bcef83bb1bfb5/lib/deep.py)
- [lib/data.py](https://github.com/yandex-research/rtdl-num-embeddings/blob/a8fc25025c83f2321c63ff127a3bcef83bb1bfb5/lib/data.py)
- [exp/mlp-plr/california/0_evaluation/0.toml](https://github.com/yandex-research/rtdl-num-embeddings/blob/a8fc25025c83f2321c63ff127a3bcef83bb1bfb5/exp/mlp-plr/california/0_evaluation/0.toml)

## 三个方法改动面（作者侧候选，收益未验证）

1. 周期编码：学习特征相关的频带选择或稳定频率参数化。
2. 分段编码：基于 train 分布的可学习节点/平滑插值，替换编码函数。
3. 嵌入融合：组合局部与周期表示的特征级门控；下游 MLP 固定。

## 制作前必须完成的适配

- train4.py 每轮 evaluate([val,test])；任务适配中移除训练端 private/test 读取与输出，只允许公开 Dev。
- checkpoint 同时保存嵌入、主干和预处理；必须确认原目标单位反标准化。
- 训练缓存必须按数据、切分和预处理哈希隔离，不能让 B/R 误用不同变换。

## 中等预评与开工门槛

官方单个 California 配置、训练入口和 best checkpoint 重载均存在；主要补私有评测边界及新进程重载。 单卡预检；单数据集、单主干配置，不包含论文多模型 HPO 与五模型集成。

[八维评级记录](../reports/selection/numemb-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
