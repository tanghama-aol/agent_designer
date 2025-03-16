import React from 'react';
import LPIDesigner from './LPIDesigner';
import AgentDesigner from './AgentDesigner';
import CommonComponent from './CommonComponents';
import './index.css';

const EditorContent = ({ component }) => {
  if (!component) {
    return (
      <div className="empty-content">
        <div className="empty-placeholder">
          <p>请从左侧选择一个组件进行编辑</p>
        </div>
      </div>
    );
  }

  // 根据组件类型渲染不同的设计器
  const renderDesigner = () => {
    switch (component.type) {
      case 'lpi':
        return <LPIDesigner component={component} />;
      case 'agent':
        return <AgentDesigner component={component} />;
      case 'common':
        return <CommonComponent component={component} />;
      default:
        return <div>未知组件类型</div>;
    }
  };

  return (
    <div className="content-container">
      {renderDesigner()}
    </div>
  );
};

export default EditorContent; 