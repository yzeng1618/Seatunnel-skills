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

## 门禁结果

- spotless: ✅
- verify: ✅
- test: ❌（1 failed）

## 发现问题

### 问题 1

- 引用：`seatunnel-connectors-v2/connector-elasticsearch/src/main/java/.../ElasticsearchSinkConfig.java:73`
- 问题描述：新增 `retry_backoff_ms` 未补 docs/zh。
- 潜在风险：中英文文档不一致，用户配置误解。
- 最佳改进建议：同步更新 `docs/en` 和 `docs/zh` 参数表。
- 严重程度：中
- 是否阻塞合并：是

### 问题 2

- 引用：`seatunnel-connectors-v2/connector-elasticsearch/src/test/java/.../ElasticsearchSinkWriterTest.java:126`
- 问题描述：失败用例断言过弱，仅校验异常类型。
- 潜在风险：回归时无法定位重试语义偏移。
- 最佳改进建议：补充重试次数与最终状态断言。
- 严重程度：中
- 是否阻塞合并：是

## merge 结论

- 结论：有条件合并
- 阻塞项：修复失败 UT，并补齐 docs/en + docs/zh
- 建议项：追加一次 `-DskipUT -DskipIT=false verify`
