# 持久化运行合同

## Plan

主控专用JSON，不得进入题包。schema_version=1；task_root是绝对作者任务目录；goal是用户目标。contract包含qa_version=0.3.4、effective_seconds_per_track=36000、stability_seconds=43200。reviewers为两个不同身份对象，各有provider/model/version，必须使用用户指定模型与最新路由，不自动替换。

drivers是这些key对应的非空argv数组：prepare、br、preflight_nop、dual_a、dual_b、finalize、nop、stability、package、qa_a、qa_b、repair。所有真实命令须先实测。调度器自动追加 `--request /absolute/job/request.json`，不使用shell拼接。可选retry_seconds默认60；job_timeout_seconds默认172800。deadline_utc仅在用户有授权预算边界时填写，过期进入NEEDS_INPUT，不标DONE。不设修复轮数上限。

7h例外需contract.seven_hour_exception含nontraining、short_iterations、continuing_directions三个全真字段；完整例外证据仍由QA核验。doctor拒绝缺driver、重复reviewer、QA版本错误、过低时长、run-dir嵌入task和不存在命令。

Python/PyPy 的直接脚本 argv 必须使用存在的绝对路径；worker 的 cwd 是 job 目录，不能依赖启动终端 cwd。reviewer 的 model 去首尾空白并忽略大小写后必须不同；provider/version 别名不构成第二个模型。对于 `python -m`、shell、容器和远程 driver，doctor 不证明其依赖或实际可用性，必须保留真实预检记录。

## Request与receipt

job为唯一UUID、新目录。request包含stage/revision/task_root/task_sha256/contract_sha256/contract/goal/receipt_path。repair收到failures（指向旧QA/运行记录）；非QA专家阶段收到upstream证据。candidate只应收到公开冻结任务，由专用sandbox/Harbor driver转译，不能继承管理request和私有路径。

driver写receipt.json：status为PASS/FAIL/RETRY/NEEDS_INPUT，revision与contract_sha256匹配，evidence为本job内非空文件的相对路径，无软链接越界，details为对象。失败附reason。真实exit code非0或缺receipt不能PASS。主控记录实际执行起止/退出和每个证据hash，不回显任意driver reason/stdout。凭据不进入driver环境；请求模型经可信网关。

各阶段details额外合同：

- dual_a/b：effective_seconds与duration_evidence。计时JSON含effective_seconds、intervals，每项start_epoch/end_epoch/kind；只计research，不重叠、不超过主控观测运行时间。适配已有格式须保留原始计时证据，不捏造。证据还需由正式QA核验。
- finalize：final_validations恰好a、b，各含method_sha256、contract_sha256和evidence；每轨自己的原始复验JSON含相同字段及status=PASS。不能互代结果，不改已冻结作者任务输入；选择/装配产物写到本job目录供package读取。
- nop/preflight_nop：trial_evidence至少含真实config、result、reward、log四类文件；原版QA负责语义核验。
- stability：observation为stability_worker产物；同容器持续健康至少合同秒数，无重启，无过大观测间隙。
- package：artifact为本job的完整ZIP。主控复制成immutable副本并重算SHA，QA只读该副本。
- qa_a/b：report和session_evidence必须在evidence。内置qa_container保存launch.json和events.jsonl实际来源。QA report只能由审查会话形成，不能主控补字段。
- repair：实质修改作者产物，主控比较repair开始/结束的作者目录hash，拒绝无改动回执。成功后新revision，清空当前阶段引用，保留历史。失败继续以新job修复，禁止改QA/contract或直接改报告PASS。

## 恢复与内置driver

并发阶段以每侧为单位持久化完成结果。若一侧 PASS、另一侧 RETRY，成功侧写入 completed 并移出在途 jobs；只为 RETRY 侧创建新 job。NEEDS_INPUT 同样保存成功侧，以 input_jobs 记录 driver 明确缺输入的侧，显式 resume 后仅清理这些已结束的尝试；plan、QA 资产或截止时间引起的配置阻塞不能清空尚未收割的 jobs。旧状态无标记时仅对明确的 driver 输入阻塞重新验证回执，选择 NEEDS_INPUT 侧。保留侧必须仍属于当前 revision/contract 且所有原始证据哈希匹配；正式任务或证据改变不能借“续接”复用。任一侧 FAIL 优先于另一侧 RETRY，进入实质 repair，避免临时故障掩盖内容失败。QA 的 driver PASS 只说明审查产物完整，报告中的 FAIL 仍由共识处理。

state原子写；调度锁避免双重派发；每job wrapper独立锁、started/heartbeat/exit记录。先落盘再启动detached wrapper。主控重启接回既有任务，不重复运行在途job；已记录但尚未启动的intent用同job锁安全续派。wrapper清除凭据环境，持续heartbeat，超时终止自己启动的进程组。缺失/改写的旧证据进入repair，旧证据失效不阻止新revision生成。每轮核验固定QA源码hash。

管理agent每个阶段从request/upstream/failures和磁盘产物重新建立上下文，stage/repair不继承旧会话历史。双轨driver必须把长研究实现为同一模型、同一冻结公开任务下的有界会话，检查点与有效计时落盘；换会话只续自身lane，不可读取另一lane或私有作者材料。后台管理程序不需要在长实验期间持续占用模型上下文。stage发生上下文/CLI失败时保留已写产物，下次由新会话修复并重新验证，不把失败会话计作完成。

`agent_stage.py --model MODEL [--gateway-url URL] [--reasoning-effort EFFORT] --request FILE`：专家侧prepare/repair等使用新Codex会话和固定回执schema。无网关时使用已有本机登录，不复制认证文件。它不是候选隔离边界或QA runner。

`qa_container.py --image CLEAN_IMAGE --network ISOLATED_MODEL_NETWORK --gateway-url http://trusted-gateway/v1 --request FILE`：image预装Linux Codex/Python3/git，无作者配置或任务历史；网络仅能访问指定可信网关。全新容器只挂input ZIP、QA skills、空out，不传凭据。gateway验证并记录指定模型/推理支持，不回退按量。

`stability_worker.py --container ACTUAL_CONTAINER_ID [--interval 30] [--health-argv-json JSON_ARRAY] --request FILE`：检查专用测试容器。无health命令时必须有Docker HEALTHCHECK且healthy。任务driver需另保存容器build/inspect与冻结任务绑定依据。

框架测试使用明确标注模拟实验和模型，仅验证管理行为。正式题目必须有真实driver、指定模型路由、Harbor版本和12h运行；尚未指定任务时不启动旧题，不宣称正式两个PASS。
