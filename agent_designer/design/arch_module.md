# aiChatOps支持Agent框架

AIChatOPS需要增加Agent框架支持。
Copilot支持多级Agent组合（场景Agent、专家Agent、能力Agent）。
Agent框架需要支持的业务场景和操作场景包括：故障闭环、网络变更闭环、报表助手、质差助手。
多Agent协作通过pipeline配置来控制。
引入技术组件包括Copilot、专家Agent、能力Agent、意图生命周期管理、意图识别与补全、工作流引擎。

##### 涉及模块

chatbot：外部模块
   1. 输入输出模块，以机器人的方式启动Agent任务，显示Agent执行过程
   2. Agent用户介入时和用户交互

copilot: 
    1. 意图识别，识别chatbot输入的自然语言对话的意图
    2. Agent路由： 根据意图识别路由消息到不同的Agent, 包括场景Agent，专家Agent，text2API，text2Rag 

场景Agent:
    1. 组织专家Agent流程形成应用场景
    2. 管理场景下的专家Agent

专家Agent：
    1. 被场景Agent或copilot调用
    2. 通过工作流组织处理步骤，步骤包括调用API，调用其他专家Agent，调用能力Agent, 分支算子处理， 用户介入
    3. 工作流生命周期管理

UME：外部模块
    1. 提供AP供调用
    2. 提供API内部思维链过程
        


##### 流程1 Agent框架主流程
0. 用户在chatbot输入Agent闭环请求，如故障处理
1. chatbot将用户输入和上下文请求copilot
2. copilot进行意图识别，找到对应的场景Agent
3. copilot根据场景Agent的输入要求，计算参数需求
4. 如果参数缺少，想copilot弹对话框要求用户补全参数
5. 参数完整后，copilot将请求消息转发到场景Agent
6. 场景Agent根据pipeline定义专家Agent路径，执行专家Agent
7. 专家Agent根据专家Agent工作流处理消息，调用LPI执行步骤
8. 专家Agent处理完成，返回场景Agent
9. 场景Agent根据pipeline定义执行下一个专家Agent，直到完成pipeline定义的专家Agent
10. 场景Agent将结果返回给Chatbot

##### 流程2 用户介入
0. 专家Agent在处理节点过程中，LPI返回需要介入
1. 专家Agent调用用户介入Agent，输入上下文，当前任务状态，用户介入界面内容。
2. 专家Agent返回等待用户介入，终止处理流程
3. 用户介入Agent调用任务中心，保存当前任务上下文
4. 用户介入Agent调用chatbot回调界面函数
5. chatbot根据用户介入Agent的界面生成界面
6. 用户操作chatbot界面做确认
7. chatbot向copilot发送用户确认回调消息，包含对应的场景Agent，专家Agent，任务id，确认结果
8. copilot根据任务id读取上下文， 根据Agent名直接路由对应Agent
9. Agent根据上下文和用户确认结果恢复执行环境，继续执行工作流

#### 流程3 专家工作流
0. 专家Agent接收消息，如果是首条消息，则开始执行工作流第一步
1. 如果是用户介入的中间消息，则恢复上下文，并跳转到相应步骤下一步开始继续执行
2. 按序执行步骤，判断节点类型
3. 如果是LPI，则调用LPI对应的函数执行
4. 如果是多步请求，则调用思维链Agent生成思维链并执行
4. 如果是单步自然语言请求，则调用text2apiAgent
5. 如果是用户介入，则调用用户介入Agent，流程结束
6. 如果是判断跳转，则执行判断并根据判断结果跳转到相应的步骤
7. 每步执行保存执行结果到上下文中
8. 调用chatbot回调接口更新Agent的执行过程界面