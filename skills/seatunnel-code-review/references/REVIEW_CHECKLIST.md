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

# Code Review Checklist（SeaTunnel）

本清单用于把“运行链路”落到可执行检查项，覆盖你提出的三大类：代码变更审查 / 代码质量评估 / 架构合理性。

> 使用方式：先根据 `RUNTIME_FLOW.md` 定位影响阶段，再按本清单逐项检查并在报告中给出 `path:line` 证据。

## A. 代码变更审查（Change Review）

### A1. 核心逻辑（必须有证据）

- 逻辑是否正确覆盖主流程与边界条件？
- 是否存在并发安全问题（共享状态、线程安全、可见性、竞态）？
- 是否可能产生重复读取/重复写入/丢数据（split 分配、重试、commit/abort）？
- streaming 场景：状态与 checkpoint 语义是否保持一致？

### A2. 兼容性影响（硬约束）

- 是否修改了配置项名称/默认值/类型/语义？是否可能导致“无感行为变化”？
- 是否变更或破坏公共 API / SPI（`seatunnel-api`）？
- 是否涉及序列化格式或状态结构变更？是否有升级/回滚路径？
- 如为不兼容变更：是否补充迁移说明与不兼容变更记录？

### A3. 副作用与性能（热路径重点）

- 是否引入额外的 IO / 网络请求 / RPC 往返 / 序列化次数？
- 是否在 reader/writer/enumerator 热路径引入不必要对象创建、全量缓存、频繁日志、锁竞争？
- 是否影响 backpressure / checkpoint 时延 / 吞吐？
- 是否可能引入资源泄露（连接、线程、文件句柄、buffer）？

### A4. 错误处理与日志（可诊断性）

- 异常是否携带足够上下文（table、task、config key、split id、并行度）？
- 是否有吞异常/静默失败？
- 日志级别是否合适（INFO 生命周期、WARN 可恢复、ERROR 任务失败）？
- 是否可能打印敏感信息（密码、token、连接串、密钥）？

## B. 代码质量评估（Quality）

### B1. 代码规范

- 是否符合项目风格（Spotless / Google Java Format）？
- 是否存在重复代码或可读性较差的实现（过深嵌套、魔法数、命名含糊）？
- 公共方法/复杂逻辑是否需要补充必要注释（避免“解释实现细节”的赘述注释）？

### B2. 测试覆盖

- 是否为新增/修改行为添加 UT（最小、确定性、覆盖关键分支）？
- 是否需要 IT/E2E 来覆盖与外部系统交互、容错恢复、并行 split？
- 失败重试/异常路径是否有覆盖？

### B3. 文档更新

- 是否更新 `docs/en` 与 `docs/zh`（如涉及用户可见行为/配置项/示例）？
- 示例配置是否与代码一致（名称、默认值、必填项）？
- 是否需要更新 release note / incompatible changes（若适用）？
- 如为 connector 文档：是否符合文档格式规范（admonitions/结构一致性）？可参考 `skills/seatunnel-contributor-playbook/references/DOCS_FORMAT_SPEC.md`。

## C. 架构合理性（Architecture）

### C1. 解决方案是否优雅

- 这是临时规避还是长期方案？长期方案是否清晰？
- 是否有明确的“责任边界”（模块职责、生命周期）？

### C2. 可维护性

- 代码是否清晰易懂、可测试、易排错？
- 错误信息是否可诊断（具备定位信息）？

### C3. 扩展性

- 对未来类似问题是否提供可复用的扩展点/抽象？
- 是否避免把 connector-specific 逻辑泄漏到 core/engine？

## D. 输出与结论（强制）

- 每个问题必须给出 `path:line` 证据与严重程度（高/中/低）。
- 明确列出“阻塞项”（必须修复）与“建议项”（可后续）。
- 给出最终 merge 建议：建议合并 / 有条件合并 / 不建议合并，并说明依据。

## E. 模块专项补充（按需）

- Connector-V2 新增/拆分模块：检查是否补齐插件集成（plugin-mapping/dist/pom/label/e2e/plugin_config）：见 `skills/seatunnel-contributor-playbook/references/CONNECTOR_INTEGRATION_CHECKLIST.md`。
- Zeta/API/Core/Docs/E2E 等高频模块：可参考近一年热点规范清单：`skills/seatunnel-contributor-playbook/references/MODULE_NORMS.md`。
