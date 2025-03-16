import React, { useState } from 'react';
import { Form, Input, Select, Button, Card, Table, Tabs, message, Popconfirm } from 'antd';
import { SaveOutlined, PlusOutlined, DeleteOutlined } from '@ant-design/icons';
import { updateLPI } from '../../services/componentService';

const { TabPane } = Tabs;
const { Option } = Select;
const { TextArea } = Input;

const LPIDetail = ({ detail, onRefresh, onRefreshTree }) => {
  const [form] = Form.useForm();
  const [inputParams, setInputParams] = useState(detail?.input_params || []);
  const [outputParams, setOutputParams] = useState(detail?.output_params || []);
  const [examples, setExamples] = useState(detail?.examples || []);
  const [loading, setLoading] = useState(false);

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
      
      await updateLPI(detail.id, updateData);
      message.success('LPI组件保存成功');
      onRefresh();
      onRefreshTree();
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAddInputParam = () => {
    setInputParams([...inputParams, { name: '', type: 'string', description: '', required: true }]);
  };

  const handleInputParamChange = (index, field, value) => {
    const newParams = [...inputParams];
    newParams[index][field] = value;
    setInputParams(newParams);
  };

  const handleRemoveInputParam = (index) => {
    const newParams = [...inputParams];
    newParams.splice(index, 1);
    setInputParams(newParams);
  };

  const handleAddOutputParam = () => {
    setOutputParams([...outputParams, { name: '', type: 'string', description: '' }]);
  };

  const handleOutputParamChange = (index, field, value) => {
    const newParams = [...outputParams];
    newParams[index][field] = value;
    setOutputParams(newParams);
  };

  const handleRemoveOutputParam = (index) => {
    const newParams = [...outputParams];
    newParams.splice(index, 1);
    setOutputParams(newParams);
  };

  const handleAddExample = () => {
    setExamples([...examples, { input: {}, output: {} }]);
  };

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

  const handleRemoveExample = (index) => {
    const newExamples = [...examples];
    newExamples.splice(index, 1);
    setExamples(newExamples);
  };

  return (
    <div>
      <div className="detail-header">
        <h2 className="detail-title">LPI组件详情</h2>
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
          api_type: detail?.api_type || 'rest',
          endpoint: detail?.endpoint || '',
          method: detail?.method || 'POST'
        }}
      >
        <Tabs defaultActiveKey="basic">
          <TabPane tab="基本信息" key="basic">
            <Form.Item
              name="name"
              label="组件名称"
              rules={[{ required: true, message: '请输入组件名称' }]}
            >
              <Input placeholder="请输入组件名称" />
            </Form.Item>

            <Form.Item
              name="description"
              label="中文描述"
              rules={[{ required: true, message: '请输入中文描述' }]}
            >
              <TextArea placeholder="请输入中文描述" rows={2} />
            </Form.Item>

            <Form.Item
              name="english_description"
              label="英文描述"
            >
              <TextArea placeholder="请输入英文描述" rows={2} />
            </Form.Item>

            <Form.Item
              name="category"
              label="分类"
            >
              <Input placeholder="请输入分类" />
            </Form.Item>
          </TabPane>

          <TabPane tab="API配置" key="api">
            <Form.Item
              name="api_type"
              label="API类型"
              rules={[{ required: true, message: '请选择API类型' }]}
            >
              <Select placeholder="请选择API类型">
                <Option value="rest">REST API</Option>
                <Option value="python">Python API</Option>
              </Select>
            </Form.Item>

            <Form.Item
              name="endpoint"
              label="API端点"
              rules={[{ required: true, message: '请输入API端点' }]}
            >
              <Input placeholder="请输入API端点，如http://example.com/api或Python模块路径" />
            </Form.Item>

            <Form.Item
              name="method"
              label="方法"
              rules={[{ required: true, message: '请输入方法' }]}
            >
              <Input placeholder="请输入方法，如GET、POST或Python函数名" />
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
                <Form.Item label="参数名称">
                  <Input 
                    value={param.name} 
                    onChange={(e) => handleInputParamChange(index, 'name', e.target.value)} 
                    placeholder="请输入参数名称"
                  />
                </Form.Item>
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
                <Form.Item label="参数描述">
                  <TextArea 
                    value={param.description} 
                    onChange={(e) => handleInputParamChange(index, 'description', e.target.value)} 
                    placeholder="请输入参数描述"
                    rows={2}
                  />
                </Form.Item>
                <Form.Item label="是否必填">
                  <Select 
                    value={param.required} 
                    onChange={(value) => handleInputParamChange(index, 'required', value)}
                  >
                    <Option value={true}>是</Option>
                    <Option value={false}>否</Option>
                  </Select>
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
                <Form.Item label="参数名称">
                  <Input 
                    value={param.name} 
                    onChange={(e) => handleOutputParamChange(index, 'name', e.target.value)} 
                    placeholder="请输入参数名称"
                  />
                </Form.Item>
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
                <Form.Item label="输入示例">
                  <TextArea 
                    value={typeof example.input === 'object' ? JSON.stringify(example.input, null, 2) : example.input} 
                    onChange={(e) => handleExampleChange(index, 'input', e.target.value)} 
                    placeholder="请输入JSON格式的输入示例"
                    rows={4}
                  />
                </Form.Item>
                <Form.Item label="输出示例">
                  <TextArea 
                    value={typeof example.output === 'object' ? JSON.stringify(example.output, null, 2) : example.output} 
                    onChange={(e) => handleExampleChange(index, 'output', e.target.value)} 
                    placeholder="请输入JSON格式的输出示例"
                    rows={4}
                  />
                </Form.Item>
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
        </Tabs>
      </Form>
    </div>
  );
};

export default LPIDetail; 