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

# Connector 集成检查清单（Connector-V2）

适用场景：

- 新增 Connector-V2（Source/Sink）
- 为 connector 增加新模块/新 jar 产物
- 需要把 connector 能力“集成到发行物/插件体系/CI”中

## 1. 发布/插件体系（必须）

- 更新 `plugin-mapping.properties`：注册新 connector 信息
- 更新 `seatunnel-dist/pom.xml`：确保发行包包含对应依赖与插件
- 更新 `config/plugin_config`：补充插件配置映射（如项目约定需要）

## 2. CI/Label（建议但强烈推荐）

- 更新 `.github/workflows/labeler/label-scope-conf.yml`：让 PR 自动打上正确 scope（便于 review 与统计）

## 3. E2E（强烈推荐）

- 为新增 connector 增加或更新 e2e 用例（`seatunnel-e2e/seatunnel-connector-v2-e2e/`）
- 让 e2e 覆盖关键语义与全量数据类型（最小、确定性、可诊断）

## 4. 文档（用户可见即必须）

- 同步更新 `docs/en` + `docs/zh` 的 connector 文档与示例
- 文档格式建议：见 `references/DOCS_FORMAT_SPEC.md`

## 5. License（有新 jar 必须）

- 新增二进制 jar / 新依赖时：补齐 License/Notice（遵循项目的 New License Guide）

