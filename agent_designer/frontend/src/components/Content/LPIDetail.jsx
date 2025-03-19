import React, { useState, useEffect } from 'react';
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

  // 当detail变化时更新表单
  useEffect(() => {
    if (detail) {
      form.setFieldsValue({
        name: detail.name,
        description: detail.description,
        english_description: detail.english_description,
        type: detail.type,
        category: detail.category,
        // 其他字段...
      });
      setInputParams(detail.input_params || []);
      setOutputParams(detail.output_params || []);
      setExamples(detail.examples || []);
    }
  }, [detail, form]);

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      
      const updateData = {
        ...detail, // 保留原有数据
        ...values, // 更新表单数据
        input_params: inputParams,
        output_params: outputParams,
        examples: examples,
        type: 'lpi', // 确保类型正确
      };
      
      await updateLPI(detail.id, updateData);
      message.success('LPI组件保存成功');
      if (onRefresh) onRefresh();
      if (onRefreshTree) onRefreshTree();
    } catch (error) {
      console.error('保存失败:', error);
      message.error('保存失败: ' + (error.message || '未知错误'));
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
    <div className="lpi-detail">
      <Form
        form={form}
        layout="vertical"
        initialValues={{
          name: detail?.name,
          description: detail?.description,
          english_description: detail?.english_description,
          type: detail?.type || 'lpi',
          category: detail?.category,
        }}
      >
        <Card
          title="LPI组件详情"
          extra={
            <Button
              type="primary"
              icon={<SaveOutlined />}
              onClick={handleSave}
              loading={loading}
            >
              保存
            </Button>
          }
        >
          <Form.Item
            name="name"
            label="名称"
            rules={[{ required: true, message: '请输入名称' }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="description"
            label="描述"
            rules={[{ required: true, message: '请输入描述' }]}
          >
            <TextArea rows={4} />
          </Form.Item>
          <Form.Item
            name="english_description"
            label="英文描述"
            rules={[{ required: true, message: '请输入英文描述' }]}
          >
            <TextArea rows={4} />
          </Form.Item>
          <Form.Item
            name="category"
            label="分类"
            rules={[{ required: true, message: '请选择分类' }]}
          >
            <Input />
          </Form.Item>
          
          {/* 其他表单项... */}
        </Card>
      </Form>
    </div>
  );
};

export default LPIDetail; 