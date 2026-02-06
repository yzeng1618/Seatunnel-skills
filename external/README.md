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

# external/

用于放置**本地工作区依赖**（例如上游仓库克隆），默认不纳入版本控制。

## 上游 SeaTunnel（本地分析用）

推荐在本地准备一份 SeaTunnel 源码（例如位于本项目根目录的 `seatunnel/` 或 `external/seatunnel/`），用于：

- 功能设计阶段：扫描“是否已有实现/相似实现”
- 贡献者洞察：分析近 1~2 年 commit 模式（source/sink/配置项/bugfix）

> 注意：`external/*` 与 `seatunnel/` 默认在 `.gitignore` 中忽略，避免把上游仓库内容提交进本项目。
