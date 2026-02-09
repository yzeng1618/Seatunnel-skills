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

## E2E 方案

- 用例：`KafkaToJdbcFailoverIT`
- 断言：failover 后总写入条数与唯一键集合不变
- 命令：`./mvnw -DskipUT -DskipIT=false verify`

## 需要补充的 UT 标准

### 问题 1

- 引用：`seatunnel-connectors-v2/connector-kafka/src/main/java/.../KafkaSourceConfig.java:47`
- 问题描述：缺少无效 offset 策略的参数校验单测。
- 潜在风险：E2E 失败时难定位到配置错误。
- 最佳改进建议：新增 `KafkaSourceConfigTest#shouldRejectInvalidOffsetMode`。
- 严重程度：高
- 是否阻塞合并：是

### 问题 2

- 引用：`seatunnel-e2e/seatunnel-connector-v2-e2e/src/test/java/.../KafkaToJdbcFailoverIT.java:133`
- 问题描述：仅有 happy-path，无提交失败异常路径覆盖。
- 潜在风险：故障语义可能回归。
- 最佳改进建议：增加 mock/UT 覆盖 `commit` 失败分支。
- 严重程度：中
- 是否阻塞合并：是

## merge 结论

- 结论：有条件合并
- 阻塞项：补齐 UT（参数校验 + 异常路径）并关联到 E2E 场景
- 建议项：增加容器日志采样输出以便排查 flaky
