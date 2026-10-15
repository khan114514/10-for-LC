# 04 · TF-C：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[Self-Supervised Contrastive Pre-Training for Time Series via Time-Frequency Consistency](https://proceedings.neurips.cc/paper_files/paper/2022/hash/194b8dac525581c346e30a2cebe9a369-Abstract-Conference.html)，NeurIPS 2022。
- 官方仓库：[mims-harvard/TFC-pretraining](https://github.com/mims-harvard/TFC-pretraining)；锁定提交 `96675826e9ef234a9b01cc63d484c66cb0441bc0`。
- 目标范围：SleepEEG 无标签预训练 → Epilepsy 小样本分类；时间与频率双编码器。
- 代码授权：MIT（代码）；数据使用条款另外核对。
- 在线查重：2026-10-15，`pass`，最高相似度 0.585，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

保留时间、频率双编码器、各自增强和跨域一致性目标；下游分类器独立训练。完整训练轮数由官方配置与真实收敛预检共同确认，两边共用。

**主指标及质量门**：Macro-F1 为主，balanced accuracy/各类召回为质量门；类别和小样本预算冻结。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- download_datasets.sh：SleepEEG https://figshare.com/ndownloader/articles/19930178/versions/1；Epilepsy https://figshare.com/ndownloader/articles/19930199/versions/2。
- 下载清单覆盖多个数据集；此题只准备上述两项，不运行无关下载。SleepEEG 规模约 37 万样本，成本需实际计时。

- 资源规划：单卡 24GB 起做预检；实测后冻结显存、CPU、内存和磁盘预算。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
cd code/TFC
python main.py --training_mode pre_train --pretrain_dataset SleepEEG --target_dataset Epilepsy
python main.py --training_mode fine_tune_test --pretrain_dataset SleepEEG --target_dataset Epilepsy
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

Figshare API 已确认所需版本的逐文件名称、大小、下载 URL、MD5 和 CC BY 4.0 标注，见 [资产元数据](../reports/selection/figshare-assets.json)。文件内容尚未下载验证，收到后仍需重新算 SHA256、解析检查和审查原始数据条款。

## 开放方法面：三个独立候选方向

- 频率增强：保相位/频段结构的扰动策略。
- 时频一致性：跨域对齐目标、正负样本选择和坍缩防护。
- 双分支融合：按样本或频带条件化融合，保留训练和推理接口。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- trainer 的 valid_dl 实际用于优化，不能按变量名把它当 Dev；重建明确的 target-train/Dev/private-test 语义。
- 源码每轮测试并报告最佳 F1/KNN；全部选择改为 Dev，不能在私有集挑 epoch、分类头或 KNN 设置。
- 固定保存两套 encoder、projection、classifier 及预处理参数，独立重载；官方预训练权重不替代正式独立训练。
- 处理后数据不保证可追溯受试者划分；验收明确为固定公共 benchmark，不能宣称临床效果。

## 困难预评与退回条件

环境轴 E=5/8（困难），优化轴 O=4/8（中等）；E4=2 触发困难。依据：两个编码器的预训练、迁移分类头和多种评估路径耦合；源码 loader 角色与命名不一致，必须实现可信划分、权重迁移和独立重载闭环。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/tfc-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [code/TFC/main.py](https://github.com/mims-harvard/TFC-pretraining/blob/96675826e9ef234a9b01cc63d484c66cb0441bc0/code/TFC/main.py)
- [code/TFC/trainer.py](https://github.com/mims-harvard/TFC-pretraining/blob/96675826e9ef234a9b01cc63d484c66cb0441bc0/code/TFC/trainer.py)
- [code/TFC/model.py](https://github.com/mims-harvard/TFC-pretraining/blob/96675826e9ef234a9b01cc63d484c66cb0441bc0/code/TFC/model.py)
- [code/TFC/dataloader.py](https://github.com/mims-harvard/TFC-pretraining/blob/96675826e9ef234a9b01cc63d484c66cb0441bc0/code/TFC/dataloader.py)
- [download_datasets.sh](https://github.com/mims-harvard/TFC-pretraining/blob/96675826e9ef234a9b01cc63d484c66cb0441bc0/download_datasets.sh)
- [code/config_files/SleepEEG_Configs.py](https://github.com/mims-harvard/TFC-pretraining/blob/96675826e9ef234a9b01cc63d484c66cb0441bc0/code/config_files/SleepEEG_Configs.py)
- [code/config_files/Epilepsy_Configs.py](https://github.com/mims-harvard/TFC-pretraining/blob/96675826e9ef234a9b01cc63d484c66cb0441bc0/code/config_files/Epilepsy_Configs.py)
