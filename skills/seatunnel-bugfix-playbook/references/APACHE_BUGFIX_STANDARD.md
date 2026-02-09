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

# Apache 项目 Bug 修复标准（统一抽象）

本文件基于其他 Apache 项目的公开贡献规范，提炼通用 Bug 修复标准，用于 SeaTunnel bugfix 场景对齐。

## 1. 来源项目与链接

- Apache Flink PR 模板（Issue 绑定、测试验证、兼容与性能影响声明）  
  `https://raw.githubusercontent.com/apache/flink/master/.github/PULL_REQUEST_TEMPLATE.md`
- Apache Spark 贡献指南（可复现 bug 报告、根因收敛、回归/性能基准）  
  `https://spark.apache.org/contributing.html`
- Apache Kafka 开发者贡献指南（Issue 上下文、测试与文档同步、兼容性意识）  
  `https://kafka.apache.org/community/developer/`
- Apache Beam PR 模板与贡献指南（Issue 链接、变更日志、CI 健康、测试要求）  
  `https://raw.githubusercontent.com/apache/beam/master/.github/PULL_REQUEST_TEMPLATE.md`  
  `https://raw.githubusercontent.com/apache/beam/master/CONTRIBUTING.md`

## 2. 跨项目共性标准

1. 问题追踪绑定
   - PR 必须关联 Issue/JIRA，并在描述中明确目标与范围。
2. 单问题单 PR
   - 每个 PR 只修一个核心问题，避免混入无关重构。
3. 可复现与根因导向
   - Bug 必须可复现；修复应收敛到根因，而不是仅绕过表象。
4. 测试闭环
   - 新增或修改行为需要测试覆盖（UT/IT/E2E）；对性能回归问题需要基准或可比较证据。
5. 影响面显式声明
   - 显式声明 API/序列化/依赖/运行时热路径/部署恢复等影响。
6. 文档与发布信息同步
   - 用户可见行为变化必须同步文档；重要变化进入变更日志或 release note。

## 3. SeaTunnel 统一 Bugfix 标准（执行版）

### A. 立项与范围

- 关联 Issue 或在 PR 描述给出问题编号。
- 标记问题级别：correctness、data-loss、security、performance regression、stability。

### B. 复现与证据

- 给出最小复现（配置、输入、触发步骤、预期/实际、环境信息）。
- 报告中对根因提供 `path:line` 证据。

### C. 修复设计

- 首选根因修复；临时规避必须说明退出条件与后续计划。
- 禁止在同一 PR 混入无关优化或重构。

### D. 风险与兼容

- 逐项检查：Option/API/SPI、序列化状态、默认值、性能热路径、依赖与安全日志。
- 对 streaming/checkpoint/recovery 语义变更必须给出明确说明。

### E. 验证与回归

- 至少覆盖修复点 UT；必要时补 IT/E2E。
- 对性能回归修复给出 benchmark 或对比数据。

### F. 文档与发布

- 用户可见变化同步 `docs/en` + `docs/zh`。
- 必要时补充不兼容变更记录、迁移说明、release note、backport 说明。

## 4. Merge 判定基线

- 可 merge：复现明确、根因证据明确、测试闭环完整、风险受控、文档同步完成。
- 有条件 merge：存在非阻塞遗留项，但有明确跟踪 issue 与截止计划。
- 不建议 merge：缺少复现或根因证据、测试不足、兼容性风险未闭环。
