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

# 文档格式规范（精简版）

本规范面向 SeaTunnel 文档贡献（尤其 connector 文档），目标是：

- 让文档结构统一、可读性强
- 让“注意事项/易踩坑点”突出显示
- 减少中英文文档不一致与示例错误

## 1. Admonitions（提示框）语法

推荐用三种提示框类型强调内容：

- `tip`：操作技巧 / 小建议
- `info`：补充解释 / 背景说明
- `caution`：注意事项 / 风险警告

示例：

```markdown
:::tip 提示
这里放操作技巧或经验建议
:::

:::info 备注
这里放补充解释、背景、更多细节
:::

:::caution 注意
这里放风险点、兼容性限制、需要额外小心的操作
:::
```

## 2. 文档一致性（强约束）

- 用户可见变更必须同步 `docs/en` + `docs/zh`。
- Option/参数名、类型、默认值、示例必须以代码为准（建议从 Option 定义处复制，避免手敲拼写错误）。
- 示例配置必须可运行（至少语法完整、括号/大括号闭合、必填项齐全）。

## 3. Connector 文档的最小结构建议

- 简介（做什么/不做什么）
- 支持的模式（batch/streaming、增量/全量、是否支持 checkpoint/Exactly-once 前提）
- 配置项（分组：连接、读取/写入、容错/重试、性能、语义）
- 示例配置（最小可跑 + 常见高级用法）
- 注意事项（用 `caution`：权限、幂等、schema 演进、性能陷阱）

## 4. 高频错误清单（来自近一年 Docs 变更）

- 示例配置括号/大括号不闭合（用户照抄即报错）
- Option/参数名漂移（代码已改名但文档未同步，或中英文不一致）
- 参数类型/默认值格式写错（尤其时间/日期格式、单位与范围）
- 代码块语言标记缺失导致渲染与复制体验差（建议标注 `hocon`/`json`/`sql`/`bash`）
