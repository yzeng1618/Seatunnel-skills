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

# Code Review 报告（SeaTunnel）

## 1. 基本信息

- PR / 变更标题：
- 变更类型（Fix/Feature/Improve/Docs/Test/Chore）：
- 影响模块（Core/Zeta/Connector-V2/Transform-V2/Format/Translation/E2E）：
- 运行模式（batch/streaming，本地/集群，Zeta/Flink/Spark）：
- 评审范围（文件/目录列表）：

## 2. 运行链路影响（基于 SeaTunnel Runtime Flow）

> 参考：`skills/seatunnel-code-review/references/RUNTIME_FLOW.md`

- 影响阶段（勾选/补充）：
  - [ ] 配置解析与 Option 校验
  - [ ] 插件发现/Factory 加载
  - [ ] 引擎调度（Zeta：Client/Master/Worker）
  - [ ] Source：split/enumerator/reader
  - [ ] Transform：链路/状态/性能
  - [ ] Sink：writer/commit/幂等/事务
  - [ ] Checkpoint/恢复/容错（尤其 streaming）
  - [ ] 指标/日志/可观测性

## 3. 整体结论（是否可 merge）

- 结论（选择其一）：建议合并 / 有条件合并 / 不建议合并
- 阻塞项（必须修复才能 merge）：
  - -
- 建议项（不阻塞但建议尽快处理）：
  - -

## 4. 发现的问题清单（必须提供引用与严重程度）

> 每条问题都必须包含：
> - 引用：`path/to/File.java:123`（1-based 行号）
> - 1~5 行最小代码片段（可选但强烈建议）
> - 问题描述 / 潜在风险 / 最佳改进建议 / 严重程度（高/中/低）

### 4.1 问题 #1（严重程度：高/中/低）

- 引用：`path/to/File.java:123`

```java
// paste minimal snippet here (1~5 lines)
```

- 问题描述：
- 潜在风险：
- 最佳改进建议：
- 是否阻塞合并：是/否

### 4.2 问题 #2（严重程度：高/中/低）

- 引用：`path/to/File.java:123`

```java
// paste minimal snippet here (1~5 lines)
```

- 问题描述：
- 潜在风险：
- 最佳改进建议：
- 是否阻塞合并：是/否

## 5. 覆盖性检查（必填）

### 5.1 兼容性影响

- 是否新增/修改配置项（Option）？是否保持向后兼容（名称/默认值/SPI）？
- 是否需要迁移说明？是否需要在不兼容变更文档中记录？

### 5.2 副作用与性能

- 是否引入额外 RPC/序列化/IO/锁竞争/内存占用？
- 在 split/enumerator、reader、writer 热路径是否有不必要对象创建或全量缓存？
- 是否可能引入 backpressure、checkpoint 变慢、吞吐下降？

### 5.3 错误处理与日志

- 异常是否携带足够上下文（table、task、config key）？
- 日志级别是否合理（INFO/WARN/ERROR）？是否可能泄露敏感信息？

### 5.4 测试与文档

- 是否新增/更新 UT / IT / E2E？是否覆盖关键分支与边界条件？
- 是否更新文档（docs/en & docs/zh），且配置示例与默认值准确？

## 6. 建议的本地验证命令（按需选择）

```bash
./mvnw spotless:apply
./mvnw -q -DskipTests verify
./mvnw test
./mvnw -DskipUT -DskipIT=false verify
```

