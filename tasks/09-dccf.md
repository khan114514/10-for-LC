# 09 · DCCF：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[Disentangled Contrastive Collaborative Filtering](https://doi.org/10.1145/3539618.3591665)，SIGIR 2023。
- 官方仓库：[HKUDS/DCCF](https://github.com/HKUDS/DCCF)；锁定提交 `c9bcac4fee2e15d1a02a1396470b3ec29b5177d1`。
- 目标范围：Tmall 全物品推荐；从原 train 冻结独立 Dev。
- 代码授权：未发现根目录 LICENSE；不随本交接转载上游源码，正式再分发需先解决授权或独立实现。
- 在线查重：2026-10-15，`pass`，最高相似度 0.7339，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

完整 DCCF：潜在意图表征、自适应图增强、多个视图的对比与推荐损失。官方 Tmall 命令 100 epochs 并使用最终 epoch；作者先验证该规则健康，B/R 共用冻结选择策略。

**主指标及质量门**：Recall@20 为主、NDCG@20 为质量门；固定全物品候选与交互过滤。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- 固定源码 data/tmall 的 train/test pickle 与索引文件；README 说明 Tmall/Gowalla 已将 validation 并入 train。
- 重新切出 Dev 后重建所有派生索引和归一化邻接；切分不能在后续搜索中变化或再次并回训练。

- 资源规划：单卡 24–48GB 作为预检范围；若完整 Tmall 超限，冻结前改预算或换题，不能正式阶段只缩短 B。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
python DCCF_PyTorch.py --dataset tmall --epoch 100
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- 意图分解与分配约束，避免意图坍缩。
- 意图条件化的图边权/视图构造策略。
- 跨意图/跨视图对比目标与负样本选择，保持相同监督信息。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- 新 Dev 的全部交互必须从训练图和派生缓存移除；原 README 的合并流程不可沿用到研究迭代。
- 顶层固定 seed 改为显式成对 seed；每次从头训练并保存最终模型，而非重测一次模型。
- 完整记录四类视图的内存峰值和全物品排名耗时；内存修复 B/R 同享。

## 困难预评与退回条件

环境轴 E=4/8（中等），优化轴 O=5/8（困难）；O4=2 触发困难。依据：全图意图分解、多视图 SSL 和全物品排序同时存在；跨 seed 的低方差改善不能由单次短测证明，30 分钟闭环困难属于待实测的受控推断。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/dccf-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [DCCF_PyTorch.py](https://github.com/HKUDS/DCCF/blob/c9bcac4fee2e15d1a02a1396470b3ec29b5177d1/DCCF_PyTorch.py)
- [model.py](https://github.com/HKUDS/DCCF/blob/c9bcac4fee2e15d1a02a1396470b3ec29b5177d1/model.py)
- [utility/parser.py](https://github.com/HKUDS/DCCF/blob/c9bcac4fee2e15d1a02a1396470b3ec29b5177d1/utility/parser.py)
