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

# 贡献场景通用套路（SeaTunnel）

> 本文件强调“通用可执行步骤”，不依赖特定 PR。需要结合具体模块与 connector 特性做裁剪。

补充参考（按需打开）：

- 模块规范与高频风险：`skills/seatunnel-contributor-playbook/references/MODULE_NORMS.md`
- 新 connector 的集成清单：`skills/seatunnel-contributor-playbook/references/CONNECTOR_INTEGRATION_CHECKLIST.md`
- 文档格式与一致性：`skills/seatunnel-contributor-playbook/references/DOCS_FORMAT_SPEC.md`

## 场景 A：新增 Source Connector（Connector-V2）

### 1) 先查重

- 是否已有同类 connector 或同协议实现？（避免重复造轮子）
- 是否已有相同能力在 Transform/Format/Engine 层实现？

### 2) 设计与契约（建议先输出小设计）

- 明确读取语义：增量/全量、顺序保证、容错与重试语义。
- split/enumerator 策略：并行度、倾斜、边界条件（空数据/分区变化/权限异常）。
- Option：名称稳定、默认值谨慎、描述含单位与范围。

### 3) 实现要点

- reader 热路径：避免全量缓存、控制对象创建与日志量。
- 资源释放：连接/线程/buffer 在异常路径也必须 close。
- 错误信息：包含 table/task/config key/split id 等上下文，不泄露敏感信息。

### 4) 测试与文档

- UT：split 边界、异常路径、重试语义。
- IT/E2E：外部系统交互、并行 split、容错恢复（必要时）。
- docs/en + docs/zh：配置项、示例、默认值一致。
- 新增 connector 的集成（发行物/插件/CI）：按 `CONNECTOR_INTEGRATION_CHECKLIST.md` 检查并补齐。

## 场景 B：新增 Sink Connector（Connector-V2）

### 1) 先明确写入语义

- 幂等/事务：至少一次/恰好一次的前提条件与承诺。
- commit/abort：失败后不留脏数据、不重复提交。

### 2) 性能策略

- batch/flush：避免 per-record 提交；注意 backpressure 与内存控制。

### 3) 测试与文档

- UT：commit/abort/重试语义。
- IT/E2E：目标系统端到端写入验证、失败重试。
- 文档双语同步。
- 新增 connector 的集成（发行物/插件/CI）：按 `CONNECTOR_INTEGRATION_CHECKLIST.md` 检查并补齐。

## 场景 C：新增/调整配置参数（Option）

### 1) 契约与兼容性（硬约束）

- 不改名、不随意改默认值；如必须改，提供迁移说明与回滚路径。
- 描述清晰：单位、取值范围、默认值、与其他参数的关系（互斥/依赖）。

### 2) 验证与示例

- 代码侧：Option 校验与错误信息可诊断。
- 文档侧：docs/en + docs/zh 示例同步；避免示例与代码不一致。

## 场景 D：修复 Bug

### 1) 最小复现与根因定位

- 复现步骤（配置 + 数据 + 环境）与预期/实际行为。
- 根因归类：资源泄露、重试语义、并发竞态、序列化/状态升级、checkpoint 语义等。

### 2) 修复策略

- 尽量修“根因”，避免临时绕过；如需临时规避，明确长期方案与 TODO。
- 错误处理补齐上下文；避免吞异常。

### 3) 测试回归

- UT 覆盖修复点与边界条件。
- 需要时补 IT/E2E（尤其外部系统/容错/并行）。

## 场景 E：Docs（文档）修复/补充

### 1) 先对齐代码契约（避免“文档正确但不可用”）

- 配置项/Option 名称、类型、默认值以代码为准；不要凭记忆手敲。
- 如涉及 connector：确认文档与实现的语义一致（batch/streaming、Exactly-once 前提、权限/幂等等）。

### 2) 中英文同步与格式一致（硬约束）

- `docs/en` 与 `docs/zh` 同步更新；示例必须可复制即用（括号/必填项齐全）。
- 格式与提示框：按 `DOCS_FORMAT_SPEC.md`（admonitions + 最小结构）。

## 场景 F：E2E（端到端）新增/稳定性修复

### 1) 优先保证稳定与可诊断

- 失败时能定位：容器日志/关键配置/断言信息必须清晰。
- 避免固定 sleep：优先 await/轮询条件达成 + 合理超时。

### 2) 常见不稳定来源（近一年高频）

- timeout 太短、镜像 tag 变动、容器删除冲突、外部依赖启动时序。
- 资源隔离与清理：表名/topic/bucket 追加随机后缀，确保 teardown。

## 场景 G：Zeta/Core/API/工程化模块（CI/Dist/Shade/Plugin）变更

### 1) 兼容性与影响面先行（硬约束）

- API/SPI/状态（state/serialVersionUID）属于对外契约：任何变更都要给出兼容性说明与验证用例。
- checkpoint/恢复语义变化必须明确：对吞吐/延迟/一致性的影响，并补齐稳定性测试。

### 2) 工程化联动检查（易漏）

- connector 能力是否需要同步 `plugin-mapping.properties` / `seatunnel-dist` / `seatunnel-plugin-discovery`？
- shading/依赖冲突：优先 shaded；新增非 shaded 依赖需要冲突评估与策略。
- CI/workflow 变更：考虑可复现性（镜像/tag/缓存）与回滚策略，避免引入全量不稳定。
