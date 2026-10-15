# 03 · SimMTM：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[SimMTM: A Simple Pre-Training Framework for Masked Time-Series Modeling](https://proceedings.neurips.cc/paper_files/paper/2023/hash/5f9bfdfe3685e4ccdbc0e7fb29cccf2a-Abstract-Conference.html)，NeurIPS 2023。
- 官方仓库：[thuml/SimMTM](https://github.com/thuml/SimMTM)；锁定提交 `169513bef74fb676e48d98a0e30f8823793f691c`。
- 目标范围：分类分支：SleepEEG 无标签预训练 → Epilepsy 小样本迁移；与 TF-C 使用不同方法接口。
- 代码授权：未发现根目录 LICENSE；不随本交接转载上游源码，正式再分发需先解决授权或独立实现。
- 在线查重：2026-10-15，`pass`，最高相似度 0.6061，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

保留 masked-series 相似度学习、邻域加权聚合和逐点重建。源码默认预训练 10 epochs、微调默认 300（run.sh 有 100 的覆盖）；预检明确采用哪套完整配置并冻结，不随 B/R 结果改变。

**主指标及质量门**：Macro-F1 为主，balanced accuracy/各类召回为质量门；类别顺序与阈值冻结。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- 源码 download_datasets.sh：SleepEEG figshare article 19930178 v1；Epilepsy article 19930199 v1。与 TF-C 的 v2 不应静默混用。
- 真实目录是 SimMTM_Classification，README 的 SimMTM_Class 名称过时；数据需放在 dataloader 实际解析路径，逐项记录 tensor shape/标签映射/划分哈希。

- 资源规划：单卡 24GB 起做预检；实测后冻结显存、CPU、内存和磁盘预算。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
cd SimMTM_Classification
python code/main.py --training_mode pre_train --pretrain_dataset SleepEEG --target_dataset Epilepsy
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

Figshare API 已确认所需版本的逐文件名称、大小、下载 URL、MD5 和 CC BY 4.0 标注，见 [资产元数据](../reports/selection/figshare-assets.json)。文件内容尚未下载验证，收到后仍需重新算 SHA256、解析检查和审查原始数据条款。

## 开放方法面：三个独立候选方向

- 掩码生成器：片段/频率结构感知的重建扰动。
- 邻域聚合：样本相似度校准、错误邻居抑制或稀疏权重机制。
- 重建目标：多尺度一致性或重建与迁移特征协同，不只改变损失系数。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- trainer 在预训练中周期性启动下游微调并报告测试最优；改成公开 Dev 选择，私有测试只由独立评测读取。
- 检查 ckp_best 保存对象：正式输出必须包含实际选中微调 encoder 和 classifier，不能只保存原预训练模型；新增独立进程重载评分。
- 原多阶段嵌套成本不能按一个 epoch 估计。预训练与微调均须记入资源预算，不能用同一预训练权重冒充多次独立训练。
- 公开 EEG 数据的受试者/片段来源需要检查；无法重建 subject split 时只声明基准切分表现，不声称跨受试者或临床泛化。

## 困难预评与退回条件

环境轴 E=5/8（困难），优化轴 O=4/8（中等）；E4=2 触发困难。依据：源码预训练中嵌套重新微调和选优，且预训练与微调模型的保存对象不同；需完整贯通两个训练阶段、Dev 选择和正确模型重载。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/simmtm-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [SimMTM_Classification/code/main.py](https://github.com/thuml/SimMTM/blob/169513bef74fb676e48d98a0e30f8823793f691c/SimMTM_Classification/code/main.py)
- [SimMTM_Classification/code/trainer.py](https://github.com/thuml/SimMTM/blob/169513bef74fb676e48d98a0e30f8823793f691c/SimMTM_Classification/code/trainer.py)
- [SimMTM_Classification/code/model.py](https://github.com/thuml/SimMTM/blob/169513bef74fb676e48d98a0e30f8823793f691c/SimMTM_Classification/code/model.py)
- [SimMTM_Classification/code/dataloader.py](https://github.com/thuml/SimMTM/blob/169513bef74fb676e48d98a0e30f8823793f691c/SimMTM_Classification/code/dataloader.py)
- [SimMTM_Classification/download_datasets.sh](https://github.com/thuml/SimMTM/blob/169513bef74fb676e48d98a0e30f8823793f691c/SimMTM_Classification/download_datasets.sh)
- [SimMTM_Classification/run.sh](https://github.com/thuml/SimMTM/blob/169513bef74fb676e48d98a0e30f8823793f691c/SimMTM_Classification/run.sh)
