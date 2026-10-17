# 中等批次选题证据

本批 2026-10-17 按用户最新要求重新选十道，替换当前主目录的困难批次；旧材料保留在 Git 提交 [6370c57](https://github.com/khan114514/10-for-LC/tree/6370c579ee299e3346ff57d0997fc1a2ed7422bf)。没有把旧题直接改名或改评级。

从 29 个候选中筛选，排除在线 duplicate/suspect、未证实顶会来源及本轮迁移负担较大的方向。[排除记录](screening.json)。最终十题以正式题名与链接在线复查，全部 pass；批次 `20261017_165105`，题库快照 5610 条，构建时间 2026-10-09T10:57:07。[原服务响应](dedup.json)保留最相似 ID、相似度和当次阈值。查重 pass 不等于平台正式收录，开工须重新查当期库。

使用当次拉取的动态规则（revision 2026-09-28，服务器标识 a0674a53），调用原版 difficulty_pe、venue_check 和在线 check_dedup。临时规则包不入仓库，用后删除。本目录只属于作者审核侧，不能进入题包、镜像、日志或 Actor 运行环境。

十题均按**所列小任务范围**计算 E=4、O=4，整题中等，置信度中。E1–E4/O1–O2 每项 1 分，逐题理由见各 JSON；O3（完整消融/失败证据）和 O4（30min 低方差实验）未核实，按规则缺失默认 1 分。相同总分只说明当前证据落在相同区间，并不说明实际成本相同。GPU 完整训练、峰值显存、方差和改善余量都没有实测。若实测严重项为 2 或触发其他困难规则，应从本中等批次移除，不降分凑档。

降低复杂度的依据是固定一个小数据/短窗口或两张小图、单阶段训练、明确方法接口，保留完整健康 B。NODE 需要 notebook→CLI；DANet/FFL 需要新数据适配，均在卡中显式标注。其余为官方原生小基准分支。不运行论文全部 HPO、迁移或攻击实验，不宣称复现整篇论文。FT-Transformer/MLP-PLR、ACM-GCN/EvenNet、三道预测题通过不同冻结/开放接口区分，不能制作成同一任务换标题。

正式出处、固定源码提交和逐文件内容哈希见 [sources.json](../../manifests/sources.json)。venue.json 是字段分类，不单独证明发表。DANet/NeurIPS/Leddam 正式页面已核对；RevIN/MICN 的 OpenReview 受阻时，用固定提交的官方 README 接受说明交叉核对；NODE 另查 [ICLR 2020 官方论文列表](https://iclr.cc/virtual_2020/papers.html?filter=authors&search=Stanislav+Morozov)，FFL 获得 CVF 官方索引的会议/页码，并与 README 核对。Leddam 另有 [ICML PMLR 正式页面](https://proceedings.mlr.press/v235/yu24s.html)，在线查重保留原 OpenReview 链接以维持请求可追溯。

[ETT 资产记录](ett-assets.json)含固定提交的 ETTh1/ETTh2 实际下载字节、SHA256、行数、列和时间范围，仅证明 CSV 内容可取，不代表切分/训练已验证。其他数据仅定位官方入口，未全量下载或解析。代码/数据许可证分开核验，EvenNet/MICN 未发现根目录许可证，本仓库不转载其实现。

建议先做 RevIN、MLP-PLR、Leddam 的预检；DANet/FFL 先完成数据适配，NODE 先固化 CLI，EvenNet/MICN 先处理分发授权。正式全流程的证据门槛保持不变。
