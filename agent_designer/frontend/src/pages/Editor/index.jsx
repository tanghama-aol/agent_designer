import React, { useState } from 'react';
import { Layout, Button, Modal, Form, Input, Select, message } from 'antd';
import { SaveOutlined, PlayCircleOutlined, StopOutlined, EyeOutlined, CloudUploadOutlined, CloudDownloadOutlined, DeleteOutlined, SettingOutlined } from '@ant-design/icons';
import EditorSider from '../../components/Sider';
import EditorContent from '../../components/Content';
import './index.css';

const { Header, Sider, Content, Footer } = Layout;

const EditorPage = () => {
  const [settingsVisible, setSettingsVisible] = useState(false);
  const [currentComponent, setCurrentComponent] = useState(null);
  
  const saveComponent = () => {
    message.success('组件已保存');
  };
  
  const previewComponent = () => {
    message.info('预览功能开发中');
  };

  const publishComponent = () => {
    message.success('组件已发布');
  };

  const deleteComponent = () => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除此组件吗？此操作不可撤销。',
      onOk() {
        message.success('组件已删除');
      }
    });
  };

  return (
    <Layout style={{ height: '100vh' }}>
      <Header className="editor-header">
        <div className="logo">Agent设计器</div>
        <div className="header-actions">
          <Button icon={<SaveOutlined />} type="primary" onClick={saveComponent}>保存</Button>
          <Button icon={<EyeOutlined />} onClick={previewComponent}>预览</Button>
          <Button icon={<CloudUploadOutlined />} onClick={publishComponent}>发布</Button>
          <Button icon={<DeleteOutlined />} danger onClick={deleteComponent}>删除</Button>
          <Button icon={<CloudDownloadOutlined />}>导入</Button>
          <Button icon={<CloudUploadOutlined />}>导出</Button>
          <Button icon={<SettingOutlined />} onClick={() => setSettingsVisible(true)}>配置</Button>
        </div>
      </Header>
      <Layout>
        <Sider width={250} className="editor-sider">
          <EditorSider onSelectComponent={setCurrentComponent} />
        </Sider>
        <Content className="editor-content">
          <EditorContent component={currentComponent} />
        </Content>
      </Layout>
      <Footer className="editor-footer">
        <Button icon={<SaveOutlined />} type="primary">保存</Button>
        <Button icon={<PlayCircleOutlined />} type="primary">运行</Button>
        <Button icon={<StopOutlined />} danger>停止</Button>
      </Footer>
      
      <SettingsModal visible={settingsVisible} onClose={() => setSettingsVisible(false)} />
    </Layout>
  );
};

const SettingsModal = ({ visible, onClose }) => {
  const [form] = Form.useForm();
  
  const handleSave = () => {
    form.validateFields().then(values => {
      message.success('配置已保存');
      onClose();
    });
  };
  
  return (
    <Modal
      title="系统配置"
      visible={visible}
      onCancel={onClose}
      onOk={handleSave}
      width={600}
    >
      <Form form={form} layout="vertical">
        <h3>大模型配置</h3>
        <Form.Item name="modelName" label="大模型名称" rules={[{ required: true }]}>
          <Input placeholder="请输入大模型名称" />
        </Form.Item>
        <Form.Item name="modelType" label="大模型类型" rules={[{ required: true }]}>
          <Select placeholder="请选择大模型类型">
            <Select.Option value="openai">OpenAI</Select.Option>
            <Select.Option value="azureopenai">Azure OpenAI</Select.Option>
            <Select.Option value="claude">Claude</Select.Option>
          </Select>
        </Form.Item>
        <Form.Item name="apiKey" label="API Key" rules={[{ required: true }]}>
          <Input.Password placeholder="请输入API Key" />
        </Form.Item>
        <Form.Item name="apiBaseUrl" label="API Base URL">
          <Input placeholder="请输入API Base URL" />
        </Form.Item>
        <Form.Item name="deploymentName" label="部署名称/模型名称">
          <Input placeholder="请输入部署名称或模型名称" />
        </Form.Item>
        
        <h3>存储配置</h3>
        <Form.Item name="storageDir" label="存储目录">
          <Input placeholder="请输入存储目录路径" />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default EditorPage; 