# 当前计划：Ads SD 报告接入

北京时间2026-10-17 21:13，用户明确回复“SD收尾。”，SD报告九项已确认完成，最终确认事项关闭。此次仅记录用户接受现有范围和验收结果，不新增采集或测试执行记录；原覆盖边界和证据保持，见[九项最终验收](../tools/SD报告九项最终验收.md)。下方实施步骤保留为历史。

2026-10-17 10:48 UTC，用户明确确认此前 Basic、Ads 通用、SP/SB/SD 基础数据、SP/SB 报告、两步业务数值示例复核及无凭据测试隔离修复全部完成。此确认不新增用户测试次数。下方旧阶段的待用户复验状态已关闭，原始执行记录保留。

本轮接入 SDK 原 SD 报告分区 9 个方法、18 个响应模型。唯一进度清单为 [todo.md](todo.md)，执行基线及证据为 [sd-reports-2026-10-17](../tools/verification/sd-reports-2026-10-17/)。沿用既有连接与开发凭据加载器，只执行授权的只读请求；不展示凭据，不修改 base，不 stage/commit/push，不改写既有 SP/SB 数据和用户修改。

1. 核对：冻结 SDK/已有数据/index；逐项对照官方路由、共享参数、版本头与响应结构，列清日报/小时差异和适用矩阵。
2. 最小接入：按 Campaign → AdGroup → Product → Target → MatchedTarget 顺序；每项先补采集/请求回归，再通过同一 main/main_testing 服务获取 Schema 前完整原文。人工零重试；自动开发采样只对瞬时错误有界退避，成功空结果不重试。
3. 每项闭环：严格 raw 差异 → 明确新增字段/类型语义及专用例外决定 → 原文 pass → 显式身份脱敏 → 正式 fixture/pytest → 真实完整业务行的字段、集合和方法文档。只暂停依赖未决项的步骤，其余继续；业务指标值及 JSON 类型保持。
4. 整体验收：SD 报告菜单、固定路径、明确 pytest 分组和整批固定分母；干净隔离环境与真实 main TTY 回归；验证旧数据、base、用户修改和暂存区保护。覆盖不足明确列出，由用户最终亲自验收 SD。

## 历史计划（已完成，原执行记录保留）

# Ads SP 六接口接入计划

## 当前新增授权：pytest分类及SD基础数据

完成检查点：用户两项明确批准均已实施，SD五项助手验收完成，当前只剩用户最终全链复验。最新2966项完整回归及1077项实际SD菜单回归均退出0，见[批准后验收](../tools/verification/pytest-groups-sd-2026-10-16/approved-finish.json)；以下保留分步计划和历史阶段。

用户已确认SB重新采集、核验脱敏及pytest全部正常，SB基础数据正式标记完成。下一步先交付pytest分类，再逐项推进SD，不修改base，不stage/commit/push，保留当前工作及暂存状态。

1. pytest分类：以正式测试文件的明确清单组合模块、Ads通用/SP/SB/SD板块和共享基础回归；保留全部正式测试及包含tools/tests的完整回归。不使用关键词过滤，展示真实范围，来源新鲜度检查只针对所选接口，保持只读数据、退出码和分页警告边界。验收菜单、返回/取消、分组覆盖及全跑一致性。
2. SD最小接入：按原SDK分区接入SdCampaigns、SdAdGroups、SdProducts、SdTargets、SdNegativeTargets，五项均有sid/profile_id、state、next_token、offset、length及版本头2。先核对官方参数与SDK，新增独立SD目录/登记及无豁免的严格契约，人工重试保持0。
3. 真实证据：复用原连接、单次传输捕获与轻量窗口，逐项核实标识、双传优先级、状态和offset/token完整data。临时自动采集对限流/服务端错误做有界退避，成功空响应不重试。差异点单列待决，其余独立部分继续。
4. 每项验收：原文严格核验→pass→明确叶子脱敏→fixture/正式pytest→真实非空字段及API/参数文档；仅已实证路径调整公开标识签名。完成后运行相关/完整离线回归并审计旧数据、base和暂存区。空结果和未观察结构仅记覆盖边界。

当前任务及检查点追加在todo.md；以下内容保留为此前已完成阶段。

范围：SpAdGroups、SpProducts、SpKeywords、SpTargets、SpNegativeKeywords、SpNegativeTargets。按接口完成 tools → 真实只读采集 → 严格差异核验 → 显式脱敏及 fixture → Schema/API/必要 Parameter 文档。共同参数及官方文档已核对；四个普通实体支持 state，两个否定接口不暴露 state，共享官方路由并分别固定 target_type。所有接口使用 X-API-VERSION: 2。

## 执行与保护

- 唯一进度清单为 [todo.md](todo.md)，验收证据集中在 tools/Ads六接口接入验收.json。
- 自动采集调用 main_testing.load_dev_credentials 和 main/workflow 共同服务；不复制凭据、签名、连接或采集旁路。
- 基线：/tmp/sp_entities_six_1v2553gx/before.json；141 个模型、39 份已有 Ads fixture、六份暂存文件及 raw/pass/fixture 指纹已保存。
- 不修改 base，不 stage/commit/push，已有数据和修改按基线保护；新接口使用同级固定前缀路径。
- A/B 沿用既有账号；每次请求至少间隔 1 秒，共享服务原有瞬时失败至多重试一次。只读实体窗口默认 2 条，参考窗口 4 条；独立视频诊断的真实命中整页作为补充证据，不改常规14场景。
- 不复用 SpCampaigns 的 tags 豁免。遇字段、行为或隐私决定，只暂停对应接口或步骤，其余继续。

## 顺序与验收

1. 共用接入：新增六个采集适配、固定注册及单行进度；离线验证准确签名、请求键、版本头、重试/取消、固定路径与旧文件保护。
2. SpAdGroups：独立 A/B 标识及错配、state、offset/token 窗口；严格核验真实响应，通过后完成脱敏 fixture、字段与方法文档及回归。
3. SpProducts：同类窗口；video_details采用用户批准的SpProductVideoDetail，六字段必填，name/url复用StrOrNone2Blank；完整非空视频补充页进入日常核验和fixture。
4. SpKeywords：同类窗口；脱敏关键词与实体标识，保留类型和跨页关系，完成文档和回归。
5. SpTargets：同类窗口；检查 expression/resolved_expression 内嵌业务值的隐私策略后再发布 fixture。
6. SpNegativeKeywords：不虚构 state 参数；固定 target_type=keyword，验证标识及分页；按批准决定直接更名campaign_id并验证真实筛选。
7. SpNegativeTargets：固定 target_type=target，其他同上一项；空结果仅说明当前覆盖不足。
8. 整体验收：正式 fixture、main/main_testing 共用路径、子步骤和单行总进度回归；完整离线测试及索引、base、旧数据保护检查。

每个接口只有真实非空响应契约、脱敏策略、fixture pytest、5A/5B 文档与行为对照全部满足才标完成。空状态、无游标、实体不足分别记录，不冒充覆盖。

## 已更新的决定

用户明确不保留兼容：两个公开参数已直接更名为campaign_id并正确输出请求，两组真实筛选已通过。表达式仅替换内嵌业务标识的策略已批准、实施并验证。两个否定字段采用专用值守卫豁免，保留现有有意义字段及原始数据。视频模型按最终名称SpProductVideoDetail实施，不保留旧提案名称；四个原生str字段及两个StrOrNone2Blank字段均必填，列表无默认值。独立任务找到的500条完整响应中有12个真实视频元素，固定原文和来源元数据受到SHA门禁保护；常规采集刷新保留补充页。人工main及公共服务未扩展重试，自动执行层只对暂时错误安排退避，不重试成功空结果。

六项已全部完成：79份原始契约通过，六项pass/fixture发布及5A/5B完成，最终完整离线回归1967通过（158.72秒）。142模型/118冻结响应对照、base/旧数据/index保护通过。准确证据、覆盖边界及修改清单见[最终验收](../tools/Ads六接口接入验收.json)，不需要继续联网。

## 后续文档审查

用户新增范围为全部已接入Basic/Ads方法的data示例空值检查，参数及运行逻辑不在额外范围。允许组合不同已核验脱敏真实记录的字段，关联值保持合理；外层响应不动，0/False不作空值，未发现非空来源的字段保留。既有fixture、固定raw/pass及补充证据共373份已检查，17方法/19场景全部覆盖。5个方法data示例与4处Schema examples已补齐，原规范已同步；14项定向检查及162模型/128冻结响应对照通过。最终完整离线回归1968项通过（154.46秒，退出0），结果已保存于[文档空值审查验收](../tools/已接入接口文档空值审查.json)，本轮完成，不再扩大联网。

## 后续已授权 Ads 子板块与目录整理

2026-10-16按用户确认增加通用2项、SP7项子板块和各层全选；仅传递原登记项给共用执行层，保持Basic、全局批量和独立pytest。用户随后授权把已有文件夹同样整理，三层统一采用`ads/basic/common/`及`ads/basic/sp/`，完整迁移固定样本、补充证据与独立视频探测目录；不更改SDK、业务参数、响应正文或暂存区。本轮实际验收及逐文件旧新路径/SHA保存于[迁移验收](../tools/Ads子板块与目录迁移验收.json)，进度仍用[todo.md](todo.md)。
