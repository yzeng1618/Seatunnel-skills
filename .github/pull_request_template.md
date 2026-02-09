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

# Skill Repo Change (Default)

本默认模板用于 **yzeng1618/Seatunnel-skills** 仓库改动。

如你要填写“贡献 Apache SeaTunnel 主仓库”的 checklist，请改用：

- `.github/PULL_REQUEST_TEMPLATE/seatunnel_upstream_change.md`

## 1. 概览

- 变更类型（Feature/Fix/Improve/Docs/Test/Chore）：
- 影响范围（skills/scripts/docs/.github）：
- 影响的 skill：

## 2. 必跑校验

- [ ] `python scripts/validate_skills.py`
- [ ] `python scripts/generate_skills_index.py`
- [ ] `python scripts/validate_skills.py --check-index`

## 3. 兼容性与规范

- [ ] `SKILL.md` front-matter 字段齐全且 `name` 与目录一致
- [ ] `templates/references/agents` 路径均可解析到真实文件
- [ ] 如存在 `DISABLED`，已说明原因与恢复计划

## 4. 关键说明

- 主要改动：
- 风险与回滚：
- 额外上下文：
