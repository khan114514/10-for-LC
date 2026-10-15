# 本次交接验证

这是仓库材料与管理框架的验证，不是十题正式执行验收。

| 项目 | 本次结果 |
|---|---|
| 正式题名在线查重 | 10/10 pass；2026-10-15 当次题库快照 |
| 顶会与固定源码 | 10 篇正式出处、10 个官方仓库固定提交，训练/模型/配置入口已读 |
| 困难 PE | 10/10 困难预评，置信度中；目标机实测未完成 |
| 独立 manager 行为测试 | 15 + 10 + 5 + 4 = 34/34 PASS |
| 主控对交付测试脚本复跑 | 同四组 34/34 PASS；旧测试仅作变量改名，新增测试使用仓库相对定位 |
| 实际 Docker 隔离测试 | 1/1 PASS，两个独立容器与终止回收；模型输出为模拟 |
| skill-creator quick_validate | PASS；使用带 PyYAML 的验证环境，系统 Python 缺 PyYAML 已单独处理 |
| Python 语法 / JSON 解析 | PASS |
| 源码获取工具 smoke | ConsisGAD 实际拉取并核对固定 SHA；未安装、执行训练或解析数据 |
| 固定 QA | v0.3.4 的 34 文件保持原始哈希 |
| 严格隐私与可移植性检查 | 见 privacy-summary.json；使用本地 strict protocol 扩展，非平台官方验收 |
| 文件清单、完整性、git diff | 上传前由 verify_handoff 与 git diff --check 核验 |

复现管理器测试（仓库根目录）：

```bash
python3 skills/autoresearch-manager/scripts/test_manager.py
python3 skills/autoresearch-manager/scripts/test_recovery_regressions.py
python3 skills/autoresearch-manager/scripts/test_adversarial_recovery.py
python3 skills/autoresearch-manager/scripts/test_input_markers.py
```

Docker 测试需已运行 Docker 和 python:3.12-slim 基础镜像，执行：

```bash
AUTORESEARCH_MANAGER_DOCKER_TEST=1 python3 skills/autoresearch-manager/scripts/test_qa_docker.py
```

独立测试原始日志在 ../skill-review；manager.py 被测哈希绑定在审查报告中。模型身份、模型真实调用、长研究时长、Harbor 实际运行、数据资产完整性、真实训练得分、最终双 AI 质检不在本次测试范围内；不能用模拟 PASS 替代。
