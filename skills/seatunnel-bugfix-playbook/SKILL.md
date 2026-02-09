---
name: seatunnel-bugfix-playbook
description: Apache SeaTunnel Bug 修复工作流（bugfix、regression、correctness、data-loss、performance），用于输出可评审的修复与回归结论。
when_to_use: 当用户需要输出 SeaTunnel Bug 修复报告（最小复现、根因证据、修复策略、回归验证、merge 结论）时触发。
inputs_required:
  - 问题现象与期望行为（含错误日志或失败信息）
  - 变更范围（PR/diff/关键文件路径）
  - 运行上下文（引擎、模式、版本、外部依赖）
templates:
  - templates/BUGFIX_REPORT.md
references:
  - references/APACHE_BUGFIX_STANDARD.md
  - references/SEATUNNEL_BUGFIX_CHECKLIST.md
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

# 目标

- 把 Bug 修复过程标准化为一条可执行链路：复现 -> 定位 -> 修复 -> 验证 -> 回归 -> 合并结论。
- 输出可评审、可追溯的结果，避免“只改现象、不改根因”。

# 工作流（按顺序）

1. 明确问题分级与影响面
   - 标记问题类型：correctness、data-loss、security、performance regression、稳定性。
   - 识别影响模块与运行模式（Core/Zeta/Connector/Transform；batch/streaming；Flink/Spark/Zeta）。

2. 产出最小复现
   - 提供最小配置、最小数据、触发步骤、预期结果与实际结果。
   - 记录环境信息（版本、引擎、依赖、部署模式）。

3. 根因定位
   - 给出证据：`path:line` + 1~5 行最小代码片段。
   - 区分触发条件、根因与表象，避免把二次错误当根因。

4. 设计修复方案
   - 优先根因修复，不优先临时绕过。
   - 若必须临时规避，明确退出条件、风险与后续彻底修复计划。
   - 每个 PR 仅解决一个问题，避免混杂改动。

5. 风险与兼容性评估
   - 检查 Option/API/SPI 兼容性、默认值变化、序列化状态演进。
   - 检查性能副作用（热路径对象创建、IO/RPC、锁竞争、checkpoint 影响）。
   - 检查敏感信息日志泄露风险。

6. 验证与回归
   - 为修复点添加或更新 UT，必要时补 IT/E2E。
   - 把“如何验证修复有效且无回归”写成可重复执行步骤。
   - 明确是否需要 backport、release note 或迁移说明。

7. 输出结论
   - 使用模板 `templates/BUGFIX_REPORT.md` 输出报告。
   - 必须给出：阻塞项/建议项 + 是否可 merge（建议合并/有条件合并/不建议合并）。

## 常用参考（按需打开）

- 外部项目标准汇总与统一抽象：`references/APACHE_BUGFIX_STANDARD.md`
- SeaTunnel 落地清单与命令：`references/SEATUNNEL_BUGFIX_CHECKLIST.md`

## 输出约束

- 每个问题必须包含：问题描述、潜在风险、改进建议、严重程度（高/中/低）。
- 每个问题必须包含至少一个 `path:line` 证据。
- 对 correctness/data-loss/security 问题，默认按高优先级处理并明确阻塞合并条件。

## Examples

- 输入示例：`examples/example_input.md`
- 输出示例：`examples/example_output.md`
