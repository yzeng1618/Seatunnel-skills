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

## 发现的问题

### 问题 1

- 引用：`seatunnel-connectors-v2/connector-kafka/src/main/java/org/apache/seatunnel/connectors/seatunnel/kafka/sink/KafkaSinkWriter.java:176`
- 问题描述：flush 在 checkpoint 前无超时控制。
- 潜在风险：broker 抖动时卡住 checkpoint，影响任务恢复。
- 最佳改进建议：为 flush 添加超时与可中断处理，并记录 task/split 上下文。
- 严重程度：高
- 是否阻塞合并：是

### 问题 2

- 引用：`seatunnel-connectors-v2/connector-kafka/src/main/java/org/apache/seatunnel/connectors/seatunnel/kafka/sink/KafkaCommitter.java:92`
- 问题描述：`Exception` 直接吞并并返回成功状态。
- 潜在风险：提交失败被误判为成功，造成数据一致性问题。
- 最佳改进建议：失败时抛出带 topic/partition 信息的异常。
- 严重程度：中
- 是否阻塞合并：是

## 合并结论

- 结论：不建议合并
- 阻塞项：修复问题 1 与问题 2，并补 checkpoint 失败回归测试。
- 建议项：补充 docs/en 与 docs/zh 的失败语义说明。
