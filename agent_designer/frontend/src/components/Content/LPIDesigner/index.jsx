import React from 'react';
import { Form, Input, Select, Card, Tabs, Button } from 'antd';
import './index.css';

const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const LPIDesigner = ({ component }) => {
  const [form] = Form.useForm();

  return (
    <div className="lpi-designer">
      <Card title="LPI基本信息">
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            name: component?.title || '',
            description: '',
            type: 'rest'
          }}
        >
          <Form.Item name="name" label="LPI名称" rules={[{ required: true }]}>
            <Input placeholder="请输入LPI名称" />
          </Form.Item>

          <Form.Item name="description" label="中文描述" rules={[{ required: true }]}>
            <TextArea rows={4} placeholder="请输入LPI中文描述" />
          </Form.Item>

          <Form.Item name="englishDescription" label="英文描述">
            <TextArea rows={4} placeholder="请输入LPI英文描述" />
          </Form.Item>

          <Form.Item name="type" label="API类型" rules={[{ required: true }]}>
            <Select>
              <Option value="rest">REST API</Option>
              <Option value="python">Python API</Option>
            </Select>
          </Form.Item>

          <h3>API配置</h3>
          <Form.Item
            noStyle
            shouldUpdate={(prevValues, currentValues) => prevValues.type !== currentValues.type}
          >
            {({ getFieldValue }) => (
              getFieldValue('type') === 'rest' ? (
                <>
                  <Form.Item name="endpoint" label="接口地址" rules={[{ required: true }]}>
                    <Input placeholder="请输入接口地址" />
                  </Form.Item>
                  <Form.Item name="method" label="请求方法" rules={[{ required: true }]}>
                    <Select>
                      <Option value="GET">GET</Option>
                      <Option value="POST">POST</Option>
                      <Option value="PUT">PUT</Option>
                      <Option value="DELETE">DELETE</Option>
                    </Select>
                  </Form.Item>
                </>
              ) : (
                <Form.Item name="pythonCode" label="Python代码" rules={[{ required: true }]}>
                  <TextArea rows={8} placeholder="请输入Python代码" />
                </Form.Item>
              )
            )}
          </Form.Item>

          <h3>参数配置</h3>
          <Form.List name="params">
            {(fields, { add, remove }) => (
              <>
                {fields.map(field => (
                  <Card 
                    key={field.key} 
                    size="small" 
                    style={{ marginBottom: 16 }}
                    extra={
                      <a onClick={() => remove(field.name)}>删除</a>
                    }
                  >
                    <Form.Item
                      {...field}
                      name={[field.name, 'name']}
                      label="参数名称"
                      rules={[{ required: true }]}
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
                      name={[field.name, 'required']}
                      label="是否必填"
                    >
                      <Select>
                        <Option value={true}>是</Option>
                        <Option value={false}>否</Option>
                      </Select>
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
                  <Button type="dashed" onClick={() => add()} block>
                    添加参数
                  </Button>
                </Form.Item>
              </>
            )}
          </Form.List>

          <h3>返回值配置</h3>
          <Form.Item name="responseType" label="返回值类型" rules={[{ required: true }]}>
            <Select>
              <Option value="string">字符串</Option>
              <Option value="number">数字</Option>
              <Option value="boolean">布尔值</Option>
              <Option value="object">对象</Option>
              <Option value="array">数组</Option>
            </Select>
          </Form.Item>

          <Form.Item name="responseDescription" label="返回值描述">
            <TextArea rows={4} placeholder="请输入返回值描述" />
          </Form.Item>

          <Form.Item name="responseExample" label="返回值示例">
            <TextArea rows={4} placeholder="请输入返回值示例" />
          </Form.Item>
        </Form>
      </Card>
    </div>
  );
};

export default LPIDesigner; 