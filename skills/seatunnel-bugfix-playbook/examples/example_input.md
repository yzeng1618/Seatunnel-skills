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

# 示例输入

请使用 `$seatunnel-bugfix-playbook` 帮我输出修复报告：

- 现象：MySQL source 在 streaming 模式下偶发重复消费。
- 变更：`seatunnel-connectors-v2/connector-jdbc/.../MysqlSourceReader.java`
- 期望：checkpoint 恢复后不重复提交已处理 offset。
- 已知失败日志：`duplicate primary key on sink`。
