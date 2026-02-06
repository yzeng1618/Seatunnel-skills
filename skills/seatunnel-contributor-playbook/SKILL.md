---
name: seatunnel-contributor-playbook
description: Apache SeaTunnel 贡献者通用 Playbook（新增 source/sink、新增配置参数、修复 bug）。当需要一份通用、可执行的贡献流程与检查清单，并能结合 code review 与质量门禁 skills 给出行动计划时使用。
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

# 目标

- 用“通用套路 + 清单”的方式覆盖高频贡献场景：
  1) 新增 source/sink 数据源（Connector-V2）
  2) 新增/调整数据源参数（Option）
  3) 修复 bug（含兼容性/性能/容错）
  4) Docs（文档）修复/补充（`docs/en` + `docs/zh`）
  5) E2E（端到端测试）新增/稳定性修复
  6) Zeta/Core/API/工程化模块变更（如 checkpoint、插件体系、CI/Dist/Shade）

# 使用方式

- 先按 `references/CHANGE_RECIPES.md` 选中对应场景，生成一份行动计划（代码点位 + 测试 + 文档 + 风险）。
- 输出时建议使用模板：`templates/CONTRIBUTION_PLAN.md`（更适合写到 PR 描述/设计文档里）。
- 参考上游 SeaTunnel 的“已有实现与近期变更热点”（例如：Connector-V2 / Docs / E2E / Zeta）对齐实现与文档风格，并把结论反哺到 `references/CHANGE_RECIPES.md`（保持通用，不粘具体 PR）。
- 开发完成后建议配合：
  - `$seatunnel-post-dev-audit` 做质量门禁
  - `$seatunnel-code-review` 做结构化评审输出

## 常用参考（按需打开）

- `references/MODULE_NORMS.md`：按模块的高频风险与规范（基于近一年变更热点）
- `references/CONNECTOR_INTEGRATION_CHECKLIST.md`：新增 connector 的集成检查清单
- `references/DOCS_FORMAT_SPEC.md`：文档格式与一致性规范（含 admonitions）
