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

# 开发后自检报告（SeaTunnel）

## 1. 变更概览

- 变更标题：
- 变更类型（Fix/Feature/Improve/Docs/Test/Chore）：
- 影响模块（Core/Zeta/Connector-V2/Transform-V2/Format/Translation/E2E/Docs）：
- 是否用户可见（配置/语义/默认值/行为）：
- 是否涉及 streaming checkpoint / 状态升级：

## 2. 必跑命令与结果（粘贴真实输出摘要）

```bash
./mvnw spotless:apply
./mvnw -q -DskipTests verify
./mvnw test
```

- 结果摘要：
  - spotless: ✅/❌（补充关键信息）
  - verify: ✅/❌（补充关键信息）
  - test: ✅/❌（补充关键信息）

## 3. 按需验证（有则必填）

- IT/E2E（如涉及外部系统、容错、split、commit 语义）：

```bash
./mvnw -DskipUT -DskipIT=false verify
```

- 结果摘要：

## 4. 兼容性与风险检查

- 配置项（Option）是否新增/修改？是否保持向后兼容？
- 是否涉及 SPI/API 变更？是否需要迁移说明或不兼容变更记录？
- 是否新增依赖？是否使用了 `org.apache.seatunnel.shade.*`？
- 日志是否可能泄露敏感信息？异常信息是否携带上下文？

## 5. 文档检查

- docs/en 更新：是/否（列出文件）
- docs/zh 更新：是/否（列出文件）
- 示例配置是否与代码一致：是/否

## 6. 是否可合并结论

- 结论：可以合并 / 有条件合并 / 暂不建议合并
- 阻塞项（必须修复）：
  - -
- 风险与待办（可后续）：
  - -

