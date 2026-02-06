---
name: seatunnel-e2e-authoring
description: Apache SeaTunnel E2E 用例编写与稳定性指南（Testcontainers、资源清理、flaky 规避、运行命令）。当你需要新增/修改 seatunnel-e2e 测试、复现集成问题、或为 connector 行为提供端到端验证时使用。
---

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

# 工作流（E2E）

1. 明确验证目标（新配置/兼容性/容错/幂等/并行 split/commit 语义）。
2. 按 `references/E2E_GUIDE.md`：
   - 选择合适的 TestSuiteBase 与容器（Testcontainers）
   - 确保资源清理与隔离，避免 flaky
   - 让用例可重复、可诊断（日志、超时、断言）
3. 记录运行命令与结果，补充到 PR 描述或自检报告。

