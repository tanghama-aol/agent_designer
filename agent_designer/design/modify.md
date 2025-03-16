### change1:
Agent组件分为场景agent和专家Agent，专家Agent由LPI组成workflow，而场景Agent由专家Agent组成workflow，并修改相应的数据库初始化脚本，
1. 场景Agent包括故障闭环Agent，由故障诊断，故障修复，业务恢复，修复验证，故障总结几个Agent组成
2. 专家Agent包括故障诊断Agent，故障修复Agent，业务恢复Agent，修复验证Agent，故障总结Agent
3. 故障诊断Agent调用故障诊断LPI，异步等待LPI， 诊断报告LPI，用户介入LPI，判断跳转LPI组成工作流，其他的专家Agent需要按设计工作流
4. 通用LPI包括用户介入LPI，异步等待LPI，记忆查询，记忆修改，条件跳转，无条件跳转几种
5. 都要写入数据库初始化脚本，并展现在左侧组件树中
6. Agent编辑器工作流和markdown编辑器放在tab中可切换
7. 编辑器的form需要紧凑一些，如一些输入框可以放在同一行