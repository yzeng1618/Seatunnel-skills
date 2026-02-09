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

# LLM Context Guide for Apache SeaTunnel

This guide helps AI assistants (LLMs / Agents) make **safe, consistent, and verifiable** changes to the Apache SeaTunnel codebase. It mirrors practices from mature Apache projects and adapts them to SeaTunnel’s **build, testing, architecture, and documentation conventions**.

## Skills（渐进式披露）

本仓库提供一组可复用的 Skills（工作流/模板/参考资料），用于把“贡献开发指南 + Code Review + 质量门禁”标准化：

- `skills/README.md`：Skill 索引入口与通用输出约定
- `skills/seatunnel-code-review/`：按运行链路评审并输出可 merge 结论（要求 `path:line` 引用 + 严重程度）
- `skills/seatunnel-post-dev-audit/`：开发完成后的质量门禁自检（spotless/verify/test + 文档双语 + 兼容性检查）
- `skills/seatunnel-feature-design/`：功能设计/技术方案输出（含 mermaid 架构图与实现规划）
- `skills/seatunnel-bugfix-playbook/`：Bug 修复专项流程（最小复现、根因定位、修复策略、风险评估、验证回归与 merge 结论）

修改/新增 skills 后，建议运行：

```bash
python scripts/validate_skills.py
```

## ⚠️ CRITICAL: Validate Before Proposing Changes

**Agents MUST run verification commands locally before suggesting or finalizing changes.**

```bash
# Format code (mandatory)
./mvnw spotless:apply

# Quick verification (mandatory)
./mvnw -q -DskipTests verify

# Unit tests (strongly recommended)
./mvnw test
```

Failure to meet these requirements will likely result in PR rejection.

## Git Commit Message Convention

SeaTunnel follows a **strict commit message format** to maintain a clean and searchable history.

**Format**:

```
[Type][Module] Description

# Optional (recommended for connectors or fine-grained changes)
[Type][Module][SubModule] Description
```

### Types

* `Feature`  – New features
* `Fix`      – Bug fixes
* `Improve`  – Improvements to existing behavior
* `Docs`     – Documentation-only changes
* `Test`     – Test cases or test framework changes
* `Chore`    – Build, dependency, or maintenance tasks
* `Hotfix`   – Urgent fix (use sparingly)
* `Bug` / `Bugfix` – Bug fix (prefer统一用 `Fix`)
* `Refactor` – Refactor without behavior change

### Modules

* `Connector-V2`  – seatunnel-connectors-v2
* `Zeta`          – seatunnel-engine (Zeta engine)
* `Core`          – seatunnel-core
* `API`           – seatunnel-api
* `Common`        – seatunnel-common
* `Config`        – seatunnel-config / config
* `Transform-V2`  – seatunnel-transforms-v2
* `Format`        – seatunnel-formats
* `Translation`   – seatunnel-translation
* `E2E`           – seatunnel-e2e
* `CI`            – .github / seatunnel-ci-tools
* `Dist`          – seatunnel-dist
* `Shade`         – seatunnel-shade
* `Plugin`        – seatunnel-plugin-discovery / plugins
* `Tools`         – tools

### Examples

* `[Fix][Connector-V2] Fix MySQL source split enumeration bug`
* `[Fix][Zeta] Fix checkpoint timeout under heavy backpressure`
* `[Feature][Transform-V2] Add LLM transform plugin`
* `[Improve][Core] Optimize jar package loading speed`
* `[Docs] Update quick start guide`
* `[Feature][JDBC][Oracle] Support TIMESTAMP_TZ read in Source`

## Repository Structure

```text
seatunnel/
├── seatunnel-api/              # Core API definitions
├── seatunnel-common/           # Common utils & shared components
├── seatunnel-config/           # Configuration module
├── seatunnel-connectors-v2/    # Source & Sink connectors (main contribution area)
├── seatunnel-transforms-v2/    # Transform plugins (including LLM)
├── seatunnel-engine/           # Zeta engine & Web UI
├── seatunnel-core/             # Job submission & CLI entry points
├── seatunnel-dist/             # Distributions & packaging
├── seatunnel-translation/      # Flink & Spark adapters
├── seatunnel-formats/          # Data formats (JSON, Avro, etc.)
├── seatunnel-plugin-discovery/ # SPI plugin discovery/loading
├── seatunnel-shade/            # Shaded dependencies
├── seatunnel-e2e/              # End-to-End integration tests
├── seatunnel-examples/         # Local examples
├── seatunnel-ci-tools/         # CI helper tools
├── docs/                       # Documentation (en & zh)
├── tools/                      # Build/dev tools
└── config/                     # Default configurations
```

## Code Standards

### Java Backend

* **Formatting**: Google Java Format (AOSP style), enforced by Spotless
* **Imports**:
    * No wildcard imports
    * Use shaded dependencies: `org.apache.seatunnel.shade.*`
* **Nullability**: Avoid implicit null assumptions
* **Visibility**: Keep APIs minimal; prefer package-private when possible
* **Comments**: Add comments for important methods (public APIs, complex logic).

### Apache License Header (MANDATORY)

All **new files** MUST include the ASF license header:

```java
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
```

## 🚨 Backward Compatibility (VERY IMPORTANT)

Agents MUST treat backward compatibility as a **hard constraint**.

* DO NOT remove or rename existing config options
* DO NOT change default values casually
* DO NOT break public APIs or SPI contracts

Any incompatible change MUST:

* Be explicitly documented
* Be documented in `docs/en/introduction/concepts/incompatible-changes.md`
* Include migration guidance
* Be clearly explained in the PR description

## Dependency Rules

* DO NOT introduce new dependencies unless absolutely necessary
* Prefer existing shaded dependencies under `org.apache.seatunnel.shade.*`
* Any new dependency MUST:
    * Be justified in the PR description
    * Consider shading, size, and conflict risks

## Architecture Guidelines

### Connector (V2)

* Implement `SeaTunnelSource` or `SeaTunnelSink`
* Define configs using `Option`
* Support parallelism via `SourceSplitEnumerator`
* Avoid connector-specific logic leaking into engine or core

### Zeta Engine

* **Client**: Submits job config
* **Master**: Schedules & coordinates
* **Worker**: Executes tasks (Source → Transform → Sink)

Respect task boundaries and lifecycle semantics.

## Configuration (Option) Rules

* All user-facing configs MUST be defined using `Option`
* Each option MUST include:
    * name
    * type
    * default value (if applicable)
    * clear description
* Option names are **stable contracts** and must not be renamed lightly

## Error Handling & Logging

* Exceptions MUST include sufficient context (table, task, config key)
* Avoid swallowing exceptions
* Use proper log levels:
    * INFO  – lifecycle events
    * WARN  – recoverable issues
    * ERROR – task-failing errors
* NEVER log sensitive information (passwords, tokens, credentials)

## Documentation Rules

* Any user-visible change MUST update:

    * `docs/en`
    * `docs/zh`
* Config names, defaults, and examples MUST match the code exactly
* Documentation is part of the feature, not an afterthought

## Testing Guidelines

### Unit Tests

* Located under `src/test/java`
* Validate behavior, not implementation details
* Prefer deterministic and minimal tests

Command:

```bash
./mvnw test
```

### E2E Tests

* Located in `seatunnel-e2e`
* Uses Testcontainers
* Extend `TestSuiteBase`

Command:

```bash
./mvnw -DskipUT -DskipIT=false verify
```

## Performance Awareness

Agents MUST consider performance implications:

* Avoid unnecessary object creation in hot paths
* Be cautious with large in-memory buffers
* Consider parallelism and resource usage

## PR Scope Rule

* Keep changes minimal and focused
* Avoid unrelated refactors or formatting-only changes
* One PR should solve **one problem**

## Running & Debugging

### Build from Source

```bash
./mvnw clean install -DskipTests -Dskip.spotless=true
```

### Install Connectors

```bash
sh bin/install-plugin.sh $current_version
```

### Run Job (Zeta)

```bash
sh bin/seatunnel.sh --config config/v2.batch.config.template -e local
```
