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

使用 `$seatunnel-connector-v2-dev` 评审这个新 sink connector 设计：

- 目标：新增 Redis sink
- 变更：`RedisSink.java`、`RedisSinkWriter.java`、`RedisConfig.java`
- 要求：幂等写入、checkpoint 对齐、docs/en+zh、UT+E2E
