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

# 贡献行动计划（SeaTunnel）

## 1. 场景选择

（选择其一）

- [ ] 新增 Source Connector（Connector-V2）
- [ ] 新增 Sink Connector（Connector-V2）
- [ ] 新增/调整配置参数（Option）
- [ ] 修复 Bug
- [ ] Docs（文档）修复/补充
- [ ] E2E（端到端测试）新增/稳定性修复
- [ ] Zeta/Core/API/工程化模块变更（CI/Dist/Shade/Plugin）

## 2. 背景与目标

- 背景：
- 目标：
- 非目标：
- 影响模块：
- 影响运行模式（Zeta/Flink/Spark；batch/streaming）：

## 3. 现状对齐（推荐：先查重）

> 要求：列出证据（至少 `path`，建议 `path:line`）。

- 现有实现/相似实现：
  - `path/to/File.java:123`：
- 差距与需要新增的能力：
- （可选）补充“近期主流实现/改动热点”的证据（例如引用代表性实现位置 `path:line` 或典型变更点）。

## 4. 方案与实现要点

- 配置（Option）设计（如适用）：
- split/enumerator/reader（Source）要点（如适用）：
- writer/commit/abort（Sink）要点（如适用）：
- 错误处理与日志（上下文、敏感信息）：
- 性能与副作用（热路径、资源释放）：
- streaming checkpoint/恢复语义（如适用）：

## 5. 分阶段实现计划（建议可拆多 PR）

- Phase 1：
  - 代码点位：
  - 测试：
  - 文档（docs/en + docs/zh）：
  - 风险与验证：
- Phase 2：

## 6. 测试与验证计划

```bash
./mvnw spotless:apply
./mvnw -q -DskipTests verify
./mvnw test
```

- 是否需要 IT/E2E（外部系统/容错/并行 split/commit 语义）：

```bash
./mvnw -DskipUT -DskipIT=false verify
```

## 7. 文档与发布影响

- docs/en 更新：
- docs/zh 更新：
- 不兼容变更（如适用）：迁移与回滚方案：

## 8. 风险与回滚

- 风险：
- 缓解措施：
- 回滚/降级策略：
