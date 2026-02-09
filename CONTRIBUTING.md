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

# 贡献指南（Seatunnel-skills）

本仓库用于维护面向 **Apache SeaTunnel** 的 Agent Skills、模板和参考资料。

## 1. 新增/修改 Skill 的目录约定

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml                 # 可选但推荐
  references/*.md                    # 可选
  templates/*.md                     # 可选
  examples/example_input.md          # 必须
  examples/example_output.md         # 必须
```

## 2. SKILL.md front-matter 规范（必填）

`SKILL.md` 第一段必须是 YAML front-matter，字段如下：

- `name`：必须，且与目录名一致
- `description`：必须，一行摘要
- `when_to_use`：必须，触发条件
- `inputs_required`：必须，数组
- `templates`：必须，数组（可空）
- `references`：必须，数组（可空）
- `agents`：必须，数组（可空）
- `version`：可选

示例：

```yaml
---
name: seatunnel-code-review
description: 基于 Apache SeaTunnel 运行链路进行代码评审。
when_to_use: 当需要对 SeaTunnel PR/diff 输出结构化评审结论时使用。
inputs_required:
  - PR 链接或 diff
  - 变更背景
templates:
  - templates/REVIEW_REPORT.md
references:
  - references/RUNTIME_FLOW.md
agents:
  - agents/openai.yaml
version: "1.0.0"
---
```

约束：

- `templates` / `references` / `agents` 必须是 skill 目录内的相对文件路径。
- `name` 必须是 hyphen-case，且和目录名一致。

## 3. DISABLED 机制

若 skill 目录存在 `DISABLED` 文件：

- `python scripts/validate_skills.py` 会跳过该 skill；
- `python scripts/generate_skills_index.py` 不会把该 skill 写入索引。

用于临时下线，不建议长期保留。

## 4. 本地校验与索引更新（必跑）

```bash
python scripts/validate_skills.py
python scripts/generate_skills_index.py
python scripts/validate_skills.py --check-index
```

可选：一次性检查并修复 README 索引漂移：

```bash
python scripts/validate_skills.py --check-index --fix-index
```

兼容旧格式（无 front-matter）仅用于过渡：

```bash
python scripts/validate_skills.py --allow-legacy-no-frontmatter
```

## 5. PR 模板

- 本仓库改动：`.github/PULL_REQUEST_TEMPLATE/skill_repo_change.md`
- SeaTunnel 上游参考模板：`.github/PULL_REQUEST_TEMPLATE/seatunnel_upstream_change.md`

默认模板 `.github/pull_request_template.md` 面向本仓库提交。
