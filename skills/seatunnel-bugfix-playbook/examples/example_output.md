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

## 1. 问题概览

- 问题类型：correctness
- 严重程度：高

## 2. 根因分析（证据）

- 证据 1：`seatunnel-connectors-v2/connector-jdbc/src/main/java/org/apache/seatunnel/connectors/seatunnel/jdbc/source/MysqlSourceReader.java:214`
- 证据 2：`seatunnel-engine/seatunnel-engine-server/src/main/java/org/apache/seatunnel/engine/server/checkpoint/CheckpointCoordinator.java:337`

## 3. 风险与建议

- 问题描述：reader 在 `snapshotState` 后仍可能推进本地 offset。
- 潜在风险：恢复后重复读取，导致下游主键冲突。
- 改进建议：将 offset 推进与 checkpoint barrier 对齐，并在恢复时只从已确认 offset 继续。
- 严重程度：高

## 4. 合并结论

- 阻塞项：补充“恢复后不重复消费”的回归 UT。
- 建议项：补 1 条 E2E 覆盖 checkpoint failover。
- 是否可 merge：有条件合并
