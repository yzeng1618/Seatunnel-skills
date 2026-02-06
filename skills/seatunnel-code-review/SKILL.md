---
name: seatunnel-code-review
description: 基于 Apache SeaTunnel 运行链路进行代码评审（PR/diff/review）。当需要审查 SeaTunnel 变更、评估兼容性/性能副作用/错误处理/测试与文档/架构合理性，并输出带 path:line 引用的问题清单与是否可合并结论时使用。
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

- 基于 SeaTunnel 的“配置 → 插件加载 → 引擎调度 → Source/Transform/Sink 执行 → Checkpoint/Commit”链路做系统性评审。
- 对每个发现的问题给出可操作的改进建议，并给出最终 merge 结论。

# 工作流（按顺序执行）

1. 收集上下文
   - 获取 PR 描述、变更动机、影响模块（Core / Zeta / Connector-V2 / Transform-V2 / Format / Translation / E2E）。
   - 获取变更范围：新增/修改的配置项、行为改变点、涉及的运行模式（batch/streaming、本地/集群、Zeta/Flink/Spark）。

2. 运行链路定位
   - 对照 `references/RUNTIME_FLOW.md` 标注本次变更影响的阶段（解析配置、Option 校验、Factory/SPI 插件加载、调度、split/enumerator、reader/writer、checkpoint/commit、错误恢复等）。
   - 明确“谁调用谁 / 生命周期边界 / 状态与并发模型”，再进入细节评审。

3. 逐类评审（必须覆盖）
   - 使用 `references/REVIEW_CHECKLIST.md` 逐项检查：核心逻辑、兼容性影响、副作用与性能、错误处理与日志、测试与文档、架构合理性。
   - 任何兼容性变更：要求明确文档与迁移方案（避免改 config 名称/默认值、避免破坏 SPI）。

4. 输出评审报告（严格按模板）
   - 以 `templates/REVIEW_REPORT.md` 为输出骨架。
   - 每个问题都必须包含 `path:line` 引用（1-based 行号）并尽量给最小代码片段（1~5 行）。
   - 对每个问题给出：问题描述 / 潜在风险 / 最佳改进建议 / 严重程度（高/中/低）。
   - 最后给出：是否可 merge 的整体结论（建议合并 / 有条件合并 / 不建议合并）与阻塞项列表。

# 输出要求（硬性约束）

- 仅在证据充分时下结论；不确定的地方要标注“待确认”并给出最小验证方法。
- 不输出敏感信息（密码、token、连接串等）；评审时也要检查日志是否可能泄露敏感信息。
- 避免“泛泛而谈”；必须把建议落到具体位置（`path:line`）与可执行动作。

