---
name: seatunnel-e2e-authoring
description: Apache SeaTunnel E2E 用例编写与稳定性指南（Testcontainers、资源清理、flaky 规避、运行命令），用于新增/修改 e2e 验证方案。
when_to_use: 当用户需要新增或审查 SeaTunnel E2E 用例，复现集成问题，或验证 connector 端到端行为时使用。
inputs_required:
  - 目标行为与验收条件（需要验证什么）
  - 相关改动或候选用例（PR/diff/测试目录）
  - 运行环境约束（容器依赖、CI 资源、超时要求）
templates: []
references:
  - references/E2E_GUIDE.md
agents:
  - agents/openai.yaml
version: "1.0.0"
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
3. 补充最小单元测试标准（与 E2E 配套，避免仅靠集成用例兜底）：
   - 必须覆盖：配置解析/参数校验（非法参数、缺省值、边界值）
   - 必须覆盖：核心行为的纯逻辑断言（不依赖容器）
   - 必须覆盖：至少 1 条异常路径（例如连接失败、反序列化失败、提交失败）
   - 在输出中记录 UT 用例名与对应 `path:line`，并说明其与 E2E 场景的对应关系
4. 记录运行命令与结果，补充到 PR 描述或自检报告。

## Examples

- 输入示例：`examples/example_input.md`
- 输出示例：`examples/example_output.md`
