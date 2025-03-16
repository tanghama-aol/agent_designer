# Agent设计器

Agent设计器是一个可视化的Agent编辑工具，用于设计和管理LPI、Agent和通用组件，支持工作流编排和执行。

## 项目结构

```
agent_designer/
├── apiserver/         # 示例API服务器
├── backend/           # 后端服务
│   ├── controllers/   # 控制器
│   ├── models/        # 数据模型
│   ├── services/      # 业务逻辑
│   ├── app.py         # 应用入口
│   ├── config.py      # 配置文件
│   └── init_data.py   # 初始化数据脚本
└── frontend/          # 前端应用
    ├── public/        # 静态资源
    └── src/           # 源代码
        ├── components/# 组件
        ├── pages/     # 页面
        └── services/  # 服务
```

## 功能特性

- 组件管理：创建、编辑、删除LPI、Agent和通用组件
- 工作流编排：可视化设计Agent工作流
- 工作流执行：测试和执行工作流
- 配置管理：管理大模型和存储配置

## 快速开始

### 1. 安装依赖

#### 后端依赖

```bash
cd agent_designer/backend
pip install -r requirements.txt
```

#### 前端依赖

```bash
cd agent_designer/frontend
npm install
```

#### API服务器依赖

```bash
cd agent_designer/apiserver
pip install -r requirements.txt
```

### 2. 启动服务

#### 启动API服务器（示例API）

```bash
cd agent_designer/apiserver
python app.py
```

API服务器将在 http://localhost:8000 上运行。

#### 初始化后端数据

```bash
cd agent_designer/backend
python init_data.py
```

#### 启动后端服务

```bash
cd agent_designer/backend
python app.py
```

后端服务将在 http://localhost:5000 上运行。

#### 启动前端服务

```bash
cd agent_designer/frontend
npm start
```

前端服务将在 http://localhost:3000 上运行。

### 3. 访问应用

打开浏览器访问 http://localhost:3000 即可使用Agent设计器。

## 使用指南

### 组件管理

1. 在左侧组件树中可以查看所有组件
2. 点击"+"按钮可以创建新组件
3. 点击组件可以在右侧查看和编辑组件详情

### 工作流设计

1. 选择一个Agent组件
2. 在工作流标签页中可以设计工作流
3. 拖拽节点到画布上创建工作流
4. 连接节点定义执行流程
5. 保存工作流后可以测试执行

### 系统配置

1. 点击右上角的"配置"按钮
2. 设置大模型参数和存储目录
3. 保存配置后生效

## 示例

系统初始化后包含以下示例组件：

- LPI组件：故障诊断API、业务恢复API、故障修复API、修复验证API、故障总结API
- Agent组件：故障处理Agent（包含完整工作流）

可以通过这些示例了解系统的基本使用方法。 