### change1:
Agent组件分为场景agent和专家Agent，专家Agent由LPI组成workflow，而场景Agent由专家Agent组成workflow，并修改相应的数据库初始化脚本，
1. 场景Agent包括故障闭环Agent，由故障诊断，故障修复，业务恢复，修复验证，故障总结几个Agent组成
2. 专家Agent包括故障诊断Agent，故障修复Agent，业务恢复Agent，修复验证Agent，故障总结Agent
3. 故障诊断Agent调用故障诊断LPI，异步等待LPI， 诊断报告LPI，用户介入LPI，判断跳转LPI组成工作流，其他的专家Agent需要按设计工作流
4. 通用LPI包括用户介入LPI，异步等待LPI，记忆查询，记忆修改，条件跳转，无条件跳转几种
5. 都要写入数据库初始化脚本，并展现在左侧组件树中
6. Agent编辑器工作流和markdown编辑器放在tab中可切换
7. 编辑器的form需要紧凑一些，如一些输入框可以放在同一行

### change2:
业务LPI包括：故障诊断LPI，诊断总结LPI，恢复方案仿真LPI，恢复方案LPI，恢复执行LPI， 修复方案LPI， 修复仿真LPI， 修复执行LPI， 故障验证LPI，故障总结LPI
通用LPI包括： 用户介入LPI，异步等待LPI，记忆查询，记忆修改，条件跳转，无条件跳转
场景Agent包括：故障处理闭环
专家Agent包括：故障诊断Agent，故障修复Agent，业务恢复Agent，修复验证Agent，故障总结Agent


更改reactflow没有边
index.mjs:153  [React Flow]: Couldn't create edge for source handle id: "undefined", edge id: e2. Help: https://reactflow.dev/error#008

### change3：
根据DiagnoseAgentWorkFlow.md生成相应的场景Agent，专家Agent，专家Agent对应的工作流
场景Agent用一级标题表示
专家Agent用二级标题表示
专家Agent对应的工作流包含阶段和任务，阶段用三级标题表示，任务是阶段下面的序列，包括序号和对应的LPI描述
编写翻译代码，根据Agent描述生成
backend/data/agent/生成场景Agent定义json
backend/data/agent/生成专家Agent定义json
backend/data/agent/生成专家Agent对应的工作流json
backend/data/lpi/busi/生成业务lpi定义json
backend/data/lpi/common/生成通用lpi定义json

修改相应的前后端代码，从data目录中读取场景Agent，专家Agent，业务LPI，通用LPI
修改专家Agent工作流显示reactflow，增加阶段节点，阶段节点横向排列， LPI节点作为阶段节点子节点，纵向排列
场景Agent工作流由专家Agent名字节点组成

通用LPI包括： 用户介入LPI，异步等待LPI，记忆查询LPI，记忆修改LPI，条件跳转LPI，无条件跳转LPI，下一步LPI
busi下的有些对应的通用LPI，如\backend\data\lpi\busi\busi_6.json，不是跳转6，是无条件跳转，参数为6，所以就是无条件跳转LPI，请修改busi下的LPI，去掉或移动到通用LPI下