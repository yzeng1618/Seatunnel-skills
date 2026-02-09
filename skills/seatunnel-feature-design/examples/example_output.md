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

## 设计结论

- 采用“全量快照 + CDC 衔接”双阶段方案。
- 保持现有 Option 名称不变，只新增可选参数 `snapshot.chunk.size`。

## 风险项

### 风险 1

- 引用：`seatunnel-connectors-v2/connector-jdbc/src/main/java/.../JdbcSourceFactory.java:89`
- 问题描述：新增参数默认值可能扩大单批加载数据量。
- 潜在风险：启动阶段内存峰值升高。
- 最佳改进建议：默认值保持小批量，并加入上限保护。
- 严重程度：中

### 风险 2

- 引用：`seatunnel-engine/seatunnel-engine-server/src/main/java/.../CheckpointCoordinator.java:412`
- 问题描述：CDC 衔接点未绑定 checkpoint barrier。
- 潜在风险：故障恢复可能出现重放窗口。
- 最佳改进建议：在 barrier 对齐后再推进衔接位点。
- 严重程度：高

## merge 结论

- 结论：有条件合并
- 阻塞项：先补 checkpoint 对齐语义验证
- 建议项：补充压测计划与回滚脚本
