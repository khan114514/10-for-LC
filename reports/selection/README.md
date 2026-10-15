# 选题证据与当前结论

2026-10-15 从新候选集中选出十项，排除上一批三题。以正式题名和正式发表链接再次在线查重，十项全部 pass，无 suspect/duplicate。批次 `20261015_220319`，题库快照 5610 条、构建于 2026-10-09；阈值来自本次服务器响应，不作为未来固定值。逐题最相似记录 ID 和相似度见 [dedup.json](dedup.json)。ID `adagcl` 在请求中拼为 `adacgl`，论文题名及链接不变，映射明确保留。

会议分类脚本接受十篇的明确顶会字段，且人工核对正式论文页面/作者官方仓库。`venue.json` 是分类记录，不单独构成论文存在证据；正式链接与固定源码提交见 ../../manifests/sources.json。AdaGCL 是 KDD 2023，AFGRL 的正式题名是 Augmentation-Free Self-Supervised Learning on Graphs，已更正后重查。

本次先获取当期动态规则，版本 2026-09-28、服务器标识 `a0674a53`；调用原规则附带的 venue_check、difficulty_pe、在线 check_dedup。该规则包是临时审核材料，未收入仓库。此目录仍属于作者侧审核物料，不能进入题包、镜像、Actor 日志或运行环境。

十题均给出八维 PE 分数；环境复杂的多阶段任务由 E4=2 触发困难，AFGRL/LightGCL/DCCF 由代码成本信号支持 O4=2 的受控推断。所有难度是预评，O3 默认缺失，置信度中。尚未完整验证论文消融与失败证据、目标 GPU 成本、30 分钟单变量实验方差以及 Reference 的显著改善。不能把缺失、实现故障或人为放大预算当作难度；预检后复评不达标即换题。

代码读取固定提交的训练入口、模型、配置和数据加载路径，未执行上游代码、未解包 pickle/tensor、未声称数据已经下载。检查足以定位制作入口和风险，不等同十题端到端复现。数据镜像失效、条款不允许再分发、依赖无法构建或预算内无法充分训练时，应在开工前解决或换题。

建议先验证 MIT/Apache 授权清晰的 ConsisGAD、TimeSiam、GraphMAE2、BGRL、TF-C；其余五项并行做作者侧授权与资产确认后再开工。不得因此缩减完整方法或正式验收要求。

额外对五个数据/簇入口做 HTTP HEAD，见 [asset-endpoints.json](asset-endpoints.json)：Figshare 返回 202，Tsinghua 返回 HTML 页面，这些响应不证明数据可完整下载。不能把 HTTP 成功码当成资产验证通过；目标机仍需获取真实文件并校验。

进一步读取 Figshare 版本 API，已取得 SleepEEG v1 与 Epilepsy v1/v2 的逐文件元数据（共 9 个版本化文件记录），包括直接下载链接、字节数、发布方 MD5 和 CC BY 4.0 标注，见 [figshare-assets.json](figshare-assets.json)。这解决聚合下载入口仅返回 202 的定位问题，仍不代表文件内容已验证。
