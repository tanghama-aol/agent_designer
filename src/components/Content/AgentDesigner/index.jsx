import React, { useState, useCallback } from 'react';
import { Form, Input, Select, Button, Card, Tabs } from 'antd';
import ReactFlow, { 
  addEdge, 
  Background, 
  Controls, 
  MiniMap 
} from 'react-flow-renderer';
import { PlusOutlined } from '@ant-design/icons';
import './index.css';

const { TabPane } = Tabs;
const { TextArea } = Input;
const { Option } = Select;

// 自定义节点类型
const nodeTypes = {
  startNode: StartNode,
  endNode: EndNode,
  lpiNode: LPINode,
  agentNode: AgentNode,
  commonNode: CommonNode,
};

function StartNode({ data }) {
  return (
    <div className="custom-node start-node">
      <div className="node-header">开始</div>
    </div>
  );
}

function EndNode({ data }) {
  return (
    <div className="custom-node end-node">
      <div className="node-header">结束</div>
    </div>
  );
}

function LPINode({ data }) {
  return (
    <div className="custom-node lpi-node">
      <div className="node-header">执行LPI: {data.label}</div>
      <div className="node-content">
        {data.description}
      </div>
    </div>
  );
}

function AgentNode({ data }) {
  return (
    <div className="custom-node agent-node">
      <div className="node-header">执行Agent: {data.label}</div>
      <div className="node-content">
        {data.description}
      </div>
    </div>
  );
}

function CommonNode({ data }) {
  return (
    <div className="custom-node common-node">
      <div className="node-header">通用组件: {data.label}</div>
      <div className="node-content">
        {data.description}
      </div>
    </div>
  );
}

const AgentDesigner = ({ component }) => {
  const [form] = Form.useForm();
  const [nodes, setNodes] = useState([
    {
      id: '1',
      type: 'startNode',
      data: { label: '开始' },
      position: { x: 250, y: 5 },
    },
    {
      id: '2',
      type: 'endNode',
      data: { label: '结束' },
      position: { x: 250, y: 400 },
    },
  ]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  const onNodeClick = (event, node) => {
    setSelectedNode(node);
  };

  const addNode = (type) => {
    const newNode = {
      id: String(Date.now()),
      type: `${type}Node`,
      data: { 
        label: `新${type === 'lpi' ? 'LPI' : type === 'agent' ? 'Agent' : '通用'}节点`,
        description: '请编辑节点内容'
      },
      position: { 
        x: 250, 
        y: nodes.length * 100 + 50 
      },
    };
    
    setNodes((nds) => [...nds, newNode]);
  };

  return (
    <div className="agent-designer">
      <Tabs defaultActiveKey="profile">
        <TabPane tab="Agent配置" key="profile">
          <Card title="Agent基本信息">
            <Form
              form={form}
              layout="vertical"
              initialValues={{
                name: component?.title || '',
                description: '',
                type: 'assistant',
              }}
            >
              <Form.Item name="name" label="Agent名称" rules={[{ required: true }]}>
                <Input placeholder="请输入Agent名称" />
              </Form.Item>
              
              <Form.Item name="description" label="描述" rules={[{ required: true }]}>
                <TextArea rows={4} placeholder="请输入Agent描述" />
              </Form.Item>
              
              <Form.Item name="englishDescription" label="英文描述">
                <TextArea rows={4} placeholder="请输入Agent英文描述" />
              </Form.Item>
              
              <Form.Item name="type" label="Agent类型" rules={[{ required: true }]}>
                <Select>
                  <Option value="assistant">助手型</Option>
                  <Option value="task">任务型</Option>
                  <Option value="workflow">工作流型</Option>
                </Select>
              </Form.Item>
              
              <h3>入口参数配置</h3>
              <Form.List name="params">
                {(fields, { add, remove }) => (
                  <>
                    {fields.map(field => (
                      <Card 
                        key={field.key} 
                        size="small" 
                        style={{ marginBottom: 16 }}
                        extra={
                          <Button 
                            type="text" 
                            danger 
                            onClick={() => remove(field.name)}
                          >
                            删除
                          </Button>
                        }
                      >
                        <Form.Item
                          {...field}
                          name={[field.name, 'name']}
                          label="参数名称"
                          rules={[{ required: true, message: '请输入参数名称' }]}
                        >
                          <Input placeholder="参数名称" />
                        </Form.Item>
                        
                        <Form.Item
                          {...field}
                          name={[field.name, 'description']}
                          label="参数描述"
                        >
                          <Input placeholder="参数描述" />
                        </Form.Item>
                        
                        <Form.Item
                          {...field}
                          name={[field.name, 'type']}
                          label="参数类型"
                        >
                          <Select placeholder="参数类型">
                            <Option value="string">字符串</Option>
                            <Option value="number">数字</Option>
                            <Option value="boolean">布尔值</Option>
                            <Option value="object">对象</Option>
                            <Option value="array">数组</Option>
                          </Select>
                        </Form.Item>
                        
                        <Form.Item
                          {...field}
                          name={[field.name, 'defaultValue']}
                          label="默认值"
                        >
                          <Input placeholder="默认值" />
                        </Form.Item>
                        
                        <Form.Item
                          {...field}
                          name={[field.name, 'example']}
                          label="示例值"
                        >
                          <Input placeholder="示例值" />
                        </Form.Item>
                      </Card>
                    ))}
                    <Form.Item>
                      <Button 
                        type="dashed" 
                        onClick={() => add()} 
                        icon={<PlusOutlined />}
                        block
                      >
                        添加入口参数
                      </Button>
                    </Form.Item>
                  </>
                )}
              </Form.List>
            </Form>
          </Card>
        </TabPane>
        
        <TabPane tab="工作流设计" key="workflow">
          <div className="workflow-designer">
            <div className="toolbar">
              <div className="node-buttons">
                <Button onClick={() => addNode('lpi')}>添加LPI节点</Button>
                <Button onClick={() => addNode('agent')}>添加Agent节点</Button>
                <Button onClick={() => addNode('common')}>添加通用节点</Button>
              </div>
              
              <div className="node-editor">
                {selectedNode && (
                  <Card title={`编辑节点: ${selectedNode.data.label}`} size="small">
                    <Form layout="vertical">
                      <Form.Item label="节点名称">
                        <Input 
                          value={selectedNode.data.label} 
                          onChange={(e) => {
                            const updatedNodes = nodes.map(node => {
                              if (node.id === selectedNode.id) {
                                return {
                                  ...node,
                                  data: {
                                    ...node.data,
                                    label: e.target.value
                                  }
                                };
                              }
                              return node;
                            });
                            setNodes(updatedNodes);
                          }}
                        />
                      </Form.Item>
                      
                      <Form.Item label="节点内容">
                        <TextArea 
                          rows={4}
                          value={selectedNode.data.description}
                          onChange={(e) => {
                            const updatedNodes = nodes.map(node => {
                              if (node.id === selectedNode.id) {
                                return {
                                  ...node,
                                  data: {
                                    ...node.data,
                                    description: e.target.value
                                  }
                                };
                              }
                              return node;
                            });
                            setNodes(updatedNodes);
                          }}
                        />
                      </Form.Item>
                    </Form>
                  </Card>
                )}
              </div>
            </div>
            
            <div className="workflow-canvas">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                onConnect={onConnect}
                onNodeClick={onNodeClick}
                nodeTypes={nodeTypes}
                fitView
              >
                <Controls />
                <MiniMap />
                <Background variant="dots" gap={12} size={1} />
              </ReactFlow>
            </div>
          </div>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default AgentDesigner; 