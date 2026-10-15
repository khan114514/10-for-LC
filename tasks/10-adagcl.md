# 10 · AdaGCL：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[Adaptive Graph Contrastive Learning for Recommendation](https://doi.org/10.1145/3580305.3599768)，KDD 2023。
- 官方仓库：[HKUDS/AdaGCL](https://github.com/HKUDS/AdaGCL)；锁定提交 `6359f1ed568bf3f99d6351848b9a0c7391c1c93f`。
- 目标范围：LastFM 自适应图对比推荐；Yelp 仅作为后续固定扩展，不默认并入本题。
- 代码授权：未发现根目录 LICENSE；不随本交接转载上游源码，正式再分发需先解决授权或独立实现。
- 在线查重：2026-10-15，`pass`，最高相似度 0.7402，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

完整推荐器、可训练生成视图与去噪视图及耦合目标。LastFM 示例 gamma=-0.95、ib_reg=1e-2；Params 默认 200 epochs，须按实际参数解析和曲线确认充分训练。

**主指标及质量门**：Recall@20 为主、NDCG@20 为质量门；使用原 val 切分进行选择。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- 固定源码 Datasets/lastFM/{trnMat,valMat,tstMat}.pkl；严格使用原三分法，转换后保存一致性和哈希记录。
- Model.py 多套网络和 Main.py 多优化器需要整体保存，单一推荐 embedding 不一定能重建训练或推理状态。

- 资源规划：单卡 24GB 起做预检；实测后冻结显存、CPU、内存和磁盘预算。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
python Main.py --data lastfm --gamma -0.95 --ib_reg 1e-2
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- 生成图视图的边分布/结构先验与采样机制。
- DenoisingNet 的可学习过滤目标与图一致性策略。
- 推荐器与两个视图的训练耦合/更新规则，区别于固定 SVD 或意图解耦。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- 默认 GPU 参数与 .cuda 路径需核对，按容器设备映射统一修正；预检保存实际 argv。
- 每轮 test 改成 val 选择；私有 test 只在正式评测中使用。
- 分别保存生成器、去噪器、推荐器与各自优化状态，检查重载后的实际预测一致性；固定随机视图采样 seed。

## 困难预评与退回条件

环境轴 E=5/8（困难），优化轴 O=4/8（中等）；E4=2 触发困难。依据：生成式图模块、去噪网络和推荐器由多个优化器协同更新；checkpoint 完整性、视图采样和最终排名必须贯通验证。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/adagcl-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [Main.py](https://github.com/HKUDS/AdaGCL/blob/6359f1ed568bf3f99d6351848b9a0c7391c1c93f/Main.py)
- [Model.py](https://github.com/HKUDS/AdaGCL/blob/6359f1ed568bf3f99d6351848b9a0c7391c1c93f/Model.py)
- [Params.py](https://github.com/HKUDS/AdaGCL/blob/6359f1ed568bf3f99d6351848b9a0c7391c1c93f/Params.py)
- [DataHandler.py](https://github.com/HKUDS/AdaGCL/blob/6359f1ed568bf3f99d6351848b9a0c7391c1c93f/DataHandler.py)
