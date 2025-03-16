import React, { useState, useEffect } from 'react';
import { Layout, Button, message, Modal } from 'antd';
import { SaveOutlined, PlayCircleOutlined, StopOutlined, SettingOutlined } from '@ant-design/icons';
import ComponentSider from '../../components/Sider/ComponentSider';
import ComponentDetail from '../../components/Content/ComponentDetail';
import SettingsModal from '../../components/Settings/SettingsModal';
import { getComponentTree } from '../../services/componentService';
import './index.css';

const { Header, Sider, Content, Footer } = Layout;

const EditorPage = () => {
  const [componentTree, setComponentTree] = useState([]);
  const [selectedComponent, setSelectedComponent] = useState(null);
  const [settingsVisible, setSettingsVisible] = useState(false);
  const [loading, setLoading] = useState(false);
  const [draggedComponent, setDraggedComponent] = useState(null);
  const [siderWidth, setSiderWidth] = useState(250);

  useEffect(() => {
    fetchComponentTree();
  }, []);

  const fetchComponentTree = async () => {
    try {
      setLoading(true);
      const data = await getComponentTree();
      
      // 修改树结构，将LPI分为通用LPI和业务LPI，将Agent分为专家Agent和场景Agent
      const modifiedTree = data.map(node => {
        if (node.key === 'lpi') {
          // 找到所有LPI组件
          const lpiChildren = node.children || [];
          
          // 分类LPI组件
          const generalLpiNodes = lpiChildren.filter(child => 
            ['general', 'user_interaction', 'async_wait', 'memory_query', 
             'memory_modify', 'conditional_jump', 'unconditional_jump'].includes(child.category)
          );
          
          const businessLpiNodes = lpiChildren.filter(child => 
            child.category === 'business' || !['general', 'user_interaction', 'async_wait', 
            'memory_query', 'memory_modify', 'conditional_jump', 'unconditional_jump'].includes(child.category)
          );
          
          // 创建新的子节点
          return {
            ...node,
            children: [
              {
                title: '通用LPI',
                key: 'general_lpi',
                children: generalLpiNodes
              },
              {
                title: '业务LPI',
                key: 'business_lpi',
                children: businessLpiNodes
              }
            ]
          };
        } else if (node.key === 'agent') {
          // 找到所有Agent组件
          const agentChildren = node.children || [];
          
          // 分类Agent组件
          const expertAgentNodes = agentChildren.filter(child => 
            child.agentType === 'expert' || !child.agentType
          );
          
          const scenarioAgentNodes = agentChildren.filter(child => 
            child.agentType === 'scenario'
          );
          
          // 创建新的子节点
          return {
            ...node,
            children: [
              {
                title: '专家Agent',
                key: 'expert_agent',
                children: expertAgentNodes
              },
              {
                title: '场景Agent',
                key: 'scenario_agent',
                children: scenarioAgentNodes
              }
            ]
          };
        }
        return node;
      });
      
      setComponentTree(modifiedTree);
    } catch (error) {
      message.error('获取组件树失败');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleComponentSelect = (selectedKeys, info) => {
    if (info.node.id) {
      setSelectedComponent({
        id: info.node.id,
        type: info.node.type
      });
    }
  };

  const handleSave = () => {
    message.success('保存成功');
  };

  const handleRun = () => {
    message.info('开始运行');
  };

  const handleStop = () => {
    message.info('已停止');
  };

  const handleSettingsClick = () => {
    setSettingsVisible(true);
  };

  const handleSettingsClose = () => {
    setSettingsVisible(false);
  };

  const handleDragComponent = (component) => {
    setDraggedComponent(component);
    
    // 创建自定义事件，通知工作流编辑器
    const dragEvent = new CustomEvent('component-drag', { 
      detail: { component } 
    });
    document.dispatchEvent(dragEvent);
  };

  // 处理Sider宽度调整
  const handleSiderResize = (e) => {
    if (e.clientX > 100 && e.clientX < 500) {
      setSiderWidth(e.clientX);
    }
  };

  const handleSiderResizeStart = () => {
    document.addEventListener('mousemove', handleSiderResize);
    document.addEventListener('mouseup', handleSiderResizeEnd);
  };

  const handleSiderResizeEnd = () => {
    document.removeEventListener('mousemove', handleSiderResize);
    document.removeEventListener('mouseup', handleSiderResizeEnd);
  };

  return (
    <Layout>
      <Header className="editor-header">
        <div className="logo">Agent编辑器</div>
        <div className="header-actions">
          <Button type="primary" icon={<SaveOutlined />} onClick={handleSave}>
            保存
          </Button>
          <Button type="default" icon={<SettingOutlined />} onClick={handleSettingsClick}>
            配置
          </Button>
        </div>
      </Header>
      <Layout>
        <div style={{ position: 'relative', display: 'flex' }}>
          <Sider width={siderWidth} className="editor-sider">
            <ComponentSider 
              componentTree={componentTree} 
              onSelect={handleComponentSelect}
              loading={loading}
              onRefresh={fetchComponentTree}
              onDragComponent={handleDragComponent}
            />
          </Sider>
          <div 
            className="sider-resizer" 
            onMouseDown={handleSiderResizeStart}
          />
          <Content className="editor-content">
            <ComponentDetail 
              componentInfo={selectedComponent}
              onRefreshTree={fetchComponentTree}
              draggedComponent={draggedComponent}
            />
          </Content>
        </div>
      </Layout>
      <Footer className="editor-footer">
        <Button type="primary" icon={<SaveOutlined />} onClick={handleSave}>
          保存
        </Button>
        <Button type="primary" icon={<PlayCircleOutlined />} onClick={handleRun}>
          运行
        </Button>
        <Button danger icon={<StopOutlined />} onClick={handleStop}>
          停止
        </Button>
      </Footer>

      <SettingsModal 
        visible={settingsVisible}
        onClose={handleSettingsClose}
      />
    </Layout>
  );
};

export default EditorPage; 