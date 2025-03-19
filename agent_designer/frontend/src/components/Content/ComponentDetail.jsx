import React, { useState, useEffect } from 'react';
import { Spin, Tabs, Empty, message } from 'antd';
import LPIDetail from './LPIDetail';
import AgentDetail from './AgentDetail';
import CommonComponentDetail from './CommonComponentDetail';
import { getComponentDetail } from '../../services/componentService';
import './ComponentDetail.css';

const { TabPane } = Tabs;

const ComponentDetail = ({ componentInfo, onRefreshTree }) => {
  const [loading, setLoading] = useState(false);
  const [componentDetail, setComponentDetail] = useState(null);

  useEffect(() => {
    if (componentInfo && componentInfo.id) {
      fetchComponentDetail(componentInfo.type, componentInfo.id);
    } else {
      setComponentDetail(null);
    }
  }, [componentInfo]);

  const fetchComponentDetail = async (type, id) => {
    try {
      setLoading(true);
      const data = await getComponentDetail(type, id);
      setComponentDetail(data);
    } catch (error) {
      message.error('获取组件详情失败');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const renderComponentDetail = () => {
    if (!componentDetail) {
      return <Empty description="请选择一个组件" />;
    }

    switch (componentDetail.component_type || componentInfo?.type) {
      case 'lpi':
        return <LPIDetail detail={componentDetail} onRefresh={() => fetchComponentDetail(componentInfo.type, componentInfo.id)} onRefreshTree={onRefreshTree} />;
      case 'agent':
        return <AgentDetail detail={componentDetail} onRefresh={() => fetchComponentDetail(componentInfo.type, componentInfo.id)} onRefreshTree={onRefreshTree} />;
      case 'common':
        return <CommonComponentDetail detail={componentDetail} onRefresh={() => fetchComponentDetail(componentInfo.type, componentInfo.id)} onRefreshTree={onRefreshTree} />;
      default:
        return <Empty description="未知组件类型" />;
    }
  };

  return (
    <div className="component-detail">
      <Spin spinning={loading}>
        {renderComponentDetail()}
      </Spin>
    </div>
  );
};

export default ComponentDetail; 