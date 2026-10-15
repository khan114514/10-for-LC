# 02 · TimeSiam：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[TimeSiam: A Pre-Training Framework for Siamese Time-Series Modeling](https://proceedings.mlr.press/v235/dong24e.html)，ICML 2024。
- 官方仓库：[thuml/TimeSiam](https://github.com/thuml/TimeSiam)；锁定提交 `c06f05df6197af0d780fae16b272ee4bd7d54ed9`。
- 目标范围：ETTh1 + ETTh2；PatchTST 编码器；预测长度 96/192/336/720，预训练后分别微调。
- 代码授权：MIT（代码）；数据使用条款另外核对。
- 在线查重：2026-10-15，`pass`，最高相似度 0.595，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

保留时间配对、lineage embedding 和 Siamese reconstruction 的完整 TimeSiam；示例预训练 50 epochs 后四个 horizon 微调。每个训练 seed 从初始化预训练，再派生各 horizon。

**主指标及质量门**：八个固定 dataset×horizon case 的 MSE 均值（越低越好）；各 case MAE 为质量门。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- 官方 README 的 Google Drive/Tsinghua 数据镜像；目标文件 dataset/ETT-small/ETTh1.csv、ETTh2.csv。也可从[原始 ETT 作者仓](https://github.com/zhouhaoyi/ETDataset/tree/main/ETT-small)获取，但必须验证内容一致并冻结哈希。
- 无需现成论文 checkpoint；正式 B/R 从头预训练，公开下载权重只可作独立 smoke 对照。

- 资源规划：单卡 24GB 起做预检；实测后冻结显存、CPU、内存和磁盘预算。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
bash scripts/TimeSiam/ETT_script/PatchTST_ETTh1.sh
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- 时间配对采样：依赖跨度、周期性或难度的采样机制。
- Lineage 表征：离散/连续时间距离编码与融合模块。
- 掩码重建：跨分支信息融合或预测目标形式，不只改 mask 比例。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- 严格按时间切分，标准化只拟合训练段；窗口和目标不能穿越切分边界。
- 预训练只读训练段；逐项记录 checkpoint→微调→评测血缘，禁止共享跨 seed 的预训练权重充当独立训练。
- 脚本含多个命令，必须收集每个子命令退出码并实现失败即停，不能以最后一个子命令成功掩盖先前失败。

## 困难预评与退回条件

环境轴 E=5/8（困难），优化轴 O=4/8（中等）；E4=2 触发困难。依据：预训练权重迁移到多个微调模型，再汇总八个未来时间预测 case；时间边界和各模型 checkpoint 血缘共同决定指标有效性。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/timesiam-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [exp/pretrain.py](https://github.com/thuml/TimeSiam/blob/c06f05df6197af0d780fae16b272ee4bd7d54ed9/exp/pretrain.py)
- [models/PatchTST.py](https://github.com/thuml/TimeSiam/blob/c06f05df6197af0d780fae16b272ee4bd7d54ed9/models/PatchTST.py)
- [data_provider/data_loader.py](https://github.com/thuml/TimeSiam/blob/c06f05df6197af0d780fae16b272ee4bd7d54ed9/data_provider/data_loader.py)
- [scripts/TimeSiam/ETT_script/PatchTST_ETTh1.sh](https://github.com/thuml/TimeSiam/blob/c06f05df6197af0d780fae16b272ee4bd7d54ed9/scripts/TimeSiam/ETT_script/PatchTST_ETTh1.sh)
- [scripts/TimeSiam/ETT_script/PatchTST_ETTh2.sh](https://github.com/thuml/TimeSiam/blob/c06f05df6197af0d780fae16b272ee4bd7d54ed9/scripts/TimeSiam/ETT_script/PatchTST_ETTh2.sh)
- [requirements.txt](https://github.com/thuml/TimeSiam/blob/c06f05df6197af0d780fae16b272ee4bd7d54ed9/requirements.txt)
