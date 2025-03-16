import React from 'react';
import { Form, Input, Select, Card } from 'antd';
import './index.css';

const { TextArea } = Input;
const { Option } = Select;

const CommonComponent = ({ component }) => {
  const [form] = Form.useForm();

  return (
    <div className="common-component">
      <Card title="通用组件配置">
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            name: component?.title || '',
            type: 'condition'
          }}
        >
          <Form.Item name="name" label="组件名称" rules={[{ required: true }]}>
            <Input placeholder="请输入组件名称" />
          </Form.Item>

          <Form.Item name="description" label="组件描述" rules={[{ required: true }]}>
            <TextArea rows={4} placeholder="请输入组件描述" />
          </Form.Item>

          <Form.Item name="type" label="组件类型" rules={[{ required: true }]}>
            <Select>
              <Option value="condition">条件跳转</Option>
              <Option value="executor">执行器操作</Option>
            </Select>
          </Form.Item>

          <Form.Item
            noStyle
            shouldUpdate={(prevValues, currentValues) => prevValues.type !== currentValues.type}
          >
            {({ getFieldValue }) => (
              getFieldValue('type') === 'condition' ? (
                <>
                  <h3>条件配置</h3>
                  <Form.Item name="condition" label="条件表达式" rules={[{ required: true }]}>
                    <TextArea rows={4} placeholder="请输入条件表达式" />
                  </Form.Item>
                  <Form.Item name="trueTarget" label="条件为真时跳转到">
                    <Input placeholder="请输入目标节点ID" />
                  </Form.Item>
                  <Form.Item name="falseTarget" label="条件为假时跳转到">
                    <Input placeholder="请输入目标节点ID" />
                  </Form.Item>
                </>
              ) : (
                <>
                  <h3>执行器配置</h3>
                  <Form.Item name="executorType" label="执行器类型">
                    <Select>
                      <Option value="python">Python执行器</Option>
                      <Option value="shell">Shell执行器</Option>
                      <Option value="javascript">JavaScript执行器</Option>
                    </Select>
                  </Form.Item>
                  <Form.Item name="executorCode" label="执行代码">
                    <TextArea rows={8} placeholder="请输入执行代码" />
                  </Form.Item>
                </>
              )
            )}
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default CommonComponent; 