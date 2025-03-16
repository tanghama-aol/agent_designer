# Agent设计器应用

一个用于设计和管理AI Agent的可视化编辑平台。

## 项目结构
```
backend/
├── app.py
├── config.py
├── models/
│   ├── __init__.py
│   ├── agent.py
│   ├── component.py
│   └── workflow.py
├── controllers/
│   ├── __init__.py
│   ├── component_controller.py
│   └── workflow_controller.py
├── services/
│   ├── __init__.py
│   ├── component_service.py
│   └── workflow_service.py
└── requirements.txt
```

## 功能特点

- LPI（语言处理接口）设计
- Agent设计和配置
- 工作流可视化编辑
- 通用组件库
- 配置化管理

## 项目结构

- 前端：基于React + Ant Design + React Flow Renderer
- 后端：基于Flask + SQLite + SQLAlchemy

## 开发环境搭建

### 前端
```bash
#安装依赖
npm install
#启动开发服务器
npm run dev
#构建生产版本
npm run build
```

### 后端
```bash
#创建虚拟环境
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate
#安装依赖
pip install -r requirements.txt
#启动服务
python backend/app.py
```


## 配置说明

在前端界面的"配置"选项中可以设置以下内容：

1. 大模型配置
   - 支持OpenAI、Azure OpenAI、Claude等
   - 需配置API密钥和基础URL

2. 存储配置
   - 配置组件和工作流的存储位置

## 使用指南

1. 在左侧菜单创建或选择组件
2. 在右侧编辑区进行详细配置
3. 对于Agent，可以配置基本信息和工作流
4. 使用工作流编辑器可视化设计Agent的执行流程
5. 保存并发布您的组件

## 技术栈

- 前端：React、Ant Design、React Flow Renderer
- 后端：Flask、SQLite、SQLAlchemy

