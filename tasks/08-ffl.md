# 08 · Focal Frequency Loss

状态：**PREPARATION_ONLY · 中等预评**，E=4/8，O=4/8，置信度中。未完成目标 GPU 训练、Reference 改善或正式验收。

## 来源与本题范围

- 论文：[完整正式标题](https://openaccess.thecvf.com/content/ICCV2021/html/Jiang_Focal_Frequency_Loss_for_Image_Reconstruction_and_Synthesis_ICCV_2021_paper.html)：Focal Frequency Loss for Image Reconstruction and Synthesis（ICCV 2021）。
- 官方源码：[EndlessSora/focal-frequency-loss](https://github.com/EndlessSora/focal-frequency-loss/tree/352f69da503f55267d8c148da04ea625ed1c9552)，固定提交 `352f69da503f55267d8c148da04ea625ed1c9552`。
- 代码许可：MIT（根许可证；捆绑组件和数据条款分别核验）。
- 范围：**CIFAR-10 32×32 图像重建；官方 MLP 自编码器 + FFL**。适配类型 `NEW_DATASET_ADAPTER_REQUIRED`。
- 主指标：逐图 PSNR（[0,1]、data_range=1）宏平均，越高越好；SSIM 为质量门。不以可修改训练 loss 自评。

## 健康 Baseline

采用官方 VanillaAE 的 MLP（不是卷积 AE），输入/输出 3072、nz 256、nblk 2，完整像素 MSE+FFL。权重/训练长度在公开 Dev 上用可比机会选择健康配置，不能删 FFL 或压低训练。CIFAR 是新任务适配，不能引用 CelebA 表中分数作本题 B。

## 数据准备与切分

- CIFAR-10 官方 50,000 train / 10,000 test，32×32 RGB；训练内固定 45,000/5,000 train/Dev。
- 优先二进制版，逐条校验 label+3072 bytes，导出 PNG/filelist 或等价只读 loader；图像 identity 及切分哈希冻结。此轮未下载完整 CIFAR。

资产入口：[入口 1](https://www.cs.toronto.edu/~kriz/cifar.html).

## 代码入口与启动依据

VanillaAE/train.py 原生接受 filelist/folderall；先做 CIFAR 解码和 filelist 适配，imageSize=32。官方 CelebA 脚本不能直接当本题已验证命令。

- [VanillaAE/models.py](https://github.com/EndlessSora/focal-frequency-loss/blob/352f69da503f55267d8c148da04ea625ed1c9552/VanillaAE/models.py)
- [VanillaAE/networks.py](https://github.com/EndlessSora/focal-frequency-loss/blob/352f69da503f55267d8c148da04ea625ed1c9552/VanillaAE/networks.py)
- [VanillaAE/train.py](https://github.com/EndlessSora/focal-frequency-loss/blob/352f69da503f55267d8c148da04ea625ed1c9552/VanillaAE/train.py)
- [VanillaAE/data.py](https://github.com/EndlessSora/focal-frequency-loss/blob/352f69da503f55267d8c148da04ea625ed1c9552/VanillaAE/data.py)
- [VanillaAE/utils.py](https://github.com/EndlessSora/focal-frequency-loss/blob/352f69da503f55267d8c148da04ea625ed1c9552/VanillaAE/utils.py)
- [focal_frequency_loss/focal_frequency_loss.py](https://github.com/EndlessSora/focal-frequency-loss/blob/352f69da503f55267d8c148da04ea625ed1c9552/focal_frequency_loss/focal_frequency_loss.py)
- [scripts/VanillaAE/train/celeba_recon_w_ffl.sh](https://github.com/EndlessSora/focal-frequency-loss/blob/352f69da503f55267d8c148da04ea625ed1c9552/scripts/VanillaAE/train/celeba_recon_w_ffl.sh)

## 三个方法改动面（作者侧候选，收益未验证）

1. 频率权重：分布稳健或误差历史条件化的频率加权函数。
2. 频率表示：多尺度局部频谱分解，保持空间重建对象不变。
3. 目标组合：按频段校准像素/频谱梯度或约束一致性，而非只改 alpha/ffl_w。

## 制作前必须完成的适配

- 训练循环只按 epoch 保存 checkpoint，没有 Dev 选优；新增共享 Dev PSNR 选优和新进程重载。
- 统一 [-1,1] 网络输入/输出到 [0,1] 评测的变换、裁剪和 SSIM 参数，防止利用尺度拿分。
- 冻结 MLP 架构与信息瓶颈，禁止 identity bypass；训练用输入本身作重建标签是任务定义，禁止查表或 memorized private 图像。

## 中等预评与开工门槛

一个自编码器、一个优化器的监督重建；需要数据 filelist 和 Dev 选优适配，评分可直接从重建图复算。 单卡预检；32×32 MLP 重建，不引入 GAN、扩散、预训练感知模型或 FID 网络。

[八维评级记录](../reports/selection/ffl-difficulty.json)按原动态 PE 规则计算；O3/O4 是缺证默认项，不是实验证明。若健康 B 的完整训练、方法空间或 30min 实验实测触发困难，换题或重新设计并重新评级，不能保持旧标签。

先完成真实依赖构建、全量 Dev、充分训练 B、checkpoint 新进程重载、成本与方差测量，再冻结 B/R/U。默认至少 3 次独立训练，高方差至少 5 次；全部配对原始值保留。G03、10h 双轨、当前 SHA 复验、NOP、12h 稳定性与同 ZIP 双 AI PASS 仍按[共同要求](../requirements/common.md)。

本题卡含论文答案、源码入口和作者方向，只供作者使用；不能进入 Actor 环境或正式公开 instruction。
