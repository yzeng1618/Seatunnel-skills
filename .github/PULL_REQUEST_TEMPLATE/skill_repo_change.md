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

# Skill Repo Change

## 1. 概览

- 变更类型（Feature/Fix/Improve/Docs/Test/Chore）：
- 影响范围（skills/scripts/docs/.github）：
- 影响的 skill（可多项）：
  - [ ] `skills/seatunnel-code-review`
  - [ ] `skills/seatunnel-post-dev-audit`
  - [ ] `skills/seatunnel-feature-design`
  - [ ] `skills/seatunnel-bugfix-playbook`
  - [ ] `skills/seatunnel-connector-v2-dev`
  - [ ] `skills/seatunnel-e2e-authoring`
  - [ ] `skills/seatunnel-contributor-playbook`
  - [ ] 其他（请写明）：

## 2. 结构与兼容性检查

- [ ] 新增/修改的 `SKILL.md` 已包含 front-matter 必填字段
- [ ] `templates` / `references` / `agents` 路径均存在且为相对路径
- [ ] 如使用 `DISABLED`，已在 PR 说明原因和恢复计划
- [ ] 如改动了 `skills/README.md` 自动区块，来自脚本生成而非手工编辑

## 3. 本地验证（必填）

```bash
python scripts/validate_skills.py
python scripts/generate_skills_index.py
python scripts/validate_skills.py --check-index
```

- validate_skills: ✅/❌
- generate_skills_index: ✅/❌
- validate --check-index: ✅/❌

## 4. 影响与风险

- 是否影响 Agent 触发稳定性（name/description/when_to_use）？
- 是否影响输出格式约束（path:line、严重程度、merge 结论）？
- 是否影响现有文档链接与模板可用性？

## 5. 说明（可选）

- 关键变更点：
- 后续计划：
- 回滚方式：

---

如果你要提交的是 **Apache SeaTunnel 主仓库变更说明模板**，请使用：

- `.github/PULL_REQUEST_TEMPLATE/seatunnel_upstream_change.md`
