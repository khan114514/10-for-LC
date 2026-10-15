# 01 · ConsisGAD：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[Consistency Training with Learnable Data Augmentation for Graph Anomaly Detection with Limited Supervision](https://proceedings.iclr.cc/paper_files/paper/2024/hash/80eecea10dc05e23db2f90c9d4567153-Abstract-Conference.html)，ICLR 2024。
- 官方仓库：[Xtra-Computing/ConsisGAD](https://github.com/Xtra-Computing/ConsisGAD)；锁定提交 `36811c5bc79be49c9740f25a1f260496bb4736af`。
- 目标范围：Amazon 主任务；YelpChi 作为固定第二场景，分别冻结有限标签比例与切分。
- 代码授权：MIT（代码）；数据使用条款另外核对。
- 在线查重：2026-10-15，`pass`，最高相似度 0.5455，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

保留完整关系图骨干、可学习增强器和一致性训练。Amazon 原配置 100 epochs、每轮 128 次训练迭代；训练是否充分由曲线和真实 steps 核验。

**主指标及质量门**：ROC-AUC 为主、PR-AUC 和少数类召回为质量门；先冻结阈值选择规则。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- DGL 自带 FraudAmazonDataset/FraudYelpDataset；官方来源见固定版本 README。预取数据后保存原包、处理结果和切分 SHA256；不得把私有标签交给 Actor。

- 资源规划：单卡 24GB 起做预检；实测后冻结显存、CPU、内存和磁盘预算。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
python main.py --config 'config/amazon.yml' --runs 5
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- SoftAttentionDrop：特征/关系条件化增强分布，改变噪声生成机制；保留完整信息预算。
- UDA_train_epoch：置信度校准与一致性样本选择，修改目标和选择策略。
- simpleGNN_MR：异配关系下的邻居聚合或消息门控，必须是模块实现。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- 原训练同时访问验证与测试 loader；改成训练仅可见独立 Dev，最终测试由 Verifier 执行。
- 把配置中的 GPU 序号改成容器内设备映射；两边相同。多次运行必须重新初始化模型、优化器、增强器和 RNG。
- 记录标签比例、标签采样 seed、图边可见范围；无标签节点特征可见性须预先约定。

## 困难预评与退回条件

环境轴 E=5/8（困难），优化轴 O=4/8（中等）；E4=2 触发困难。依据：两个可训练部分与一致性/监督目标共同更新；稀标签关系图的采样、验证选优和独立权重重载必须一致，完整闭环有多处状态耦合。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/consisgad-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [main.py](https://github.com/Xtra-Computing/ConsisGAD/blob/36811c5bc79be49c9740f25a1f260496bb4736af/main.py)
- [models.py](https://github.com/Xtra-Computing/ConsisGAD/blob/36811c5bc79be49c9740f25a1f260496bb4736af/models.py)
- [config/amazon.yml](https://github.com/Xtra-Computing/ConsisGAD/blob/36811c5bc79be49c9740f25a1f260496bb4736af/config/amazon.yml)
- [config/yelp.yml](https://github.com/Xtra-Computing/ConsisGAD/blob/36811c5bc79be49c9740f25a1f260496bb4736af/config/yelp.yml)
- [requirements.txt](https://github.com/Xtra-Computing/ConsisGAD/blob/36811c5bc79be49c9740f25a1f260496bb4736af/requirements.txt)
- [modules/data_loader.py](https://github.com/Xtra-Computing/ConsisGAD/blob/36811c5bc79be49c9740f25a1f260496bb4736af/modules/data_loader.py)
