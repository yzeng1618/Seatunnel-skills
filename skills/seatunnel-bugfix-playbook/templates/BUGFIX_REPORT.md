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

# SeaTunnel Bug 修复报告模板

## 1. 问题概览

- 问题编号：
- 问题类型（correctness/data-loss/security/performance/stability）：
- 影响模块与范围：
- 严重程度（高/中/低）：

## 2. 最小复现

- 输入配置与数据：
- 操作步骤：
- 预期行为：
- 实际行为：
- 环境信息：

## 3. 根因分析（必须附证据）

- 根因描述：
- 证据 1：`path/to/File.java:line`
- 证据 2：`path/to/OtherFile.java:line`

## 4. 修复方案

- 方案说明：
- 为什么这是根因修复（而不是绕过）：
- 若含临时规避：退出条件与后续计划：

## 5. 风险与兼容性

- 兼容性影响（Option/API/SPI/默认值）：
- 性能副作用：
- 容错与恢复语义影响：
- 依赖与安全日志影响：

## 6. 测试与验证

- 新增/修改单测：
- 新增/修改集成与 E2E：
- 命令执行摘要（spotless/verify/test）：
- 手工验证摘要：

## 7. 文档与发布

- docs/en 更新：
- docs/zh 更新：
- 不兼容变更记录与迁移说明（如有）：
- backport/release note（如有）：

## 8. 合并结论

- 阻塞项：
- 建议项：
- 是否可 merge（建议合并 / 有条件合并 / 不建议合并）：
