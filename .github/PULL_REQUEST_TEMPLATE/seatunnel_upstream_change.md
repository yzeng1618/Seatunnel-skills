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

# 变更说明

## 1. 概览

- 目标/动机：
- 变更类型（Fix/Feature/Improve/Docs/Test/Chore）：
- 影响模块（API/Core/Zeta/Connector-V2/Transform-V2/Format/Translation/E2E/Docs/Config/Common/CI/Dist/Plugin/Shade/Tools）：
- 影响运行模式（batch/streaming，本地/集群，Zeta/Flink/Spark）：

## 2. 兼容性影响（必填）

- [ ] 未修改配置项名称/默认值/语义（如有修改，请说明迁移与回滚方案）
- [ ] 未破坏公共 API / SPI（如有修改，请说明兼容策略）
- [ ] 如为不兼容变更：已补充迁移说明与不兼容变更记录（若适用）

## 3. 性能/副作用（必填）

- 是否可能引入额外 IO/RPC/序列化/锁竞争/内存占用？
- 是否影响 backpressure / checkpoint / 吞吐 / 延迟？
- 是否引入资源泄露风险（连接、线程、文件句柄、buffer）？

## 4. 错误处理与日志（必填）

- [ ] 异常包含足够上下文（table/task/config key/split id 等）
- [ ] 日志级别合理，且不会泄露敏感信息（密码/token/连接串）

## 5. 测试与验证（粘贴真实结果摘要）

```bash
./mvnw spotless:apply
./mvnw -q -DskipTests verify
./mvnw test
```

- spotless: ✅/❌
- verify: ✅/❌
- test: ✅/❌

如涉及 E2E/外部系统/容错：

```bash
./mvnw -DskipUT -DskipIT=false verify
```

- e2e/it: ✅/❌

## 6. 文档更新（用户可见变更必填）

- docs/en：是/否（列出文件）
- docs/zh：是/否（列出文件）

## 7. 回滚/降级方案（可选但推荐）

- 回滚策略：
- 监控指标/告警建议：

---

## 可选：快速生成 Review 报告（给评审者）

如需结构化评审输出，可在对话中使用：

- `$seatunnel-code-review`（评审报告：核心逻辑/兼容性/副作用/错误处理/测试与文档/架构合理性）
- `$seatunnel-post-dev-audit`（开发后自检：质量门禁与可合并结论）
