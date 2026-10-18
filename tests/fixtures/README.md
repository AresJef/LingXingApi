# Basic fixtures

## States正式fixture

`basic/states.json`来自用户已采集并核验的53条US州数据。本轮按用户批准的两条全局根路径规则仅替换request_id和response_time，States业务字段、结构及类型保留，接口专用规则为空。source=local_raw表示本地来源；助手没有重新联网采集。

fixture SHA256为`02683ca082b0a330c2cb7f4491db8407826f02403effddbc30981dc3cbe46e6b`。公共`tests/test_states_fixture.py`始终只读这个固定fixture并调用共享checker；缺文件或未经确认差异仍失败。主菜单与外部正式tests范围包含它；`--marketplace-fixture`只控制Marketplace输入。

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTEST_ADDOPTS= PYTEST_PLUGINS= .venv/bin/python -B -m pytest -q -p no:cacheprovider tests/test_states_fixture.py
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTEST_ADDOPTS= PYTEST_PLUGINS= .venv/bin/python -B -m pytest -q -p no:cacheprovider tests --marketplace-fixture tests/fixtures/basic/marketplaces.json
```

State三个字段的文档示例来自同一fixture的response.data[0]：country_code=US，state=AL-Alabama（输入state_or_province_name），state_code=AL（输入code）。本次新快照本地检查通过、待独立复核，详见[tools实施方案](../../tools/实施方案.md)。下列Marketplace记录保留其历史含义。

## Marketplace

basic/marketplaces.json 是第三步的固定输出；只有 tools/main.py 选择“脱敏核验数据”，且 raw/pass 相同并通过当前契约，按明确配置替换后再次通过，才自动覆盖。

| 文件 | 含义 |
| --- | --- |
| tools/data_raw/basic/marketplace-原始数据.json | 本地敏感原始业务 JSON |
| tools/data_pass/basic/marketplace-核验数据.json | 真实 pytest 通过的 raw 字节副本 |
| tests/fixtures/basic/marketplaces.json | 脱敏步骤的固定输出，当前文件关系验收见下文 |

字段规则在 tools/redaction/global.json 与 basic.json。当前仅两条根路径 request_id、response_time，Marketplace 专用规则为空；最终值以现有 replacement 为准。匹配 null/空值也直接赋值，不创建缺字段、不强转或修复类型。嵌套同名及其他未匹配值保持原样。生成不证明完整隐私安全，需使用者核查后决定用途。

新生成包装包含 source、endpoint、response；local_raw 只说明来自本地原始文件，不证明真实网络来源。旧包装中的元数据不参与响应契约。mock/synthetic 不可冒充真实样本。

正式 tests 独立于 tools，不读 .env、不联网、不写数据；默认严格检查固定 raw，显式 fixture 参数检查此文件：

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -B -m pytest -q -p no:cacheprovider tests
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 .venv/bin/python -B -m pytest -q -p no:cacheprovider tests --marketplace-fixture tests/fixtures/basic/marketplaces.json
```

缺文件、坏JSON、多/缺wire字段、非法别名、类型强转、错误计算或其他未经明确约定的解析值变化仍失败。已批准SDK派生response_count可缺于wire，但输出与各分支计算仍检查；成功error_details=[]合法，类型和值保持，非空明细结构覆盖未证明；total_count按已批准的SDK计数/max及直接返回分支独立核验，原始total不改。其他默认字段或空列表不自动忽略。

485356版本历史（其入口增量现已获R7认可；最新诊断/开发入口与用户手动验收见tools实施方案）：固定raw/pass/fixture均已存在，其mtime为2026-10-09 09:46–09:47 UTC，早于本轮新增入口授权。执行者本轮未恢复、生成或更新三文件。当前保存fixture的正式pytest实测66通过；全量338通过，工具272通过，真实PTY38/38。raw/pass SHA256相同，但当前来源及配置映射关系未在本轮完整复验；不能据此宣告三步发布链或真实联网验收完成。

tools/main.py主菜单“运行 pytest”直接只读本fixture并运行正式tests，不进入raw核验/脱敏步骤，不问凭据、不读.env、不运行tools/tests。测试结束后返回主菜单；累计失败保持1，Ctrl+C回收测试子进程并返回130。外部使用者无需main，仍可使用上方普通pytest命令；缺fixture真实失败，不能跳过成成功。

旧d51dd曾在已有本地raw上完成核验、发布pass、两条配置脱敏和fixture回归；旧79c45b阶段用户确认三个固定文件手动移除、有限可靠恢复核查未找到副本，缺文件回归如实FAIL。这些仅为各自历史快照证据，新诊断/开发入口补丁待增量独审，R7仅绑定485356。当前证据见[tools实施方案](../../tools/实施方案.md)。
