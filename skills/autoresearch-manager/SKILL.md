---
name: autoresearch-manager
description: 持续管理 AutoResearch 全流程，包括成对 B/R、独立双轨、当前 SHA 复验、NOP、12h 稳定性、独立双 AI 质检和失败修正，直到同一最终 ZIP 获得两个 PASS。支持持久化状态、后台任务和自动新会话交接；用于执行管理，不替代独立 QA。
---

# AutoResearch 自动管理

用户授权的目标是失败后持续修正，直到同一最终 ZIP 的两个独立质检均 PASS 且共识无分歧。不设固定修复轮数，不因失败多次或上下文不足结束任务。不能降低验收要求、改评分锚点制造提升、修改 QA 规则或伪造证据取得 PASS。

## 当前合同与路由

随附已核验的 `autoresearch-qa-skills/0.3.4`，位于 `assets/qa-skills/`，来源与 SHA256 在 `assets/qa-release.json`，比旧安装的 v0.3.2 新。每个新任务核对用户当前权威规则；当前执行冻结版本，更新规则须建立新合同并失效受影响证据，不能中途静默换规则。

豆包/Ark/Seed 只使用火山 Coding Plan：`https://ark.cn-beijing.volces.com/api/coding/v3/chat/completions`。可信主控在安全调用边界从用户当前配置读取凭据；不把 key 放入 plan、request、日志、题包或 Actor 环境。Codex + Seed 必须通过已实测的兼容网关使用指定模型，不能用普通聊天代替 Codex 轨迹，不能回退按量 `/api/v3`。指定模型/推理级别不支持时保持未完成并报告。

## 启动与续接

先读 [运行合同](references/runtime-contract.md)。基于指定任务的实际 Harbor/provider/隔离和真实命令建立 plan，不能套用其他题路径。用户没指定题目时完成管理 skill 和执行器，不擅自恢复旧题、已暂停任务或开启10h实验。

批量选题或交接准备与正式实验是两种范围。仅要求选题、准备材料或修改 Skill 时，交付作者侧题目要求、固定源码清单、数据入口、预检步骤和明确待验证项；不要启动每题10h轨迹。开工前重新获取平台自选题规则，按完整正式题名与正式链接查重；难度预评必须附论文/代码依据，不能将目标“困难”写成已认证结果。

```sh
python3 scripts/manager.py init --plan /absolute/private/plan.json --run-dir /absolute/private/manager-run
python3 scripts/manager.py doctor --run-dir /absolute/private/manager-run
python3 scripts/manager.py start --run-dir /absolute/private/manager-run
python3 scripts/manager.py status --run-dir /absolute/private/manager-run
```

顺序：prepare → br → preflight_nop → dual（两条隔离任务）→ finalize（两条最终 SHA 各自独立复验）→ nop → stability → package → 两个独立 QA → 原版共识聚合。失败自动进入 repair，再从 prepare 验证新版本；默认全量失效，不将旧版本PASS或运行证据拼到新版本。repair 使用新会话，读取当前问题和磁盘状态，做实质修改。

`start` 启动脱离当前对话的后台进程。`tick` 推进一步；`run` 前台持续调度。`pause` 暂停新派发，保留在途进程和产物；用户明确要求时 `resume`。`status` 不改变暂停状态。凭据、模型或授权缺失显示 NEEDS_INPUT，不标完成；补齐后续接原任务。

双轨或双 QA 单侧 RETRY/NEEDS_INPUT 时，先保存成功侧的原始回执及证据哈希，仅重试未成功侧。每次续接仍核验同 revision、合同、任务与证据；内容变化则进入 repair，新 revision 全量失效。已结束但被打断的失败尝试保留原始目录。doctor 只检配置，不能代替模型工具调用、隔离、真实训练与 Harbor 运行预检；Python driver 使用绝对脚本路径，两个审查者必须是不同模型，不能靠版本或 provider 别名凑数。

## 上下文与独立会话

调度器保存 state、事件、每次request、进程退出状态和产物哈希。每次stage/repair是独立调用，判断从磁盘恢复。`agent_stage.py` 使用新的 `codex exec --ephemeral`；长实验交给独立受控进程。无需操纵桌面窗口，桌面聊天仅作进度与干预入口。

正式QA使用 `qa_container.py`：每次新容器/新Codex会话，只挂载一个ZIP、固定QA skills和空输出目录，不挂载作者目录、旧报告、管理state、另一审查输出或Docker socket。通过无凭据可信网关访问模型。两种AI独立执行原版release-self-check后才能合并。保留实际container ID、thread.started、路由与报告哈希；clean_context字段不替代启动记录。QA image和网关须预先实测。

## 验收与持续修正

双轨默认各10h真实有效研究；7h例外需固定合同和完整条件证据。两条最终方法当前SHA在冻结合同下分别复验。NOP对应当前任务、双镜像和separate Verifier，0分本身不是失败。稳定性观察实际容器持续健康12h，无重启，保留声明负载/健康检查；不拿管理器睡眠或存活时间代替。

两份PASS绑定同一最终ZIP哈希、固定QA版本、不同模型身份和新会话，21+3+6项齐全、逐项无未闭环分歧。管理器调用随附原版聚合器并追加完整性校验；管理/repair agent不能自评发布PASS。

通用调度器验证退出码、版本、哈希、证据和最低时长；实际实验、Harbor、模型及隔离由任务driver与独立QA验证。框架测试不是正式任务双轨/NOP/12h/PASS。完成指本地验收完成，不自动发布、发消息或填写平台表。
