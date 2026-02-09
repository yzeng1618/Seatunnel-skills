---
name: seatunnel-connector-v2-dev
description: Apache SeaTunnel Connector-V2 开发与评审指南，覆盖 Source/Sink 实现、Option 定义、split/enumerator、checkpoint 语义、测试和文档。
when_to_use: 当用户在实现或修改 SeaTunnel Connector-V2（Source/Sink）并需要开发/评审清单时使用。
inputs_required:
  - Connector 目标系统与读写语义说明
  - 变更代码或设计草案（关键类/接口）
  - 预期运行模式与验证范围（batch/streaming，UT/IT/E2E）
templates: []
references:
  - references/CONNECTOR_V2_GUIDE.md
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

# 工作流（Connector-V2）

1. 明确连接器职责（Source/Sink）与运行模式（batch/streaming）。
2. 按 `references/CONNECTOR_V2_GUIDE.md`：
   - 定义 Option（名称稳定、描述清晰、默认值谨慎）
   - 实现 split/enumerator 与并行读写
   - 明确写入语义（幂等/事务/commit/abort）
   - 优先使用 shaded 依赖，避免新增依赖冲突
3. 补齐测试与文档：
   - UT 覆盖核心逻辑与异常路径
   - 必要时补充 IT/E2E
   - 更新 docs/en 与 docs/zh，保证配置示例与默认值一致

## Examples

- 输入示例：`examples/example_input.md`
- 输出示例：`examples/example_output.md`
