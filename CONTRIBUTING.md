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

本仓库用于维护面向 **Apache SeaTunnel** 的 Agent Skills、评审模板与参考资料，目标是让贡献与 Code Review 更一致、更可验证。

## 1. 新增/更新 Skill

### 1.1 目录约定

每个 skill 必须是一个独立目录：

```text
skills/<skill-name>/
  SKILL.md                 # 必须：YAML frontmatter + 工作流正文
  agents/openai.yaml       # 推荐：UI 元数据（display_name/short_description/default_prompt）
  references/*.md          # 可选：按需加载的参考资料
  templates/*.md           # 可选：产出模板（报告/清单）
```

### 1.2 SKILL.md 规范（强约束）

- 文件第一行必须是 `---`，且包含 YAML frontmatter。
- frontmatter 只保留 `name` 与 `description`（建议）。
- `name` 必须是 hyphen-case（小写字母/数字/短横线），例如 `seatunnel-code-review`。
- `description` 请覆盖“何时使用”的触发词（如：code review / PR / diff / 评审 / 自检）。

> 注意：为兼容 frontmatter 解析，ASF License Header 请放在 frontmatter **之后**（用 HTML 注释）。

### 1.3 agents/openai.yaml（可选但推荐）

- 仅保留 `display_name`、`short_description`、`default_prompt` 即可。
- 约束：字符串值必须加引号；`default_prompt` 必须显式包含 `$skill-name`。

## 2. 新文件 License Header（必须）

本仓库新增文件必须包含 ASF License Header：

- Markdown：使用 HTML 注释 `<!-- ... -->`。
- YAML / gitignore：使用 `#` 注释。
- 对于 `SKILL.md`：把 License Header 放在 YAML frontmatter 后，以免破坏解析。

## 3. 本地校验（推荐）

修改/新增 skill 后，建议运行：

```bash
python scripts/validate_skills.py
```

### 3.1 禁用 Skill（不建议，但可用）

如果某个 skill 需要下线但暂时无法删除，可在 skill 目录下新增 `DISABLED` 文件；`scripts/validate_skills.py` 会跳过该目录。

## 4.（可选）准备上游 SeaTunnel 用于本地分析

如需做功能设计“查重”或对齐近期变更热点，可在本地工作区准备一份上游 SeaTunnel 源码（例如位于本项目根目录的 `seatunnel/` 或 `external/seatunnel/`）。

说明：`external/README.md`

## 5. 提交/Review 建议

- PR 尽量小而聚焦（一个 PR 解决一个问题）。
- 模板与清单类变更：请在 PR 描述里说明“新增/修改点”和“预期对贡献者的影响”。
