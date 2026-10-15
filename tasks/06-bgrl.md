# 06 · BGRL：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[Large-Scale Representation Learning on Graphs via Bootstrapping](https://openreview.net/forum?id=0UXT6PpRpW)，ICLR 2022。
- 官方仓库：[nerdslab/bgrl](https://github.com/nerdslab/bgrl)；锁定提交 `60f9f19ad0598f9163ad70ebbde3e7297760901e`。
- 目标范围：PPI inductive multi-label 节点表征学习；不以 WikiCS 替代正式任务。
- 代码授权：Apache-2.0（代码）；数据使用条款另外核对。
- 在线查重：2026-10-15，`pass`，最高相似度 0.6721，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

完整 online encoder、predictor、EMA target 和双图增强。PPI 配置 10,000 steps、batch=22、每 1,000 steps 原评估一次；最终训练充分性以曲线和实际步数审查。

**主指标及质量门**：micro-F1，固定独立线性评估器；逐图结果与少数标签覆盖作为质量检查。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- torch_geometric.datasets.PPI 原生公开数据，缓存原包、图边/特征/标签和官方 train/val/test 图划分。
- 上游 PyTorch 1.9.1 / PyG 扩展组合较旧；容器需锁兼容 wheel，而非运行时临时安装。

- 资源规划：单卡 24GB 起做预检；实测后冻结显存、CPU、内存和磁盘预算。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
python3 train_ppi.py --flagfile=config/ppi.cfg
python3 linear_eval_ppi.py --flagfile=config-eval/ppi.cfg
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- 拓扑/特征联合视图生成，避免损毁稀疏标签对应结构。
- predictor 与 online/target 表征匹配目标。
- EMA 更新或正样本一致性机制，改动必须影响方法而非单个系数。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- 源码预训练把 train 和 val 的无标签图合并；正式协议明确允许范围，不能包含 private-test 图。若 Dev 图要求隔离，两边共同移出。
- 定期线性评估暴露 test 指标，改成 Dev；测试由隔离评测器读取。
- PPI 保存文件名沿用 bgrl-wikics.pt，统一修正命名并核验实际 payload、编码器结构和线性评估器一致。

## 困难预评与退回条件

环境轴 E=5/8（困难），优化轴 O=4/8（中等）；E4=2 触发困难。依据：跨多个独立图训练 online/target 编码器，并用单独多标签评估器得到最终指标；预训练图集合与评估图集合、两类 checkpoint 均需一致绑定。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/bgrl-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [train_ppi.py](https://github.com/nerdslab/bgrl/blob/60f9f19ad0598f9163ad70ebbde3e7297760901e/train_ppi.py)
- [linear_eval_ppi.py](https://github.com/nerdslab/bgrl/blob/60f9f19ad0598f9163ad70ebbde3e7297760901e/linear_eval_ppi.py)
- [config/ppi.cfg](https://github.com/nerdslab/bgrl/blob/60f9f19ad0598f9163ad70ebbde3e7297760901e/config/ppi.cfg)
- [config-eval/ppi.cfg](https://github.com/nerdslab/bgrl/blob/60f9f19ad0598f9163ad70ebbde3e7297760901e/config-eval/ppi.cfg)
- [bgrl/bgrl.py](https://github.com/nerdslab/bgrl/blob/60f9f19ad0598f9163ad70ebbde3e7297760901e/bgrl/bgrl.py)
