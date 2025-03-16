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
            if (node.key === 'general_lpi') {
                return {
                    ...node,
                    title: '通用LPI'
                };
            } else if (node.key === 'business_lpi') {
                return {
                    ...node,
                    title: '业务LPI'
                };
            } else if (node.key === 'expert_agent') {
                return {
                    ...node,
                    title: '专家Agent'
                };
            } else if (node.key === 'scenario_agent') {
                return {
                    ...node,
                    title: '场景Agent'
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
        <div style={{ position: 'relative', display: 'flex', width: '100%' }}>
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
          <Content className="editor-content" style={{ flex: 1 }}>
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