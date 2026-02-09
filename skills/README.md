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

本目录存放面向 **Apache SeaTunnel** 的 Agent Skills（工作流 + 模板 + 参考资料），目标是让贡献过程与评审输出更一致、更可验证。

## 如何使用

在对话中直接点名 Skill（建议用 `$skill-name`），并附上 PR / diff / 变更说明，例如：

- “使用 `$seatunnel-code-review` 评审这次 PR 的核心逻辑与兼容性，按模板输出报告。”
- “使用 `$seatunnel-post-dev-audit` 对我刚完成的改动做开发后自检，给出是否可合并结论。”

## 输出约定（所有 skills 通用）

- **必须**用 `path:line`（1-based 行号）定位问题；尽量附 1~5 行最小代码片段。
- 每个问题最少包含：问题描述 / 潜在风险 / 最佳改进建议 / 严重程度（高/中/低）。
- 最后给出：是否可 merge（建议合并 / 有条件合并 / 不建议合并）与“阻塞项/建议项”。

## SKILL.md Front-matter 规范

每个 `skills/<skill-name>/SKILL.md` 必须以 YAML front-matter 开头，字段如下：

- `name`（必填，且与目录名一致）
- `description`（必填，一行摘要）
- `when_to_use`（必填，触发条件）
- `inputs_required`（必填，数组）
- `templates`（必填，数组，可空）
- `references`（必填，数组，可空）
- `agents`（必填，数组，可空）
- `version`（可选）

示例：

```yaml
---
name: seatunnel-feature-design
description: Apache SeaTunnel 功能设计/技术方案输出。
when_to_use: 当需要输出可落地的 feature design 与实现规划时使用。
inputs_required:
  - 目标问题与约束
  - 变更范围
templates:
  - templates/FEATURE_DESIGN_DOC.md
references:
  - references/DESIGN_CHECKLIST.md
agents:
  - agents/openai.yaml
version: "1.0.0"
---
```

路径规则：`templates` / `references` / `agents` 中的每一项都必须是 skill 目录内的相对文件路径。

## 已提供 Skills（自动生成）

> 以下区块由 `python scripts/generate_skills_index.py` 自动维护，请勿手工编辑。

<!-- AUTO-GENERATED:START -->
| Name | Description | Entry |
| --- | --- | --- |
| `seatunnel-bugfix-playbook` | Apache SeaTunnel Bug 修复工作流（bugfix、regression、correctness、data-loss、performance），用于输出可评审的修复与回归结论。 | [`SKILL.md`](./seatunnel-bugfix-playbook/SKILL.md) |
| `seatunnel-code-review` | 基于 Apache SeaTunnel 运行链路进行代码评审（PR/diff/review），输出带 path:line 的问题清单、严重程度和可合并结论。 | [`SKILL.md`](./seatunnel-code-review/SKILL.md) |
| `seatunnel-connector-v2-dev` | Apache SeaTunnel Connector-V2 开发与评审指南，覆盖 Source/Sink 实现、Option 定义、split/enumerator、checkpoint 语义、测试和文档。 | [`SKILL.md`](./seatunnel-connector-v2-dev/SKILL.md) |
| `seatunnel-contributor-playbook` | Apache SeaTunnel 贡献者通用 Playbook（新增 source/sink、参数变更、bugfix），用于生成可执行行动计划与检查清单。 | [`SKILL.md`](./seatunnel-contributor-playbook/SKILL.md) |
| `seatunnel-e2e-authoring` | Apache SeaTunnel E2E 用例编写与稳定性指南（Testcontainers、资源清理、flaky 规避、运行命令），用于新增/修改 e2e 验证方案。 | [`SKILL.md`](./seatunnel-e2e-authoring/SKILL.md) |
| `seatunnel-feature-design` | Apache SeaTunnel 功能设计/技术方案输出（feature design/spec），覆盖现状扫描、方案对比、mermaid 架构图和实现规划。 | [`SKILL.md`](./seatunnel-feature-design/SKILL.md) |
| `seatunnel-post-dev-audit` | 开发完成后的 SeaTunnel 规范性与质量门禁自检（spotless/verify/test、兼容性、文档双语、依赖与日志脱敏）。 | [`SKILL.md`](./seatunnel-post-dev-audit/SKILL.md) |
<!-- AUTO-GENERATED:END -->

## 维护命令

新增或修改 skill 后，至少运行：

```bash
python scripts/validate_skills.py
python scripts/generate_skills_index.py
python scripts/validate_skills.py --check-index
```

也可以使用：

```bash
python scripts/validate_skills.py --check-index --fix-index
```

## 禁用 Skill（DISABLED 约定）

如需临时下线某个 skill（但暂时不删除目录），可在对应目录放置 `DISABLED` 文件：

- `validate_skills.py` 会跳过该 skill。
- `generate_skills_index.py` 会从自动索引中排除该 skill。
