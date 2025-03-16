import React, { useState } from 'react';
import { Form, Input, Select, Button, Card, Tabs, message, Popconfirm } from 'antd';
import { SaveOutlined, PlusOutlined, DeleteOutlined } from '@ant-design/icons';
import { updateCommonComponent } from '../../services/componentService';

const { TabPane } = Tabs;
const { Option } = Select;
const { TextArea } = Input;

const CommonComponentDetail = ({ detail, onRefresh, onRefreshTree }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [componentSubtype, setComponentSubtype] = useState(detail?.component_subtype || 'condition');
  const [config, setConfig] = useState(detail?.config || {});

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      
      const updateData = {
        ...values,
        component_subtype: componentSubtype,
        config: config
      };
      
      await updateCommonComponent(detail.id, updateData);
      message.success('通用组件保存成功');
      onRefresh();
      onRefreshTree();
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSubtypeChange = (value) => {
    setComponentSubtype(value);
    // 根据子类型初始化配置
    if (value === 'condition') {
      setConfig({
        condition_type: 'simple',
        field: '',
        operator: 'eq',
        value: ''
      });
    } else if (value === 'executor') {
      setConfig({
        executor_type: 'transform',
        transform_type: 'map',
        mapping: {}
      });
    }
  };

  const handleConfigChange = (field, value) => {
    setConfig({
      ...config,
      [field]: value
    });
  };

  const renderConditionConfig = () => {
    const conditionType = config.condition_type || 'simple';
    
    return (
      <>
        <Form.Item label="条件类型">
          <Select 
            value={conditionType} 
            onChange={(value) => handleConfigChange('condition_type', value)}
          >
            <Option value="simple">简单条件</Option>
            <Option value="complex">复杂条件</Option>
          </Select>
        </Form.Item>
        
        {conditionType === 'simple' ? (
          <>
            <Form.Item label="字段名">
              <Input 
                value={config.field} 
                onChange={(e) => handleConfigChange('field', e.target.value)} 
                placeholder="请输入字段名"
              />
            </Form.Item>
            <Form.Item label="操作符">
              <Select 
                value={config.operator} 
                onChange={(value) => handleConfigChange('operator', value)}
              >
                <Option value="eq">等于</Option>
                <Option value="ne">不等于</Option>
                <Option value="gt">大于</Option>
                <Option value="lt">小于</Option>
                <Option value="contains">包含</Option>
              </Select>
            </Form.Item>
            <Form.Item label="比较值">
              <Input 
                value={config.value} 
                onChange={(e) => handleConfigChange('value', e.target.value)} 
                placeholder="请输入比较值"
              />
            </Form.Item>
          </>
        ) : (
          <Form.Item label="表达式">
            <TextArea 
              value={config.expression} 
              onChange={(e) => handleConfigChange('expression', e.target.value)} 
              placeholder="请输入条件表达式，例如：input.status === 'error'"
              rows={4}
            />
          </Form.Item>
        )}
      </>
    );
  };

  const renderExecutorConfig = () => {
    const executorType = config.executor_type || 'transform';
    
    return (
      <>
        <Form.Item label="执行器类型">
          <Select 
            value={executorType} 
            onChange={(value) => handleConfigChange('executor_type', value)}
          >
            <Option value="transform">数据转换</Option>
            <Option value="external">外部调用</Option>
          </Select>
        </Form.Item>
        
        {executorType === 'transform' ? (
          <>
            <Form.Item label="转换类型">
              <Select 
                value={config.transform_type} 
                onChange={(value) => handleConfigChange('transform_type', value)}
              >
                <Option value="map">映射</Option>
                <Option value="filter">过滤</Option>
              </Select>
            </Form.Item>
            
            {config.transform_type === 'map' ? (
              <Form.Item label="映射配置">
                <TextArea 
                  value={JSON.stringify(config.mapping || {}, null, 2)} 
                  onChange={(e) => {
                    try {
                      const mapping = JSON.parse(e.target.value);
                      handleConfigChange('mapping', mapping);
                    } catch (error) {
                      // 解析失败，不更新
                    }
                  }} 
                  placeholder="请输入JSON格式的映射配置，例如：{'target_field': 'source.field'}"
                  rows={4}
                />
              </Form.Item>
            ) : (
              <Form.Item label="字段列表">
                <TextArea 
                  value={Array.isArray(config.fields) ? config.fields.join('\n') : ''} 
                  onChange={(e) => {
                    const fields = e.target.value.split('\n').filter(f => f.trim());
                    handleConfigChange('fields', fields);
                  }} 
                  placeholder="请输入要保留的字段，每行一个"
                  rows={4}
                />
              </Form.Item>
            )}
          </>
        ) : (
          <>
            <Form.Item label="URL">
              <Input 
                value={config.url} 
                onChange={(e) => handleConfigChange('url', e.target.value)} 
                placeholder="请输入外部调用URL"
              />
            </Form.Item>
            <Form.Item label="方法">
              <Select 
                value={config.method} 
                onChange={(value) => handleConfigChange('method', value)}
              >
                <Option value="GET">GET</Option>
                <Option value="POST">POST</Option>
              </Select>
            </Form.Item>
          </>
        )}
      </>
    );
  };

  return (
    <div>
      <div className="detail-header">
        <h2 className="detail-title">通用组件详情</h2>
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
          category: detail?.category || ''
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

          <TabPane tab="组件配置" key="config">
            <Form.Item
              label="组件子类型"
              rules={[{ required: true, message: '请选择组件子类型' }]}
            >
              <Select 
                value={componentSubtype} 
                onChange={handleSubtypeChange}
                placeholder="请选择组件子类型"
              >
                <Option value="condition">条件组件</Option>
                <Option value="executor">执行器组件</Option>
              </Select>
            </Form.Item>

            <Card title="组件配置" bordered={false}>
              {componentSubtype === 'condition' ? renderConditionConfig() : renderExecutorConfig()}
            </Card>
          </TabPane>
        </Tabs>
      </Form>
    </div>
  );
};

export default CommonComponentDetail; 