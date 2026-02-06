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

# Seatunnel Skills

本目录用于存放面向 **Apache SeaTunnel** 的 Agent Skills（工作流+模板+参考资料），目标是让贡献者与 Code Review 的输出更一致、更可验证。

## 如何使用

在对话中直接点名 Skill（建议用 `$skill-name`），并附上 PR / diff / 变更说明，例如：

- “使用 `$seatunnel-code-review` 评审这次 PR 的核心逻辑与兼容性，按模板输出报告。”
- “使用 `$seatunnel-post-dev-audit` 对我刚完成的改动做开发后自检，给出是否可合并结论。”

## 输出约定（所有 skills 通用）

- **必须**用 `path:line`（1-based 行号）引用定位问题；尽量附 1~5 行最小代码片段。
- 每个问题最少包含：问题描述 / 潜在风险 / 最佳改进建议 / 严重程度（高/中/低）。
- 最后给出：是否可 merge（建议合并 / 有条件合并 / 不建议合并）与“阻塞项/建议项”。

## 已提供的 Skills

- `seatunnel-code-review/`：基于 SeaTunnel 运行链路的代码评审（核心逻辑/兼容性/副作用/错误处理/测试与文档/架构合理性）。
- `seatunnel-post-dev-audit/`：开发完成后的规范性与质量门禁自检（spotless/verify/test、文档双语、兼容性与风险）。
- `seatunnel-feature-design/`：功能设计/技术方案（扫描现状、调研方案、mermaid 架构图、实现规划、优缺点评估）。
- `seatunnel-connector-v2-dev/`：Connector-V2 开发/评审要点（Option、split/enumerator、shaded 依赖、docs/en+zh、e2e）。
- `seatunnel-e2e-authoring/`：E2E 用例编写与稳定性指南（Testcontainers、资源清理、flaky 规避、运行命令）。
- `seatunnel-contributor-playbook/`：贡献者通用 Playbook（新增 source/sink、参数、bugfix 的行动清单）。

## 禁用 Skill（仓库维护约定）

如需下线某个 skill（但暂时无法物理删除/或需要保留历史），可在 skill 目录下放置 `DISABLED` 文件；校验脚本 `python scripts/validate_skills.py` 会自动跳过该目录。
