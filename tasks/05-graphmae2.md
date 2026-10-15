# 05 · GraphMAE2：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[GraphMAE2: A Decoding-Enhanced Masked Self-Supervised Graph Learner](https://doi.org/10.1145/3543507.3583379)，WWW 2023。
- 官方仓库：[THUDM/GraphMAE2](https://github.com/THUDM/GraphMAE2)；锁定提交 `bc473e8b750d6e90b7cba1c6bb20d858f617d90c`。
- 目标范围：ogbn-arxiv mini-batch 表征学习；PubMed 仅用于 smoke，正式评分不替代 arxiv。
- 代码授权：MIT（代码）；数据使用条款另外核对。
- 在线查重：2026-10-15，`pass`，最高相似度 0.5854，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

完整 GraphMAE2：多次 remasking、latent target teacher、EMA 与下游线性探针。arxiv 配置预训练 60 epochs、探针 1000 epochs；以充分训练证据审核，不删 teacher 或降低探针预算。

**主指标及质量门**：官方 ogbn-arxiv 节点分类 accuracy；固定线性探针容量、预算和 temporal split。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- [OGB 官方数据说明](https://ogb.stanford.edu/docs/nodeprop/#ogbn-arxiv)：原生下载 ogbn-arxiv；固定版本与原始 split。
- local cluster 需要 LocalGraphClustering；作者可下载预生成簇 https://cloud.tsinghua.edu.cn/d/64f859f389ca43eda472/ 或从同一图重建，固定构建程序、seed 和簇哈希。

- 资源规划：单卡 24–48GB 作为预检申请范围；簇缓存和 CPU 内存另行测量，不承诺最低配置。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
bash run_minibatch.sh ogbn-arxiv 0
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- remasking 调度与重建目标的结构化替换。
- teacher 目标更新和置信度选择，保持稳定性约束。
- 局部簇采样/上下文覆盖机制，保持数据和总训练预算。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- 把簇预处理的版本与图哈希绑定；不得在 Dev/test 标签上构造采样权重。
- 保留官方时间切分；允许的 transductive 公开特征/边须明确，私有标签隔离。
- 线性探针与表征权重分别保存，重新评分从冻结权重重载；评测协议变化两边同步。

## 困难预评与退回条件

环境轴 E=5/8（困难），优化轴 O=4/8（中等）；E4=2 触发困难。依据：簇预处理→双目标掩码训练→表征导出→固定线性探针，多级资产与 EMA 状态需绑定；mini-batch 与完整图评测有独立实现边界。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/graphmae2-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [main_large.py](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/main_large.py)
- [models/edcoder.py](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/models/edcoder.py)
- [models/finetune.py](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/models/finetune.py)
- [configs/ogbn-arxiv.yaml](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/configs/ogbn-arxiv.yaml)
- [datasets/localclustering.py](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/datasets/localclustering.py)
- [datasets/lc_sampler.py](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/datasets/lc_sampler.py)
- [run_minibatch.sh](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/run_minibatch.sh)
- [requirements.txt](https://github.com/THUDM/GraphMAE2/blob/bc473e8b750d6e90b7cba1c6bb20d858f617d90c/requirements.txt)
