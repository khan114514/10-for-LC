# 从交接材料到正式运行

## 使用本仓库的修正版 skill

本批交接修正的是 `skills/autoresearch-manager`。先运行仓库根目录的 `python3 tools/verify_handoff.py`，然后读取该目录的 SKILL.md 和 references/runtime-contract.md。接手机器可直接从仓库的绝对路径调用 manager；也可把整个 skill 目录复制到独立版本目录。不要只复制 SKILL.md，运行脚本和固定 QA 资产是必要组成部分。

本次没有覆盖提交者正在使用的全局 skill，也没有改写或恢复任何旧任务。接手已有运行时，应先保持其原始 plan、状态、证据与脚本快照，等安全轮次边界再迁移；保留用户暂停状态和在途任务。新十题使用新 run-dir，不复用旧题状态。

## 准备顺序与停止条件

每题使用三个互不嵌套的目录：作者题目工作目录、主控私有 run-dir、源码/数据获取缓存。另建最小公开 Actor 目录和独立 Verifier 环境。本交接仓库全部是作者材料，禁止整体挂载到 Actor。

先审阅题卡与源码，再下载所需资产。`tools/fetch_source.py` 只取固定源码提交；它不审查或执行上游安装/下载脚本，不提供已经完成数据校验的保证。下载 pickle/pt 后在受控准备环境转换、验证 shape/ID/split，记录下载来源、许可证、哈希和离线镜像。五个无根目录 LICENSE 的源码只能作为定位材料；正式再分发前必须解决授权，或从论文独立实现并复现，不把公开可读等同任意再分发授权。

填写 `templates/preflight.md` 与 `templates/task-contract-draft.json`。后者故意不是可执行 plan；真实的脚本路径、镜像、资产哈希、B/R/U 和分数只有在实测后才能写入运行配置。没有提供返回固定 PASS 的“示例正式 driver”。

依次完成依赖构建、短训练、正确权重保存与新进程重载、完整公共 Dev、健康 B 的多 seed 训练、难度与 headroom 复评。短测只验证管线，不能替代完整 B。若数据不可用、许可不清、没有足够方法空间或修复后不再困难，先修正设计或换题，不启动长轨迹。

## 真实 driver 与模型通路

每个 driver 接收 manager 追加的 `--request /absolute/job/request.json`，在本 job 输出目录写真实 receipt 与证据；具体字段见 runtime-contract。Python 入口脚本必须是存在的绝对路径。脚本源码本身尚未由 manager 自动哈希锁定：应放入不可变发布目录/镜像，合同记录 driver 与镜像哈希，预检核验后再派发，不能在原路径静默改脚本。

按共同要求保持指定 GPT 与 Seed 模型及推理设置。可信主控从本机用户授权配置读取凭据；本机配置路径由接手者指定，不写入版本库、Actor、题包、plan 或日志。所有 Seed/Doubao/Ark 调用只能走火山 Coding Plan `/api/coding/v3/chat/completions`，禁止自动回退按量计费。先实际验证模型、Codex 工具调用、沙箱、评分与网关隔离；套餐不支持指定模型时明确记录阻塞，不替换模型。

`doctor` 的 `configuration: PASS` 只表示配置静态检查通过，`runtime: NOT_YET_VERIFIED` 是预期字段。正式 driver 的训练、远端命令、`python -m`、容器启动与服务可达性都需实测。

## 运行与恢复

按真实 plan 执行 init → doctor → start，使用 status 查看状态；所有参数与路径见 SKILL.md。不在此处放不可用的猜测命令或私人主机地址。恢复先读 state/handoff 和事件，不以聊天摘要代替磁盘证据。

单侧 RETRY/NEEDS_INPUT 只重开该侧，成功侧仍核对 revision、合同与全部证据哈希。plan 或固定 QA 资产恢复后，先收割已结束的原 jobs，不重复启动。任一实质 FAIL 或任务/证据变化进入 repair，新 revision 使旧结果失效。不能靠手改状态、报告或计时进入 DONE。

真正完成要求：合法成对 B/R、两条指定模型各至少 10 个有效研究小时、双方最终方法按当前 SHA 独立复验、当前题包真实 NOP、同实际容器至少 12h 稳定、同一最终 ZIP 的两个独立 AI PASS 且共识无分歧。每题 1–2 天只是规划目标，资源不足时延长或说明阻塞，不删减证据。
