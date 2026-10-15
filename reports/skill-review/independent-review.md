# 最终独立复测

结论：本轮管理器行为复测通过，未发现新 input_jobs 标记引入的严重回归。manager.py SHA256：`e7dbc35e2972340b8f638d71efbfed2bfad8137ec8357ade580b63630535b611`；测试结束时已确认仓库源文件仍与被测快照一致。

## 实测

- 原有 15 项管理器测试全部通过（26.0 秒）。
- 仓库 10 项恢复回归全部通过（3.8 秒）。
- 5 项额外恢复情境全部通过（4.1 秒）。
- 独立补充 4 项 input marker 用例全部通过（1.9 秒）。

共 34 项测试通过。独立补充用例检查旧状态没有 input_jobs 时仅重开缺输入侧、双侧 NEEDS_INPUT 各仅新增一次尝试、QA assets 恢复后收割原已完成 jobs、NEEDS_INPUT 与 RETRY 混合恢复后不遗留标记。

先前发现的两类重复执行问题均已关闭：单侧 driver 暂时失败不会重跑成功 peer；plan/QA assets 配置阻塞解除不会重跑已完成但未收割的 jobs。在途 peer 不会被孤立；保留证据变化或跨 revision 会拒绝复用；任一侧 FAIL 优先于另一侧 RETRY。

## 边界

测试全部在临时快照和临时运行目录使用模拟 driver 执行，生产目录只读；未调用模型 API、未启动真实训练、未操作真实 Docker 资源。结果只证明被测管理器行为，不代表任何正式题目的有效研究时长、NOP、12h 稳定性或双 AI PASS。此前报告的 driver 源文件本身未内容锁定是已披露的额外增强项，本轮没有把它宣称为已修复。

## 原始日志

- manager-15.txt
- recovery-10.txt
- adversarial-5.txt
- input-markers-4.txt
- independent-summary.json
- manager.py SHA256 见本报告首段

额外 4 项最小测试：skills/autoresearch-manager/scripts/test_input_markers.py（仓库根目录下）。
