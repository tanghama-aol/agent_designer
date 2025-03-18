import React, { useState, useCallback, useRef, useEffect } from 'react';
import { Form, Input, Button, Card, Tabs, message, Popconfirm, Select, AutoComplete, Row, Col } from 'antd';
import { SaveOutlined, PlusOutlined, DeleteOutlined, PlayCircleOutlined, EditOutlined, AppstoreOutlined } from '@ant-design/icons';
import ReactFlow, { 
  Background, 
  Controls, 
  MiniMap, 
  addEdge, 
  applyEdgeChanges, 
  applyNodeChanges,
  Panel,
  Handle,
  Position
} from 'reactflow';
import 'reactflow/dist/style.css';
import './WorkflowEditor.css';
import { updateAgent, createWorkflow, updateWorkflow, getComponentTree } from '../../services/componentService';
import { 
  RocketOutlined, 
  ApiOutlined, 
  BlockOutlined, 
  RightCircleOutlined, 
  CheckCircleOutlined,
  FolderOutlined
} from '@ant-design/icons';

const { TabPane } = Tabs;
const { Option } = Select;
const { TextArea } = Input;

// 节点类型
const nodeTypes = {
  start: StartNode,
  end: EndNode,
  lpi: LPINode,
  agent: AgentNode,
  common: CommonNode,
  phase: PhaseNode
};

// 开始节点
function StartNode({ data }) {
  return (
    <div className="workflow-node start-node">
      <Handle type="source" position={Position.Bottom} />
      <div className="node-content">
        <RightCircleOutlined className="node-icon" />
        <span>{data?.name || '开始节点'}</span>
      </div>
    </div>
  );
}

// 结束节点
function EndNode({ data }) {
  return (
    <div className="workflow-node end-node">
      <Handle type="target" position={Position.Top} />
      <div className="node-content">
        <CheckCircleOutlined className="node-icon" />
        <span>{data?.name || '结束节点'}</span>
      </div>
    </div>
  );
}

// 阶段节点
function PhaseNode({ data }) {
  return (
    <div className="workflow-node phase-node">
      <Handle type="target" position={Position.Top} />
      <div className="node-content">
        <FolderOutlined className="node-icon" />
        <span>{data?.name || '阶段节点'}</span>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

// LPI节点
function LPINode({ data }) {
  return (
    <div className="workflow-node lpi-node">
      <Handle type="target" position={Position.Top} />
      <div className="node-content">
        <ApiOutlined className="node-icon" />
        <span>{data?.name || 'LPI节点'}</span>
      </div>
      {data?.lpiCategory && (
        <div className="node-category">{data.lpiCategory}</div>
      )}
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

// Agent节点
function AgentNode({ data }) {
  return (
    <div className="workflow-node agent-node">
      <Handle type="target" position={Position.Top} />
      <div className="node-content">
        <RocketOutlined className="node-icon" />
        <span>{data?.name || 'Agent节点'}</span>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

// 通用组件节点
function CommonNode({ data }) {
  return (
    <div className="workflow-node common-node">
      <Handle type="target" position={Position.Top} />
      <div className="node-content">
        <BlockOutlined className="node-icon" />
        <span>{data?.name || '通用组件节点'}</span>
      </div>
      <Handle type="source" position={Position.Bottom} />
    </div>
  );
}

const AgentDetail = ({ detail, onRefresh, onRefreshTree }) => {
  const [form] = Form.useForm();
  const [inputParams, setInputParams] = useState(detail?.input_params || []);
  const [outputParams, setOutputParams] = useState(detail?.output_params || []);
  const [examples, setExamples] = useState(detail?.examples || []);
  const [loading, setLoading] = useState(false);
  const [activeWorkflowId, setActiveWorkflowId] = useState(detail?.workflows?.[0]?.id);
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);
  const [selectedNode, setSelectedNode] = useState(null);
  const [componentOptions, setComponentOptions] = useState([]);
  const [searchText, setSearchText] = useState('');
  const [workflowMode, setWorkflowMode] = useState('flow'); // 'flow' or 'markdown'
  const [markdownContent, setMarkdownContent] = useState(detail?.workflow_markdown || '');
  const reactFlowWrapper = useRef(null);
  const [reactFlowInstance, setReactFlowInstance] = useState(null);

  // 初始化工作流数据
  useEffect(() => {
    if (detail?.workflows && detail.workflows.length > 0) {
      const workflow = detail.workflows[0];
      if (workflow.nodes && workflow.edges) {
        setNodes(workflow.nodes);
        setEdges(workflow.edges);
        setActiveWorkflowId(workflow.id);
      }
    }
  }, [detail]);

  // 获取组件树数据用于自动完成
  useEffect(() => {
    const fetchComponentOptions = async () => {
      try {
        const treeData = await getComponentTree();
        const options = [];
        
        const extractOptions = (nodes) => {
          if (!nodes) return;
          nodes.forEach(node => {
            if (node.id) {
              options.push({
                value: node.id.toString(),
                label: node.title,
                type: node.type,
                category: node.category
              });
            }
            if (node.children) {
              extractOptions(node.children);
            }
          });
        };
        
        extractOptions(treeData);
        setComponentOptions(options);
      } catch (error) {
        console.error('获取组件选项失败:', error);
      }
    };
    
    fetchComponentOptions();
  }, []);

  // 工作流节点变化
  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  // 工作流边变化
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  // 连接工作流节点
  const onConnect = useCallback(
    (params) => {
      // 确保有源节点和目标节点
      if (!params.source || !params.target) {
        console.error("连接缺少源节点或目标节点", params);
        return;
      }
      
      // 如果没有手柄ID，使用默认值
      const connection = {
        ...params,
        sourceHandle: params.sourceHandle || 'source',
        targetHandle: params.targetHandle || 'target',
        id: `edge_${Date.now()}`
      };
      
      console.log("创建连接:", connection);
      setEdges((eds) => addEdge(connection, eds));
    },
    []
  );

  // 选择节点
  const onNodeClick = (event, node) => {
    setSelectedNode(node);
  };

  // 保存Agent
  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      
      const updateData = {
        ...values,
        input_params: inputParams,
        output_params: outputParams,
        examples: examples
      };
      
      await updateAgent(detail.id, updateData);
      message.success('Agent组件保存成功');
      onRefresh();
      onRefreshTree();
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  // 保存工作流
  const handleSaveWorkflow = async () => {
    try {
      setLoading(true);
      
      const workflow = detail.workflows.find(w => w.id === activeWorkflowId);
      
      if (workflow) {
        await updateWorkflow(workflow.id, {
          nodes,
          edges
        });
        message.success('工作流保存成功');
      } else {
        const newWorkflow = await createWorkflow({
          name: `${detail.name}工作流`,
          description: `${detail.name}的工作流`,
          agent_id: detail.id,
          nodes,
          edges
        });
        setActiveWorkflowId(newWorkflow.id);
        message.success('工作流创建成功');
      }
      
      onRefresh();
    } catch (error) {
      console.error('保存工作流失败:', error);
      message.error('保存工作流失败');
    } finally {
      setLoading(false);
    }
  };

  // 添加节点
  const addNode = (type) => {
    let nodeName = '';
    switch(type) {
      case 'start': nodeName = '开始节点'; break;
      case 'end': nodeName = '结束节点'; break;
      case 'phase': nodeName = '新阶段'; break;
      case 'lpi': nodeName = '新LPI'; break;
      case 'agent': nodeName = '新Agent'; break;
      case 'common': nodeName = '新组件'; break;
      default: nodeName = '新节点';
    }
    
    const newNode = {
      id: `node_${Date.now()}`,
      type,
      position: { x: 250, y: 250 },
      data: { 
        name: nodeName,
        id: `node_${Date.now()}`
      }
    };
    
    setNodes((nds) => {
      const newNodes = nds.concat(newNode);
      const lastNode = nds[nds.length - 1];
      
      if (lastNode) {
        const newEdge = {
          id: `edge_${Date.now()}`,
          source: lastNode.id,
          target: newNode.id,
          sourceHandle: 'source',
          targetHandle: 'target'
        };
        setEdges((eds) => eds.concat(newEdge));
      }
      
      return newNodes;
    });
  };

  // 删除节点
  const deleteNode = () => {
    if (!selectedNode) return;
    
    setNodes(nodes.filter(node => node.id !== selectedNode.id));
    setEdges(edges.filter(edge => edge.source !== selectedNode.id && edge.target !== selectedNode.id));
    setSelectedNode(null);
  };

  // 处理组件拖拽到工作流
  const onDragOver = useCallback((event) => {
    event.preventDefault();
    event.dataTransfer.dropEffect = 'move';
  }, []);

  const onDrop = useCallback(
    (event) => {
      event.preventDefault();

      if (!reactFlowInstance || !reactFlowWrapper.current) {
        return;
      }

      const reactFlowBounds = reactFlowWrapper.current.getBoundingClientRect();
      let componentData;
      
      try {
        componentData = JSON.parse(event.dataTransfer.getData('application/reactflow'));
      } catch (err) {
        return;
      }

      // 检查是否有组件数据
      if (!componentData) {
        return;
      }

      const position = reactFlowInstance.project({
        x: event.clientX - reactFlowBounds.left,
        y: event.clientY - reactFlowBounds.top,
      });

      const nodeId = `node_${Date.now()}`;
      const newNode = {
        id: nodeId,
        type: componentData.type,
        position,
        data: { 
          name: componentData.title,
          component_id: componentData.id,
          lpiCategory: componentData.category,
          id: nodeId
        },
      };

      // 找到最近的节点并自动连接
      setNodes((nds) => {
        const newNodes = [...nds, newNode];
        
        // 尝试找到最接近的节点进行连接
        if (nds.length > 0) {
          // 简单地选择最后一个节点进行连接
          const lastNode = nds[nds.length - 1];
          const newEdge = {
            id: `edge_${Date.now()}`,
            source: lastNode.id,
            target: newNode.id,
            sourceHandle: 'source',
            targetHandle: 'target'
          };
          setEdges((eds) => [...eds, newEdge]);
        }
        
        return newNodes;
      });
    },
    [reactFlowInstance]
  );

  // 处理从组件树拖拽组件
  const handleDragComponent = (component) => {
    if (!component) return;
    
    // 创建拖拽数据
    const dragData = {
      id: component.id,
      type: component.type,
      title: component.title,
      category: component.category
    };
    
    // 设置拖拽数据
    const event = new DragEvent('dragstart');
    Object.defineProperty(event, 'dataTransfer', {
      value: {
        setData: (format, data) => {
          document.body.setAttribute('data-drag-component', data);
        },
        getData: (format) => {
          return document.body.getAttribute('data-drag-component');
        },
        effectAllowed: 'move'
      }
    });
    
    event.dataTransfer.setData('application/reactflow', JSON.stringify(dragData));
  };

  // 处理节点搜索和选择
  const handleSearch = (value) => {
    setSearchText(value);
  };

  const handleSelect = (value, option) => {
    if (!option) return;
    
    // 根据选择的组件创建新节点
    const newNode = {
      id: `node_${Date.now()}`,
      type: option.type,
      position: { x: 250, y: 250 },
      data: { 
        name: option.label,
        component_id: parseInt(option.value),
        lpiCategory: option.category,
        id: `node_${Date.now()}`
      }
    };
    
    setNodes((nds) => {
      const newNodes = [...nds, newNode];
      
      // 如果已有节点，自动连接到上一个节点
      if (nds.length > 0) {
        const lastNode = nds[nds.length - 1];
        const newEdge = {
          id: `edge_${Date.now()}`,
          source: lastNode.id,
          target: newNode.id,
          sourceHandle: 'source',
          targetHandle: 'target'
        };
        setEdges((eds) => [...eds, newEdge]);
      }
      
      return newNodes;
    });
    
    setSearchText('');
  };

  // 切换工作流编辑模式
  const handleModeChange = (mode) => {
    setWorkflowMode(mode);
  };

  // 保存Markdown内容
  const handleMarkdownSave = async () => {
    try {
      setLoading(true);
      await updateAgent(detail.id, {
        ...detail,
        workflow_markdown: markdownContent
      });
      message.success('Markdown保存成功');
      onRefresh();
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  // 添加输入参数
  const handleAddInputParam = () => {
    setInputParams([...inputParams, { name: '', type: 'string', description: '', required: true }]);
  };

  // 修改输入参数
  const handleInputParamChange = (index, field, value) => {
    const newParams = [...inputParams];
    newParams[index][field] = value;
    setInputParams(newParams);
  };

  // 删除输入参数
  const handleRemoveInputParam = (index) => {
    const newParams = [...inputParams];
    newParams.splice(index, 1);
    setInputParams(newParams);
  };

  // 添加输出参数
  const handleAddOutputParam = () => {
    setOutputParams([...outputParams, { name: '', type: 'string', description: '' }]);
  };

  // 修改输出参数
  const handleOutputParamChange = (index, field, value) => {
    const newParams = [...outputParams];
    newParams[index][field] = value;
    setOutputParams(newParams);
  };

  // 删除输出参数
  const handleRemoveOutputParam = (index) => {
    const newParams = [...outputParams];
    newParams.splice(index, 1);
    setOutputParams(newParams);
  };

  // 添加示例
  const handleAddExample = () => {
    setExamples([...examples, { input: {}, output: {} }]);
  };

  // 修改示例
  const handleExampleChange = (index, field, value) => {
    const newExamples = [...examples];
    try {
      newExamples[index][field] = JSON.parse(value);
    } catch (e) {
      // 如果不是有效的JSON，则保存为字符串
      newExamples[index][field] = value;
    }
    setExamples(newExamples);
  };

  // 删除示例
  const handleRemoveExample = (index) => {
    const newExamples = [...examples];
    newExamples.splice(index, 1);
    setExamples(newExamples);
  };

  return (
    <div>
      <div className="detail-header">
        <h2 className="detail-title">Agent组件详情</h2>
        <div className="detail-actions">
          <Button 
            type="primary" 
            icon={<SaveOutlined />} 
            onClick={handleSave}
            loading={loading}
          >
            保存
          </Button>
        </div>
      </div>

      <Form
        form={form}
        layout="vertical"
        initialValues={{
          name: detail?.name || '',
          description: detail?.description || '',
          english_description: detail?.english_description || '',
          category: detail?.category || '',
          agent_type: detail?.agent_type || 'expert'
        }}
      >
        <Tabs defaultActiveKey="basic">
          <TabPane tab="基本信息" key="basic">
            <Row gutter={16}>
              <Col span={12}>
                <Form.Item
                  name="name"
                  label="组件名称"
                  rules={[{ required: true, message: '请输入组件名称' }]}
                >
                  <Input placeholder="请输入组件名称" />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  name="agent_type"
                  label="Agent类型"
                  rules={[{ required: true, message: '请选择Agent类型' }]}
                >
                  <Select>
                    <Option value="expert">专家Agent</Option>
                    <Option value="scenario">场景Agent</Option>
                  </Select>
                </Form.Item>
              </Col>
            </Row>

            <Row gutter={16}>
              <Col span={12}>
                <Form.Item
                  name="description"
                  label="中文描述"
                  rules={[{ required: true, message: '请输入中文描述' }]}
                >
                  <TextArea placeholder="请输入中文描述" rows={2} />
                </Form.Item>
              </Col>
              <Col span={12}>
                <Form.Item
                  name="english_description"
                  label="英文描述"
                >
                  <TextArea placeholder="请输入英文描述" rows={2} />
                </Form.Item>
              </Col>
            </Row>

            <Form.Item
              name="category"
              label="分类"
            >
              <Input placeholder="请输入分类" />
            </Form.Item>
          </TabPane>

          <TabPane tab="输入参数" key="input">
            {inputParams.map((param, index) => (
              <Card 
                key={index} 
                size="small" 
                style={{ marginBottom: 16 }}
                title={`参数 ${index + 1}`}
                extra={
                  <Popconfirm
                    title="确定要删除此参数吗？"
                    onConfirm={() => handleRemoveInputParam(index)}
                    okText="是"
                    cancelText="否"
                  >
                    <Button danger icon={<DeleteOutlined />} size="small" />
                  </Popconfirm>
                }
              >
                <Row gutter={16}>
                  <Col span={8}>
                    <Form.Item label="参数名称">
                      <Input 
                        value={param.name} 
                        onChange={(e) => handleInputParamChange(index, 'name', e.target.value)} 
                        placeholder="请输入参数名称"
                      />
                    </Form.Item>
                  </Col>
                  <Col span={8}>
                    <Form.Item label="参数类型">
                      <Select 
                        value={param.type} 
                        onChange={(value) => handleInputParamChange(index, 'type', value)}
                      >
                        <Option value="string">字符串</Option>
                        <Option value="number">数字</Option>
                        <Option value="boolean">布尔值</Option>
                        <Option value="object">对象</Option>
                        <Option value="array">数组</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                  <Col span={8}>
                    <Form.Item label="是否必填">
                      <Select 
                        value={param.required} 
                        onChange={(value) => handleInputParamChange(index, 'required', value)}
                      >
                        <Option value={true}>是</Option>
                        <Option value={false}>否</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                </Row>
                <Form.Item label="参数描述">
                  <TextArea 
                    value={param.description} 
                    onChange={(e) => handleInputParamChange(index, 'description', e.target.value)} 
                    placeholder="请输入参数描述"
                    rows={2}
                  />
                </Form.Item>
              </Card>
            ))}
            <Button 
              type="dashed" 
              onClick={handleAddInputParam} 
              block 
              icon={<PlusOutlined />}
            >
              添加输入参数
            </Button>
          </TabPane>

          <TabPane tab="输出参数" key="output">
            {outputParams.map((param, index) => (
              <Card 
                key={index} 
                size="small" 
                style={{ marginBottom: 16 }}
                title={`参数 ${index + 1}`}
                extra={
                  <Popconfirm
                    title="确定要删除此参数吗？"
                    onConfirm={() => handleRemoveOutputParam(index)}
                    okText="是"
                    cancelText="否"
                  >
                    <Button danger icon={<DeleteOutlined />} size="small" />
                  </Popconfirm>
                }
              >
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item label="参数名称">
                      <Input 
                        value={param.name} 
                        onChange={(e) => handleOutputParamChange(index, 'name', e.target.value)} 
                        placeholder="请输入参数名称"
                      />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item label="参数类型">
                      <Select 
                        value={param.type} 
                        onChange={(value) => handleOutputParamChange(index, 'type', value)}
                      >
                        <Option value="string">字符串</Option>
                        <Option value="number">数字</Option>
                        <Option value="boolean">布尔值</Option>
                        <Option value="object">对象</Option>
                        <Option value="array">数组</Option>
                      </Select>
                    </Form.Item>
                  </Col>
                </Row>
                <Form.Item label="参数描述">
                  <TextArea 
                    value={param.description} 
                    onChange={(e) => handleOutputParamChange(index, 'description', e.target.value)} 
                    placeholder="请输入参数描述"
                    rows={2}
                  />
                </Form.Item>
              </Card>
            ))}
            <Button 
              type="dashed" 
              onClick={handleAddOutputParam} 
              block 
              icon={<PlusOutlined />}
            >
              添加输出参数
            </Button>
          </TabPane>

          <TabPane tab="示例" key="examples">
            {examples.map((example, index) => (
              <Card 
                key={index} 
                size="small" 
                style={{ marginBottom: 16 }}
                title={`示例 ${index + 1}`}
                extra={
                  <Popconfirm
                    title="确定要删除此示例吗？"
                    onConfirm={() => handleRemoveExample(index)}
                    okText="是"
                    cancelText="否"
                  >
                    <Button danger icon={<DeleteOutlined />} size="small" />
                  </Popconfirm>
                }
              >
                <Row gutter={16}>
                  <Col span={12}>
                    <Form.Item label="输入示例">
                      <TextArea 
                        value={typeof example.input === 'object' ? JSON.stringify(example.input, null, 2) : example.input} 
                        onChange={(e) => handleExampleChange(index, 'input', e.target.value)} 
                        placeholder="请输入JSON格式的输入示例"
                        rows={4}
                      />
                    </Form.Item>
                  </Col>
                  <Col span={12}>
                    <Form.Item label="输出示例">
                      <TextArea 
                        value={typeof example.output === 'object' ? JSON.stringify(example.output, null, 2) : example.output} 
                        onChange={(e) => handleExampleChange(index, 'output', e.target.value)} 
                        placeholder="请输入JSON格式的输出示例"
                        rows={4}
                      />
                    </Form.Item>
                  </Col>
                </Row>
              </Card>
            ))}
            <Button 
              type="dashed" 
              onClick={handleAddExample} 
              block 
              icon={<PlusOutlined />}
            >
              添加示例
            </Button>
          </TabPane>

          <TabPane tab="工作流" key="workflow">
            <div className="workflow-actions">
              <Button.Group>
                <Button 
                  type={workflowMode === 'flow' ? 'primary' : 'default'}
                  onClick={() => handleModeChange('flow')}
                >
                  可视化编辑
                </Button>
                <Button 
                  type={workflowMode === 'markdown' ? 'primary' : 'default'}
                  onClick={() => handleModeChange('markdown')}
                >
                  Markdown编辑
                </Button>
              </Button.Group>
              <Button 
                type="primary" 
                icon={<SaveOutlined />} 
                onClick={workflowMode === 'flow' ? handleSaveWorkflow : handleMarkdownSave}
                loading={loading}
              >
                保存工作流
              </Button>
              <Button 
                type="primary" 
                icon={<PlayCircleOutlined />} 
                onClick={() => message.info('测试功能待实现')}
              >
                测试工作流
              </Button>
            </div>

            {workflowMode === 'flow' ? (
              <>
                <div className="workflow-tools">
                  <Button onClick={() => addNode('start')}>添加开始节点</Button>
                  <Button onClick={() => addNode('end')}>添加结束节点</Button>
                  <Button onClick={() => addNode('phase')}>添加阶段节点</Button>
                  <Button onClick={deleteNode} disabled={!selectedNode}>删除选中节点</Button>
                </div>

                <div className="component-search">
                  <AutoComplete
                    style={{ width: '100%', marginBottom: 16 }}
                    options={componentOptions}
                    value={searchText}
                    onChange={handleSearch}
                    onSelect={handleSelect}
                    placeholder="搜索组件添加到工作流"
                    filterOption={(inputValue, option) =>
                      option.label.toLowerCase().indexOf(inputValue.toLowerCase()) !== -1
                    }
                  />
                </div>

                <div className="workflow-editor-container">
                  <div className="workflow-editor" ref={reactFlowWrapper}>
                    <ReactFlow
                      nodes={nodes}
                      edges={edges}
                      onNodesChange={onNodesChange}
                      onEdgesChange={onEdgesChange}
                      onConnect={onConnect}
                      onNodeClick={onNodeClick}
                      nodeTypes={nodeTypes}
                      onInit={setReactFlowInstance}
                      onDrop={onDrop}
                      onDragOver={onDragOver}
                      fitView
                      defaultEdgeOptions={{ 
                        type: 'smoothstep', 
                        animated: false,
                        style: { stroke: '#1890ff', strokeWidth: 2 },
                        markerEnd: {
                          type: 'arrowclosed',
                          color: '#1890ff'
                        }
                      }}
                      connectionLineStyle={{ stroke: '#1890ff', strokeWidth: 2 }}
                      connectionLineType="smoothstep"
                      snapToGrid={true}
                      snapGrid={[15, 15]}
                    >
                      <Controls position="bottom-right" />
                      <MiniMap 
                        nodeStrokeColor={(n) => {
                          if (n.type === 'start') return '#0041d0';
                          if (n.type === 'end') return '#ff0072';
                          if (n.type === 'lpi') return '#ff9a00';
                          if (n.type === 'agent') return '#7b00ff';
                          return '#999';
                        }}
                        nodeColor={(n) => {
                          if (n.type === 'start') return '#e6f7ff';
                          if (n.type === 'end') return '#f6ffed';
                          if (n.type === 'lpi') return '#fff7e6';
                          if (n.type === 'agent') return '#f9f0ff';
                          return '#f5f5f5';
                        }}
                      />
                      <Background variant="dots" gap={12} size={1} />
                      <Panel position="top-right">
                        <div className="selected-node-info">
                          {selectedNode && (
                            <Card size="small" title="节点属性">
                              <p>ID: {selectedNode.id}</p>
                              <p>类型: {selectedNode.type}</p>
                              <p>名称: {selectedNode.data?.name}</p>
                            </Card>
                          )}
                        </div>
                      </Panel>
                    </ReactFlow>
                  </div>
                </div>
              </>
            ) : (
              <div className="workflow-markdown-editor">
                <div className="markdown-editor-header">
                  <span>Markdown编辑器</span>
                  <Button 
                    type="text" 
                    icon={<EditOutlined />}
                    onClick={() => message.info('预览功能待实现')}
                  >
                    预览
                  </Button>
                </div>
                <div className="markdown-editor-content">
                  <TextArea
                    value={markdownContent}
                    onChange={(e) => setMarkdownContent(e.target.value)}
                    placeholder="请输入工作流的Markdown描述"
                    style={{ height: '100%', border: 'none', resize: 'none' }}
                  />
                </div>
              </div>
            )}
          </TabPane>
        </Tabs>
      </Form>
    </div>
  );
};

export default AgentDetail;