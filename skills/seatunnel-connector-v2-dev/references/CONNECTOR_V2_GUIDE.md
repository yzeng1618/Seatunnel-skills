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

# Connector-V2 开发/评审指南（精简版）

> 目标：把 Connector-V2 的常见“硬约束”和“高风险点”收敛成可执行清单，减少踩坑与 Review 往返。

## 1. Option（配置契约）

- 所有用户可见配置必须用 Option 定义：名称、类型、默认值（如有）、清晰描述。
- Option 名称是稳定契约：不要轻易改名；默认值变更要评估兼容性与行为漂移。
- 描述中避免模糊词（如“可能/大概”）；明确单位（ms/bytes/rows）。

## 2. split/enumerator/reader（并行读）

- SplitEnumerator
  - 负责发现 splits、分配 splits、必要时再均衡。
  - 关注边界：空数据、分区新增、权限异常、网络抖动、断点续传。
- Reader
  - 热路径避免全量缓存与不必要对象创建。
  - 资源必须可关闭（连接/线程/buffer），异常路径也要释放。
- 语义
  - 明确失败重试是否会重复读取；如可能，需具备去重或幂等策略说明。

## 3. writer/commit/abort（写入语义）

- 幂等/事务
  - 明确至少一次/恰好一次的承诺与前提条件。
  - commit/abort 行为必须一致且可恢复；失败后避免遗留脏数据或重复写入。
- 性能
  - 合理的 batch/flush 策略；避免每条记录刷盘/提交。
  - 控制日志量，避免在热路径打印 INFO。

## 4. 依赖与 shading

- 优先使用 `org.apache.seatunnel.shade.*`。
- 避免新增依赖；若必须新增，说明理由、大小、冲突与 shading 方案。

## 5. 测试与文档（用户可见即必须）

- UT：覆盖核心逻辑与异常路径（如 split 边界、重试、commit/abort）。
- IT/E2E：涉及外部系统、容错恢复、并行 split 时补齐。
- docs/en + docs/zh：配置项、默认值、示例必须与代码一致。

## 6. 集成到发行物/CI（新增 connector 常见遗漏点）

新增或拆分出新的 connector 模块后，通常还需要把它“接入”到插件体系与发行包，否则用户即使写了配置也无法在发行物中使用。

- 集成清单：`skills/seatunnel-contributor-playbook/references/CONNECTOR_INTEGRATION_CHECKLIST.md`
- 文档格式建议：`skills/seatunnel-contributor-playbook/references/DOCS_FORMAT_SPEC.md`
