# 08 · LightGCL：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[LightGCL: Simple Yet Effective Graph Contrastive Learning for Recommendation](https://openreview.net/forum?id=FKXVK9dyMM)，ICLR 2023。
- 官方仓库：[HKUDS/LightGCL](https://github.com/HKUDS/LightGCL)；锁定提交 `5590453ad86782f58017e58d0b698d7f32175be3`。
- 目标范围：Gowalla 全物品召回；冻结从 train 划出的 Dev。
- 代码授权：未发现根目录 LICENSE；不随本交接转载上游源码，正式再分发需先解决授权或独立实现。
- 在线查重：2026-10-15，`pass`，最高相似度 0.6892，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

完整 LightGCL：低秩 SVD 全局视图、局部图传播、跨视图对比与 BPR。默认 100 epochs，Gowalla 示例 lambda2=0；不得移除 SVD 造弱 B。

**主指标及质量门**：Recall@20 为主、NDCG@20 为质量门；对所有合法物品排序，屏蔽训练已交互项。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- 固定源码含 data/gowalla/trnMat.pkl 与 tstMat.pkl；仅检查树和文件引用，尚未反序列化。
- 处理资产需在可信隔离准备环境转换为可审计的稀疏数值格式，再冻结哈希；Dev 从原训练交互中一次性划出。

- 资源规划：单卡 24GB 起做预检；实测后冻结显存、CPU、内存和磁盘预算。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
python main.py --data gowalla --lambda2 0
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- 谱分量选择与全局视图重构机制；保持低秩因子计算。
- 用户/物品度感知的正负样本选择与对比目标。
- 局部传播和全局信息的融合模块，避免只改温度或 SVD rank。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- 原实现每三轮测试；改为固定 Dev 选择，独立 test 不用于调参。
- 先划 Dev 再拟合训练图/SVD，不能用测试或 Dev 交互构图；固定随机 SVD 与负采样 seed。
- 保存可独立重建的权重、ID 映射及 SVD 因子；禁止无意物化巨型 dense user×item 矩阵。

## 困难预评与退回条件

环境轴 E=4/8（中等），优化轴 O=5/8（困难）；O4=2 触发困难。依据：每轮全图多层传播与跨视图目标，并在全部用户/物品上排序；再加完整独立 seed 集，30 分钟低方差比较的可行性尚需 GPU 实测，当前为受控高成本预评。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/lightgcl-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [main.py](https://github.com/HKUDS/LightGCL/blob/5590453ad86782f58017e58d0b698d7f32175be3/main.py)
- [model.py](https://github.com/HKUDS/LightGCL/blob/5590453ad86782f58017e58d0b698d7f32175be3/model.py)
- [parser.py](https://github.com/HKUDS/LightGCL/blob/5590453ad86782f58017e58d0b698d7f32175be3/parser.py)
- [utils.py](https://github.com/HKUDS/LightGCL/blob/5590453ad86782f58017e58d0b698d7f32175be3/utils.py)
