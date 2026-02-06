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

# 功能设计 Checklist（SeaTunnel）

## 1. 兼容性（硬约束）

- 配置项（Option）名称/默认值/语义是否稳定？是否可能造成“无感行为变化”？
- 是否影响公共 API/SPI（seatunnel-api）？如何保证兼容或提供迁移？
- streaming：状态结构是否可升级？checkpoint/恢复语义是否改变？

## 2. 性能与副作用（热路径）

- 是否引入额外 IO/RPC/序列化/锁竞争/内存占用？
- 在 enumerator/reader/writer 热路径是否存在全量缓存、频繁日志、不必要对象创建？
- 是否可能恶化 backpressure / checkpoint 时延 / 吞吐？

## 3. 错误处理与可诊断性

- 异常是否包含足够上下文（table、task、config key、split id、并行度）？
- 是否存在吞异常/静默失败？
- 日志是否可能泄露敏感信息（密码/token/连接串）？

## 4. 测试与文档

- 是否有 UT 覆盖关键行为与异常路径？
- 是否需要 IT/E2E 覆盖外部系统、容错恢复、并行 split、commit 语义？
- 用户可见变更是否更新 docs/en 与 docs/zh？示例是否准确？

## 5. 运维与回滚

- 是否提供可观测性（指标/日志）与告警建议？
- 回滚/降级是否可行？是否会留下脏数据或造成不一致？

