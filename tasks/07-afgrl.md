# 07 · AFGRL：作者侧出题卡

状态：**材料准备完成 / 正式训练未开始**。这份文件含来源和方法方向，不能直接交给 Actor。与上一批 GAD-NR、SoftCLT、RecDCL 不重复。

## 来源与范围

- 正式论文：[Augmentation-Free Self-Supervised Learning on Graphs](https://ojs.aaai.org/index.php/AAAI/article/view/20700)，AAAI 2022。
- 官方仓库：[Namkyeong/AFGRL](https://github.com/Namkyeong/AFGRL)；锁定提交 `95095f4c18a54e2bda3f8a85d5e42fb9a4ce74e7`。
- 目标范围：WikiCS 节点聚类；固定同一图和无监督选择规则。
- 代码授权：未发现根目录 LICENSE；不随本交接转载上游源码，正式再分发需先解决授权或独立实现。
- 在线查重：2026-10-15，`pass`，最高相似度 0.6442，本次疑似阈值 0.8；完整作者侧记录见 [选题报告](../reports/selection/README.md)。只说明该次题库快照未命中，开工须复查。

## 正式 Baseline 和评分合同草案

保留局部邻接一致性、全局聚类正例和 EMA teacher。使用原节点聚类脚本参数、完整训练；不能把聚类正例退化为随机采样作为正式 B。

**主指标及质量门**：固定评估种子集合上的 NMI 均值；ARI 与聚类退化率为质量门。质量门的具体数值必须由论文、独立健康 B 和预检先确定，不能看 Reference 后调整。正式 seed 建议 `[11, 23, 37, 51, 71]`，冻结前确认；至少三次完整独立训练，高方差保留五次。多 case 不能只挑改善的子集。

B/R/U 和归一化公式在实测 B 后冻结；当前没有虚构分数、时长、提升或 Reference。B 与 R 共享依赖、数据修复和计算预算，遵循 [共同要求](../requirements/common.md)。

## 资产与环境准备

- PyG WikiCS 公共资产；分别锁图预处理与聚类评估 seed。
- 依赖 PyTorch/PyG/FAISS；上游旧版本需预先在 Linux GPU 环境编译验证。

- 资源规划：先申请单卡 24GB、CPU 内存至少 32GB 进行容量预检；这是规划值，不是已验证最低需求。单次耗时与全流程总成本均未实测，不承诺一天完成。
- 先构建 Linux GPU 容器并做训练、保存、重载、评分短测；将 CUDA/框架/扩展 wheel 的实际版本和镜像 digest 写入 preflight 记录。
- 资产获取、原始文件字节数与 SHA256、数据条款、完整度和离线运行检查由接手作者完成；本仓库不包含数据和上游权重。

上游入口（只作定位，尚不是完成隔离改造后的正式 driver）：

```bash
python main.py --dataset wikics --embedder AFGRL --task clustering --layers '[1024]' --pred_hid 2048 --lr 0.001 --topk 8 --device 0 --mad 0.9
```

脚本内工作目录、参数解析与真实数据位置以上述固定提交为准。不要直接批量执行未审查的上游脚本；正式 argv 与输出目录须通过预检后写入合同。

## 开放方法面：三个独立候选方向

- 局部与全局正例的交集/软一致性判定。
- 聚类置信度驱动的正样本挖掘，避免错误正例扩散。
- teacher 表征与邻域更新策略，保证不读取隐藏标签。

这些是作者侧研究假设，不保证改善。给 Actor 的接口应接受函数/模块/策略替换；保留公共 Dev、文档和合法 starter，但删去论文名、官方答案链接和上述 Reference 思路。至少做单因素对照并保留失败结果；参数网格搜索不能替代方法研究。

## 已发现的共同修复与风险

- Neighbor.forward 构造稠密相似矩阵并重复 CPU FAISS KMeans；先测峰值内存和训练耗时，不能仅按 GPU 显存推断可行性。
- 源码顶层固定 seed；改为显式训练 seed 和聚类 seed，并记录每次独立初始化。
- 训练和 checkpoint 选择不得读节点标签；无监督训练目标选择规则预先冻结。最终评测 KMeans 多 seed 不能冒充多次 encoder 训练。

## 困难预评与退回条件

环境轴 E=4/8（中等），优化轴 O=5/8（困难）；O4=2 触发困难。依据：官方实现同时构造 N×N 相似度并在训练过程中反复执行 CPU KMeans；两条信号支持 30 分钟内稳定单变量结论可能困难，尚未实测，若实测不成立必须降级或换题。

置信度为中；O3 消融/失败材料未逐项充分验证，按缺失默认 1 处理。[分项原始结果](../reports/selection/afgrl-difficulty.json) 保存评分依据。复杂故障本身不算可取的方法难度：修复后重新评估，若只剩简单调参、短测已经饱和或没有真实改善空间，就更换题目，不能用故障或弱 B 凑困难。

## 接手后的第一轮交付

1. 按固定提交获取源码和上述资产；完成授权与完整性核验，生成独立 preflight 记录。
2. 完成共同修复，冻结 split/预处理/seed/资源/接口/选优/指标，跑健康 B、独立重载与完整 Dev 评分。
3. 复评困难、可复现性和方法 headroom；确认合格再制作 Reference 与 Harbor 题包，执行完整 manager 流程。训练题每条双轨至少 10 个有效研究小时；最终同容器稳定至少 12 小时；相同 ZIP 两个独立 AI PASS。

## 已核对的代码入口

- [models/AFGRL.py](https://github.com/Namkyeong/AFGRL/blob/95095f4c18a54e2bda3f8a85d5e42fb9a4ce74e7/models/AFGRL.py)
- [main.py](https://github.com/Namkyeong/AFGRL/blob/95095f4c18a54e2bda3f8a85d5e42fb9a4ce74e7/main.py)
- [run_node_clustering.sh](https://github.com/Namkyeong/AFGRL/blob/95095f4c18a54e2bda3f8a85d5e42fb9a4ce74e7/run_node_clustering.sh)
- [embedder.py](https://github.com/Namkyeong/AFGRL/blob/95095f4c18a54e2bda3f8a85d5e42fb9a4ce74e7/embedder.py)
