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

# SeaTunnel Bug 修复检查清单

## 1. 缺陷输入信息

- 问题编号（Issue/JIRA/PR 链接）：
- 影响模块（Core/Zeta/API/Connector/Transform/E2E/...）：
- 影响运行模式（batch/streaming，Flink/Spark/Zeta）：
- 严重级别（高/中/低）：

## 2. 最小复现

- 配置与数据：
- 触发步骤：
- 预期结果：
- 实际结果：
- 环境信息（版本、部署模式、依赖）：

## 3. 根因与修复

- 根因证据（必须 `path:line`）：
- 修复策略（根因修复 / 临时规避）：
- 影响面（兼容、性能、副作用）：

## 4. 风险评估

- Option/API/SPI 或默认值影响：
- 状态/序列化（若涉及）：
- 性能热路径影响：
- 错误处理与敏感信息日志风险：

## 5. 测试与验证

```bash
./mvnw spotless:apply
./mvnw -q -DskipTests verify
./mvnw test
```

如需 E2E/IT：

```bash
./mvnw -DskipUT -DskipIT=false verify
```

- 新增/修改 UT：
- 新增/修改 IT/E2E：
- 手工验证与结果摘要：

## 6. 文档与发布

- docs/en 更新：
- docs/zh 更新：
- 不兼容变更记录与迁移说明（如适用）：
- backport/release note（如适用）：
