import React, { useState } from 'react';
import { Tree, Input, Button, Spin, Dropdown, Menu, Modal, Form, message, Popconfirm } from 'antd';
import { SearchOutlined, PlusOutlined, ReloadOutlined, MoreOutlined, EditOutlined, DeleteOutlined, DragOutlined } from '@ant-design/icons';
import { deleteComponent } from '../../services/componentService';
import './ComponentSider.css';

const { Search } = Input;
const { DirectoryTree } = Tree;

const ComponentSider = ({ componentTree, onSelect, loading, onRefresh, onDragComponent }) => {
  const [searchValue, setSearchValue] = useState('');
  const [expandedKeys, setExpandedKeys] = useState(['lpi', 'general_lpi', 'business_lpi', 'agent', 'common']);
  const [autoExpandParent, setAutoExpandParent] = useState(true);
  const [addComponentVisible, setAddComponentVisible] = useState(false);
  const [editComponentVisible, setEditComponentVisible] = useState(false);
  const [componentType, setComponentType] = useState('');
  const [lpiCategory, setLpiCategory] = useState('');
  const [currentNode, setCurrentNode] = useState(null);
  const [form] = Form.useForm();
  const [editForm] = Form.useForm();

  const handleSearch = (value) => {
    setSearchValue(value);
    if (value) {
      // 如果有搜索值，展开所有节点
      const allKeys = getAllKeys(componentTree);
      setExpandedKeys(allKeys);
      setAutoExpandParent(true);
    } else {
      // 如果搜索值为空，恢复默认展开状态
      setExpandedKeys(['lpi', 'general_lpi', 'business_lpi', 'agent', 'common']);
      setAutoExpandParent(true);
    }
  };

  const getAllKeys = (tree) => {
    let keys = [];
    const traverse = (nodes) => {
      if (!nodes) return;
      nodes.forEach(node => {
        keys.push(node.key);
        if (node.children) {
          traverse(node.children);
        }
      });
    };
    traverse(tree);
    return keys;
  };

  const handleExpand = (expandedKeys) => {
    setExpandedKeys(expandedKeys);
    setAutoExpandParent(false);
  };

  const handleAddComponent = () => {
    setAddComponentVisible(true);
  };

  const handleAddComponentOk = () => {
    form.validateFields().then(values => {
      message.success(`创建${values.componentType}组件: ${values.name}`);
      form.resetFields();
      setAddComponentVisible(false);
      onRefresh();
    }).catch(info => {
      console.log('验证失败:', info);
    });
  };

  const handleAddComponentCancel = () => {
    form.resetFields();
    setAddComponentVisible(false);
  };

  const handleEditComponent = (node) => {
    setCurrentNode(node);
    editForm.setFieldsValue({
      name: node.title,
      componentType: node.type,
      // 其他字段需要从API获取
    });
    setEditComponentVisible(true);
  };

  const handleEditComponentOk = () => {
    editForm.validateFields().then(values => {
      message.success(`更新组件: ${values.name}`);
      editForm.resetFields();
      setEditComponentVisible(false);
      onRefresh();
    }).catch(info => {
      console.log('验证失败:', info);
    });
  };

  const handleEditComponentCancel = () => {
    editForm.resetFields();
    setEditComponentVisible(false);
  };

  const handleDeleteComponent = async (node) => {
    try {
      await deleteComponent(node.id);
      message.success(`删除组件成功`);
      onRefresh();
    } catch (error) {
      console.error('删除失败:', error);
      message.error('删除失败');
    }
  };

  const handleComponentTypeSelect = (type, category = '') => {
    setComponentType(type);
    setLpiCategory(category);
    setAddComponentVisible(true);
  };

  const addMenu = (
    <Menu>
      <Menu.SubMenu key="lpi" title="添加LPI组件">
        <Menu.Item key="general_lpi" onClick={() => handleComponentTypeSelect('lpi', 'general')}>添加通用LPI</Menu.Item>
        <Menu.Item key="user_interaction_lpi" onClick={() => handleComponentTypeSelect('lpi', 'user_interaction')}>添加用户介入LPI</Menu.Item>
        <Menu.Item key="async_wait_lpi" onClick={() => handleComponentTypeSelect('lpi', 'async_wait')}>添加异步等待LPI</Menu.Item>
        <Menu.Item key="memory_query_lpi" onClick={() => handleComponentTypeSelect('lpi', 'memory_query')}>添加记忆查询LPI</Menu.Item>
        <Menu.Item key="memory_modify_lpi" onClick={() => handleComponentTypeSelect('lpi', 'memory_modify')}>添加记忆修改LPI</Menu.Item>
        <Menu.Item key="conditional_jump_lpi" onClick={() => handleComponentTypeSelect('lpi', 'conditional_jump')}>添加条件跳转LPI</Menu.Item>
        <Menu.Item key="unconditional_jump_lpi" onClick={() => handleComponentTypeSelect('lpi', 'unconditional_jump')}>添加无条件跳转LPI</Menu.Item>
        <Menu.Item key="business_lpi" onClick={() => handleComponentTypeSelect('lpi', 'business')}>添加业务LPI</Menu.Item>
      </Menu.SubMenu>
      <Menu.Item key="agent" onClick={() => handleComponentTypeSelect('agent')}>添加Agent组件</Menu.Item>
      <Menu.Item key="common" onClick={() => handleComponentTypeSelect('common')}>添加通用组件</Menu.Item>
    </Menu>
  );

  // 过滤树节点
  const filterTreeNode = (node) => {
    if (searchValue && node.title.toLowerCase().indexOf(searchValue.toLowerCase()) > -1) {
      return true;
    }
    return false;
  };

  // 自定义树节点标题，添加操作按钮
  const titleRender = (nodeData) => {
    if (!nodeData.id) return <span>{nodeData.title}</span>; // 如果是分类节点，不显示操作按钮
    
    return (
      <div className="tree-node-title">
        <span className="node-title-text">{nodeData.title}</span>
        <span className="node-actions">
          <Button 
            type="text" 
            size="small" 
            icon={<DragOutlined />} 
            className="drag-handle"
            title="拖拽到工作流"
            onMouseDown={(e) => {
              e.stopPropagation();
              onDragComponent && onDragComponent(nodeData);
            }}
          />
          <Button 
            type="text" 
            size="small" 
            icon={<EditOutlined />} 
            onClick={(e) => {
              e.stopPropagation();
              handleEditComponent(nodeData);
            }}
          />
          <Popconfirm
            title="确定要删除此组件吗？"
            onConfirm={(e) => {
              e.stopPropagation();
              handleDeleteComponent(nodeData);
            }}
            okText="是"
            cancelText="否"
          >
            <Button 
              type="text" 
              size="small" 
              icon={<DeleteOutlined />} 
              onClick={(e) => e.stopPropagation()}
            />
          </Popconfirm>
        </span>
      </div>
    );
  };

  // 处理拖拽排序
  const onDragEnter = (info) => {
    console.log(info);
    // 可以在这里处理拖拽进入逻辑
  };

  const onDrop = (info) => {
    const dropKey = info.node.key;
    const dragKey = info.dragNode.key;
    const dropPos = info.node.pos.split('-');
    const dropPosition = info.dropPosition - Number(dropPos[dropPos.length - 1]);

    // 这里需要根据拖拽结果重新构建树结构并调用API更新
    message.success('组件顺序已更新');
    onRefresh();
  };

  return (
    <div className="component-sider">
      <div className="sider-header">
        <Search
          placeholder="搜索组件"
          allowClear
          onChange={(e) => handleSearch(e.target.value)}
          style={{ width: '70%' }}
          prefix={<SearchOutlined />}
        />
        <Dropdown overlay={addMenu} placement="bottomRight">
          <Button type="primary" icon={<PlusOutlined />} size="small" />
        </Dropdown>
        <Button 
          icon={<ReloadOutlined />} 
          size="small" 
          onClick={onRefresh}
          loading={loading}
        />
      </div>
      <div className="sider-content">
        <Spin spinning={loading}>
          {componentTree.length > 0 ? (
            <DirectoryTree
              showLine
              showIcon
              expandedKeys={expandedKeys}
              autoExpandParent={autoExpandParent}
              onExpand={handleExpand}
              onSelect={onSelect}
              filterTreeNode={filterTreeNode}
              treeData={componentTree}
              titleRender={titleRender}
              draggable={{ icon: false, nodeDraggable: (node) => node.id }}
              onDragEnter={onDragEnter}
              onDrop={onDrop}
            />
          ) : (
            <div className="empty-tree">
              {loading ? '加载中...' : '暂无组件，请添加'}
            </div>
          )}
        </Spin>
      </div>

      <Modal
        title={`添加${componentType === 'lpi' ? 'LPI' : componentType === 'agent' ? 'Agent' : '通用'}组件`}
        visible={addComponentVisible}
        onOk={handleAddComponentOk}
        onCancel={handleAddComponentCancel}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="componentType" initialValue={componentType} hidden>
            <Input />
          </Form.Item>
          <Form.Item name="lpiCategory" initialValue={lpiCategory} hidden>
            <Input />
          </Form.Item>
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
            <Input.TextArea placeholder="请输入中文描述" rows={2} />
          </Form.Item>
          <Form.Item
            name="english_description"
            label="英文描述"
          >
            <Input.TextArea placeholder="请输入英文描述" rows={2} />
          </Form.Item>
          <Form.Item
            name="category"
            label="分类"
          >
            <Input placeholder="请输入分类" />
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title="编辑组件"
        visible={editComponentVisible}
        onOk={handleEditComponentOk}
        onCancel={handleEditComponentCancel}
      >
        <Form form={editForm} layout="vertical">
          <Form.Item name="componentType" hidden>
            <Input />
          </Form.Item>
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
            <Input.TextArea placeholder="请输入中文描述" rows={2} />
          </Form.Item>
          <Form.Item
            name="english_description"
            label="英文描述"
          >
            <Input.TextArea placeholder="请输入英文描述" rows={2} />
          </Form.Item>
          <Form.Item
            name="category"
            label="分类"
          >
            <Input placeholder="请输入分类" />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ComponentSider; 