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

# SeaTunnel E2E 编写指南（精简版）

## 1. 设计原则

- 目标明确：一个用例验证一个核心行为（避免“全能大用例”）。
- 可重复：可在本地与 CI 重复运行；避免依赖外部不可控环境。
- 可诊断：失败时能快速定位（日志、断言信息、容器状态）。

## 2. Testcontainers 使用要点

- 容器生命周期：创建、等待就绪（healthcheck/端口）、销毁必须可靠。
- 资源隔离：端口、临时目录、topic/table 名称要避免冲突（用随机后缀/namespace）。
- 超时策略：对启动、读写、checkpoint 等关键阶段设置合理超时，避免无限等待。

## 3. Flaky 规避清单

- 避免依赖 wall clock 时间窗口做断言；优先轮询“条件达成”。
- 避免共享外部状态；每次运行使用独立资源（表名、bucket、topic）。
- 失败时打印必要上下文（容器日志、关键配置、任务状态）。

## 4. 近一年高频不稳定原因（经验规则）

- **超时与时序**：ConditionTimeout/等待资源就绪超时很常见；优先“await 条件达成”而不是固定 sleep。
- **镜像与版本**：CI 失败经常与 docker image/tag 变动相关；尽量使用稳定来源与固定版本，避免隐式升级。
- **资源清理**：容器删除/网络释放冲突会导致偶发失败；确保 teardown 可靠，并避免多个用例共享同一外部资源名。
- **日志与诊断**：失败时必须能看到“关键阶段 + 关键配置 + 容器日志”三要素，否则很难定位 flaky 根因。

## 4. 运行与结果记录

```bash
./mvnw -DskipUT -DskipIT=false verify
```

- 在 PR 中记录命令与关键输出摘要；若失败，给出复现步骤与修复计划。
