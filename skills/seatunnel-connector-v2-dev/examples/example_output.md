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

## Connector-V2 检查结果

### 问题 1

- 引用：`seatunnel-connectors-v2/connector-redis/src/main/java/.../RedisConfig.java:58`
- 问题描述：`key_prefix` 未通过 `Option` 定义，直接硬编码读取。
- 潜在风险：配置不可发现，破坏参数稳定契约。
- 最佳改进建议：通过 `Option<String>` 定义配置名、默认值和描述。
- 严重程度：高
- 是否阻塞合并：是

### 问题 2

- 引用：`seatunnel-connectors-v2/connector-redis/src/main/java/.../RedisSinkWriter.java:141`
- 问题描述：`prepareCommit` 中无幂等去重标识。
- 潜在风险：故障恢复后重复写入。
- 最佳改进建议：引入 checkpoint-id 维度的幂等 key 或事务标识。
- 严重程度：中
- 是否阻塞合并：是

## 合并结论

- 结论：有条件合并
- 阻塞项：补齐 Option 定义、幂等语义、UT（参数校验/异常路径）
- 建议项：补充 docs/en 与 docs/zh 的配置示例
