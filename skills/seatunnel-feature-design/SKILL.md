---
name: seatunnel-feature-design
description: Apache SeaTunnel 功能设计/技术方案输出（feature design/spec/设计文档）。当需要先扫描 Seatunnel 现有模块判断是否已有实现、调研主流方案、选择简单稳定的实现路径、输出实现规划与 mermaid 架构图，并给出方案优缺点与风险评估时使用。
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

- 产出可 review、可落地、可验证的 SeaTunnel 功能设计文档（包含架构图、实现计划、风险与权衡）。
- 以 SeaTunnel 运行链路为基线，确保方案与模块边界、兼容性与可运维性一致。

# 工作流（按顺序执行）

1. 明确问题与范围
   - 定义问题陈述、目标/非目标、影响的引擎与模式（Zeta/Flink/Spark，batch/streaming）。
   - 明确影响模块（API/Core/Zeta/Connector-V2/Transform-V2/Format/Translation/E2E）。

2. 扫描现有实现（先“查重”，再设计）
   - 在 SeaTunnel 仓库中搜索关键词、接口、Option、配置示例，确认是否已有实现或相似实现。
   - 输出“已有实现清单”与差距：列出关键文件 `path:line`（或至少 `path`）作为证据。
   - 建议把上游仓库克隆到 `external/seatunnel/`（不要提交）：见 `external/README.md`。

3. 调研主流方案（可离线/可在线）
   - 优先调研：SeaTunnel 内部已有模式、同类 connector/engine 的实现、类似社区实践。
   - 记录“备选方案”并说明适用条件、复杂度与风险。

4. 选择实现原则（简单/有效/稳定）
   - 对照 `references/DESIGN_CHECKLIST.md`：兼容性、性能副作用、错误处理、可观测性、测试与文档、回滚策略。
   - 明确为何选择当前方案（而非备选），并列出取舍。

5. 输出设计文档与实现规划（必须包含 mermaid）
   - 使用 `templates/FEATURE_DESIGN_DOC.md` 输出完整设计。
   - 必须给至少 1 张 mermaid 架构图（组件图/时序图/状态图择一或多张）。
   - 给出分阶段实现计划（可拆多 PR），每阶段包含：代码点位、测试、文档、风险与验证方式。

6. 方案评估与结论
   - 输出优点/缺点/风险清单与缓解措施。
   - 标注“开放问题（Open Questions）”与需要确认的外部约束。

# 输出约束（硬性）

- 必须显式讨论：向后兼容（Option/API/SPI）、性能副作用、失败恢复语义（尤其 streaming checkpoint）。
- 不确定的结论必须标注“待验证”，并给出最小验证方法（命令/用例/指标）。
