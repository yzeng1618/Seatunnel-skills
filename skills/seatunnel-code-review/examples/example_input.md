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

使用 `$seatunnel-code-review` 评审下面改动并给出可 merge 结论：

- PR：修复 Kafka sink 提交延迟问题
- diff 涉及：
  - `seatunnel-connectors-v2/connector-kafka/.../KafkaSinkWriter.java`
  - `seatunnel-connectors-v2/connector-kafka/.../KafkaCommitter.java`
- 关注点：checkpoint 一致性、异常处理、性能副作用
