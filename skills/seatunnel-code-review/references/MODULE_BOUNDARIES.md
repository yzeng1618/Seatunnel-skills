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

# SeaTunnel 模块边界（Review 基线）

本文件用于在评审“架构合理性”时提供边界判断依据，避免 connector 逻辑泄漏到引擎/核心、避免破坏 SPI 与公共 API。

## 1. Core（seatunnel-core）

- 职责：作业配置/提交入口、通用能力（打包、CLI、基础运行抽象）。
- 评审要点：不要把 connector-specific 行为塞进 core；保持 API/SPI 最小化与稳定。

## 2. API（seatunnel-api）

- 职责：公共接口与 SPI（Source/Sink/Transform、Option 等）。
- 评审要点：这是对外契约；变更需要极强的兼容性约束与迁移说明。

## 3. Connector-V2（seatunnel-connectors-v2）

- 职责：各类 source/sink 实现；以 Option 暴露用户配置；通过 split/enumerator 支持并行。
- 评审要点：
  - Option 名称与语义稳定；避免改名/改默认值引发行为漂移。
  - 避免引入新依赖；优先使用 `org.apache.seatunnel.shade.*`。
  - reader/writer 热路径关注性能与资源释放。

## 4. Transform-V2（seatunnel-transforms-v2）

- 职责：数据处理算子链；可能涉及状态与性能热点。
- 评审要点：避免在 transform 中引入外部系统强依赖；注意状态可升级与 streaming checkpoint。

## 5. Zeta Engine（seatunnel-engine）

- 职责：调度、资源管理、容错与执行（Client/Master/Worker）。
- 评审要点：遵守任务生命周期；不要让 connector 的私有逻辑影响引擎通用调度与容错语义。

## 6. Translation（seatunnel-translation）

- 职责：对接 Flink/Spark 运行时的适配层。
- 评审要点：避免把引擎特定能力反向渗透到 Connector/API。

