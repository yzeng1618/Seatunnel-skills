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

# SeaTunnel 本地验证命令（质量门禁）

> 本文件用于贡献者自检与 Review 对齐。不同模块可能需要额外命令（例如特定 connector 的集成测试）。

## 1. 必跑（强制）

```bash
# Format code (mandatory)
./mvnw spotless:apply

# Quick verification (mandatory)
./mvnw -q -DskipTests verify
```

## 2. 强烈推荐

```bash
# Unit tests (strongly recommended)
./mvnw test
```

## 3. 按需（涉及 E2E/外部系统/容错时）

```bash
# Run IT/E2E
./mvnw -DskipUT -DskipIT=false verify
```

## 4. 结果记录要求

- 在 PR 描述或自检报告中记录：
  - 执行的命令
  - 通过/失败结论
  - 如失败：关键错误摘要与修复计划

