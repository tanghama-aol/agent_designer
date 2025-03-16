import React, { useState, useEffect } from 'react';
import { Tree, Input, Button, Dropdown, Menu } from 'antd';
import { DownOutlined, PlusOutlined, EditOutlined, DeleteOutlined, MoreOutlined } from '@ant-design/icons';
import { fetchComponentTree } from '../../services/api';
import './index.css';

const { Search } = Input;

const EditorSider = ({ onSelectComponent }) => {
  const [treeData, setTreeData] = useState([]);
  const [searchValue, setSearchValue] = useState('');

  useEffect(() => {
    // 加载组件树数据
    fetchComponentTree().then(data => {
      setTreeData(data || defaultTreeData);
    });
  }, []);

  const handleSelect = (selectedKeys, info) => {
    if (selectedKeys.length > 0) {
      onSelectComponent(info.node);
    }
  };

  const handleSearch = (value) => {
    setSearchValue(value);
  };

  const handleMenuClick = (e, node) => {
    switch(e.key) {
      case 'edit':
        // 编辑操作
        break;
      case 'delete':
        // 删除操作
        break;
      case 'add':
        // 添加操作
        break;
      default:
        break;
    }
  };

  // 树节点上下文菜单
  const getDropdownMenu = (node) => (
    <Menu onClick={(e) => handleMenuClick(e, node)}>
      <Menu.Item key="edit" icon={<EditOutlined />}>编辑</Menu.Item>
      <Menu.Item key="delete" icon={<DeleteOutlined />}>删除</Menu.Item>
      <Menu.Item key="add" icon={<PlusOutlined />}>添加子项</Menu.Item>
    </Menu>
  );

  // 自定义树节点渲染
  const renderTreeNodes = (data) => {
    return data.map(item => {
      const title = (
        <div className="tree-node-title">
          <span>{item.title}</span>
          <Dropdown overlay={getDropdownMenu(item)} trigger={['click']}>
            <Button type="text" size="small" icon={<MoreOutlined />} className="node-action-btn" />
          </Dropdown>
        </div>
      );
      
      if (item.children) {
        return {
          key: item.key,
          title,
          children: renderTreeNodes(item.children),
          type: item.type
        };
      }
      
      return {
        key: item.key,
        title,
        type: item.type
      };
    });
  };

  const defaultTreeData = [
    {
      title: 'LPI组件',
      key: 'lpi',
      children: [
        { title: '获取天气', key: 'lpi-weather', type: 'lpi' },
        { title: '搜索知识库', key: 'lpi-search', type: 'lpi' }
      ]
    },
    {
      title: 'Agent组件',
      key: 'agent',
      children: [
        { title: '客服机器人', key: 'agent-customer', type: 'agent' },
        { title: '数据分析助手', key: 'agent-data', type: 'agent' }
      ]
    },
    {
      title: '通用组件',
      key: 'common',
      children: [
        { title: '条件跳转', key: 'common-condition', type: 'common' },
        { title: '继承器操作', key: 'common-executor', type: 'common' }
      ]
    }
  ];

  return (
    <div className="sider-container">
      <div className="sider-header">
        <Search
          placeholder="搜索组件"
          onChange={(e) => handleSearch(e.target.value)}
          style={{ width: '100%' }}
        />
        <Button type="primary" icon={<PlusOutlined />} size="small" style={{ marginTop: 8 }}>
          新建组件
        </Button>
      </div>
      <div className="tree-container">
        <Tree
          showIcon
          defaultExpandAll
          onSelect={handleSelect}
          treeData={renderTreeNodes(treeData)}
          switcherIcon={<DownOutlined />}
        />
      </div>
    </div>
  );
};

export default EditorSider; 