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

# 示例输出

## 行动计划摘要

- Phase 1：定义 `Option` 与 split/enumerator 基线实现
- Phase 2：补 writer/commit 语义与容错测试
- Phase 3：补 docs/en、docs/zh 与 E2E

## 风险清单

### 风险 1

- 引用：`seatunnel-connectors-v2/connector-mongodb/src/main/java/.../MongoSourceFactory.java:63`
- 问题描述：新增参数 `scan_full` 默认值拟从 `false` 改为 `true`。
- 潜在风险：破坏历史任务行为，触发非预期全量扫描。
- 最佳改进建议：保持默认值不变，仅新增显式配置控制。
- 严重程度：高

### 风险 2

- 引用：`seatunnel-connectors-v2/connector-mongodb/src/main/java/.../MongoSplitEnumerator.java:118`
- 问题描述：split 分配缺少上限控制。
- 潜在风险：高并发下产生过多 split，导致调度抖动。
- 最佳改进建议：增加 split 批量阈值并在日志输出当前队列长度。
- 严重程度：中

## merge 结论

- 结论：有条件合并
- 阻塞项：修正默认值兼容性并补 UT
- 建议项：补充性能基线说明
