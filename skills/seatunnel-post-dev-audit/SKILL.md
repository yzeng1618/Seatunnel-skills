---
name: seatunnel-post-dev-audit
description: 开发完成后的 SeaTunnel 规范性与质量门禁自检（spotless/verify/test、兼容性、文档双语、依赖与日志脱敏）。当准备提交或合并 PR、需要输出自检报告与是否可合并结论时使用。
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

- 在提交/合并前完成“可验证的质量门禁”，减少 review 往返。
- 输出一份可复制的自检报告（包含执行过的命令与结论）。

# 工作流（按顺序执行）

1. 明确变更属性
   - 标注变更类型与模块范围（Core/Zeta/Connector-V2/Transform-V2/Format/Translation/E2E/Docs）。
   - 如果涉及用户可见变更（配置、语义、默认值、行为），提前准备 docs/en + docs/zh 的更新。

2. 运行本地质量门禁
   - 按 `references/VERIFY_COMMANDS.md` 执行格式化与构建校验；记录命令与结果。
   - 如涉及外部系统或容错：补充 IT/E2E 验证与结果。

3. 兼容性与风险自检
   - 检查是否修改 config 名称/默认值/SPI；如有，提供迁移/回滚方案与文档记录。
   - 检查依赖：避免新增依赖；优先使用 `org.apache.seatunnel.shade.*`；确认无冲突风险。
   - 检查日志：不输出敏感信息；错误信息包含足够上下文。

4. 输出自检报告
   - 使用 `templates/POST_DEV_AUDIT_REPORT.md` 输出结果。
   - 给出“是否可合并结论”与剩余风险/待办。

