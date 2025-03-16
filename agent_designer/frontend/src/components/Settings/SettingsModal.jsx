import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, Button, message } from 'antd';
import { saveSettings, getSettings } from '../../services/settingsService';

const { Option } = Select;

const SettingsModal = ({ visible, onClose }) => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (visible) {
      fetchSettings();
    }
  }, [visible]);

  const fetchSettings = async () => {
    try {
      setLoading(true);
      const settings = await getSettings();
      form.setFieldsValue(settings);
    } catch (error) {
      console.error('获取配置失败:', error);
      message.error('获取配置失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      await saveSettings(values);
      message.success('配置保存成功');
      onClose();
    } catch (error) {
      console.error('保存配置失败:', error);
      message.error('保存配置失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal
      title="系统配置"
      open={visible}
      onCancel={onClose}
      footer={[
        <Button key="cancel" onClick={onClose}>
          取消
        </Button>,
        <Button key="save" type="primary" loading={loading} onClick={handleSave}>
          保存
        </Button>
      ]}
      width={600}
    >
      <Form form={form} layout="vertical">
        <h3>大模型配置</h3>
        <Form.Item name="model_name" label="大模型名称" rules={[{ required: true, message: '请输入大模型名称' }]}>
          <Input placeholder="请输入大模型名称" />
        </Form.Item>
        <Form.Item name="model_type" label="大模型类型" rules={[{ required: true, message: '请选择大模型类型' }]}>
          <Select placeholder="请选择大模型类型">
            <Option value="openai">OpenAI</Option>
            <Option value="azureopenai">Azure OpenAI</Option>
            <Option value="claude">Claude</Option>
          </Select>
        </Form.Item>
        <Form.Item name="api_key" label="API Key" rules={[{ required: true, message: '请输入API Key' }]}>
          <Input.Password placeholder="请输入API Key" />
        </Form.Item>
        <Form.Item name="api_base_url" label="API Base URL">
          <Input placeholder="请输入API Base URL" />
        </Form.Item>
        <Form.Item name="model_deployment_name" label="部署名称/模型名称">
          <Input placeholder="请输入部署名称或模型名称" />
        </Form.Item>
        
        <h3>存储配置</h3>
        <Form.Item name="storage_dir" label="存储目录">
          <Input placeholder="请输入存储目录路径" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default SettingsModal;
