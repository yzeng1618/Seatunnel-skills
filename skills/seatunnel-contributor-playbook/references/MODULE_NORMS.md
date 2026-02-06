<!--
Licensed to the Apache Software Foundation (ASF) under one or more
contributor license agreements.  See the NOTICE file distributed with
this work for additional information regarding copyright ownership.
The ASF licenses this file to You under the Apache License, Version 2.0
(the "License"); you may not use this file except in compliance with
the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

# 模块规范（基于近一年变更热点）

本文件用于把“贡献时真正高频踩坑的地方”沉淀成通用规范与检查点，方便：

- 功能设计（避免重复造轮子、避免破坏模块边界）
- 开发实现（减少返工）
- Code Review（更快聚焦风险）

## 1. 近一年变更热点（2025-02-05 ～ 2026-02-05）

基于本地 `seatunnel/` 仓库近一年提交统计（共 573 个 commits）：

- 高频变更模块（按“触达该模块的 commits 数”粗略统计）：
  - Connector-V2（`seatunnel-connectors-v2/`）：303
  - Docs（`docs/`）：246（`docs/en` 与 `docs/zh` 都非常活跃）
  - E2E（`seatunnel-e2e/`）：198（大量与 Connector-V2 相关）
  - Zeta/Engine（`seatunnel-engine/`）：62
  - CI Tools（`seatunnel-ci-tools/`）：59
  - Transform-V2（`seatunnel-transforms-v2/`）：46
  - API（`seatunnel-api/`）：29
  - GitHub Workflows（`.github/`）：28
  - Core（`seatunnel-core/`）：24
  - Dist（`seatunnel-dist/`）：19
  - Tools（`tools/`）：17
  - Format（`seatunnel-formats/`）：15
  - Common（`seatunnel-common/`）：13
  - Translation（`seatunnel-translation/`）：11
  - Config（`config/`）：9
  - Plugin Mapping（`plugin-mapping.properties`）：9
  - Plugin Discovery（`seatunnel-plugin-discovery/`）：5
  - Shade（`seatunnel-shade/`）：4

结论（用于指导规范优先级）：

- **Connector-V2 / Docs / E2E** 是最常见组合：新增/修复 connector 往往需要同步 docs 与 e2e。
- **Zeta/Engine** 的风险集中在：checkpoint、资源/线程泄露、并发与可观测性（metrics/logs/rest）。
- **API** 的风险集中在：SPI/生命周期、序列化兼容（state/serialVersionUID）、语义变更导致的生态影响。
- **CI/工程化模块**（`.github/`、`seatunnel-ci-tools/`、`seatunnel-dist/`、`plugin-mapping.properties` 等）变更频繁且影响面大：必须更严格评估可复现性与回滚策略。

> 说明：上面的数字是“某个 commit 是否触达该模块”的计数，非代码行数与非互斥分类，仅用于感知热点区域。

## 2. Docs（文档）规范

高频问题类型（近一年常见）：

- 连接器参数名在文档中写错/过期（导致用户照抄不可用）
- 中英文文档不同步
- 代码块/括号/示例配置不完整
- 参数类型/默认值描述不一致

规范与检查点：

- 文档属于功能的一部分：用户可见变更必须同步 `docs/en` + `docs/zh`。
- 配置项/Option 名称、默认值、示例必须以代码为准，避免“凭记忆写文档”。
- Connector 文档遵循统一格式（建议用 admonitions 强调注意事项）：见 `references/DOCS_FORMAT_SPEC.md`。
- 涉及不兼容变更：必须补充迁移与影响说明（并在项目约定的不兼容变更文档中记录）。

## 3. E2E（端到端测试）规范

高频问题类型（近一年常见）：

- flaky：偶现超时、容器删除冲突、外部依赖不稳定
- timeout 设置不合理（过短导致 CI 不稳定、过长导致诊断困难）
- docker image 变更导致 CI 失败（镜像来源、tag 变动）

规范与检查点：

- 写 E2E 的第一原则是**稳定与可诊断**：失败时必须能快速定位（容器日志/关键配置/断言信息）。
- 避免强依赖 wall clock，优先“条件达成轮询 + 合理超时”。
- 容器与外部资源必须隔离（表名/topic/bucket 随机后缀）并确保清理。
- E2E 规范细节：见 `skills/seatunnel-e2e-authoring/references/E2E_GUIDE.md`。

## 4. Connector-V2（连接器）规范补充

除 Connector-V2 通用开发规范外（见 `skills/seatunnel-connector-v2-dev/`），近一年高频改动集中在：

- schema/类型兼容：例如主键、decimal 精度、复杂类型、schema evolution（尤其 CDC）
- Options：新增/修正参数，常见问题是默认值与文档不同步
- writer 语义：flush/commit、资源关闭、失败重试后的幂等风险

规范与检查点：

- 新增/变更 connector 不仅是代码实现，还需要“集成到发行物/插件体系”：见 `references/CONNECTOR_INTEGRATION_CHECKLIST.md`。

## 5. Zeta（Engine）规范

高频问题类型（近一年常见）：

- checkpoint 调度极端场景丢失/线程池提前关闭/多余读取
- 资源泄露（map/线程/文件句柄/锁）
- 测试不稳定（并发断言、动态端口、依赖服务启动时序）

规范与检查点：

- 涉及 checkpoint：必须明确语义变化与对吞吐/延迟的影响，补齐稳定性测试。
- 任何“缓存/Map/线程池/锁”引入或变更必须审查关闭与生命周期。
- 并发断言优先使用 await/条件达成，而不是固定 sleep。
- REST/可观测性变更：确保错误信息可诊断、避免敏感信息泄露、指标命名稳定。

## 6. API（seatunnel-api）规范

高频问题类型（近一年常见）：

- SPI 生命周期方法遗漏调用（例如 init）
- connector/enumerator 语义调整导致生态影响
- state/序列化兼容问题（serialVersionUID 等）

规范与检查点：

- API/SPI 是对外契约：任何变更都需要兼容性评估与迁移说明。
- 涉及 state：明确升级/回滚策略；serialVersionUID 与字段演进必须谨慎。
- 语义变更必须落到可验证用例（UT/IT/E2E），避免“只改接口不改行为验证”。

## 7. Core（seatunnel-core）规范

近一年常见改动点：

- 各引擎 starter（Flink/Spark/Zeta）行为一致性与并行度/提交语义
- config 占位符/复杂配置解析健壮性
- 脚本/跨平台（Linux shell 与 Windows cmd）
- 插件目录/加载策略

规范与检查点：

- 涉及脚本：必须考虑 Windows + Linux；避免路径/编码/权限问题。
- 涉及配置解析：给出最小复现配置并补齐单测覆盖边界。
- 涉及 starter：明确对引擎行为与兼容性的影响。

## 8. CI Tools / Dist / Shade / Plugin Discovery（工程化模块）规范

近一年常见改动点：

- CI 镜像/版本变动引发的构建与 E2E 不稳定
- connector 集成到发行物（dist/pom、plugin-mapping、labeler、plugin_config）
- shading 与依赖冲突

规范与检查点：

- 变更 `.github/` workflow（尤其 E2E 相关）：必须考虑可复现性（镜像/tag/缓存）与回滚；避免“单点锁死”导致全量用例不稳定。
- 变更 CI 镜像/版本：必须考虑可复现性与回滚；必要时补充说明与锁定策略。
- 新增依赖：优先 shaded；新增非 shaded 依赖要说明冲突风险与策略。
- 新 connector 集成流程：见 `references/CONNECTOR_INTEGRATION_CHECKLIST.md`。

## 9. Transform-V2（seatunnel-transforms-v2）规范

近一年常见改动点：

- SQL Transform：新增/修正函数、类型推断与 cast 语义、解析阶段错误提示
- Embedding/LLM：模型提供方适配、向量维度、精度与性能

规范与检查点：

- 任何“类型语义/函数语义”改动都属于**高兼容性风险**：必须给出对照用例（UT）与清晰的错误信息（定位到表达式/字段）。
- 解析阶段能发现的问题尽量前置（parse/validate），避免运行时 ClassCastException 这类低可诊断错误。
- LLM/Embedding：不要在日志中输出敏感内容（prompt/token/密钥）；补齐超时/重试/失败降级策略，并在文档说明限制与语义。

## 10. Format（seatunnel-formats）规范

近一年常见改动点：

- JSON/CDC 相关格式字段补齐、timestamp/table 元信息
- decimal/数值序列化与反序列化一致性

规范与检查点：

- Format 往往被多个 connector 复用：输出字段/序列化格式属于对外契约，必须优先考虑向后兼容（必要时记录不兼容变更与迁移）。
- 为典型输入输出补齐 UT（包含边界：空值/精度/时区/科学计数法），避免“只修一个 connector，影响全局”。

## 11. Translation（seatunnel-translation）规范

近一年常见改动点：

- Flink/Spark 的 schema 演进、checkpoint 支持与行为一致性

规范与检查点：

- 新能力要明确“哪些引擎支持/不支持”，避免在一个引擎可用、另一个引擎静默失败。
- 影响 schema 合并/顺序的逻辑必须保证确定性（避免因集合遍历顺序导致偶现差异）。

## 12. Common / Config / Tools（公共与工具链）规范

近一年常见改动点：

- Common：时间/日期解析、基础工具方法行为修正
- Config：`seatunnel.yaml` 默认值与配置项有效性修复
- Tools：changelog 生成、依赖/CVE 修复、版本更新

规范与检查点：

- Common/Config 变更属于“全局放大器”：必须补齐单测覆盖边界，且更谨慎对待默认值与行为语义。
- Tools 变更需要保证**输出稳定与可复现**（同输入得到同输出），避免破坏发布/检查流程。
