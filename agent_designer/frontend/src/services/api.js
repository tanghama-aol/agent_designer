import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 组件相关API
export const fetchComponents = (type, category) => {
  const params = {};
  if (type) params.type = type;
  if (category) params.category = category;
  
  return api.get('/components/', { params })
    .then(response => response.data)
    .catch(error => {
      console.error('获取组件列表失败:', error);
      return [];
    });
};

export const fetchComponentTree = () => {
  return api.get('/components/tree')
    .then(response => response.data)
    .catch(error => {
      console.error('获取组件树失败:', error);
      // 返回本地模拟数据
      return [
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
    });
};

export const fetchComponentDetail = (id) => {
  return api.get(`/components/${id}`)
    .then(response => response.data)
    .catch(error => {
      console.error('获取组件详情失败:', error);
      return null;
    });
};

export const createComponent = (data) => {
  return api.post('/components/', data)
    .then(response => response.data)
    .catch(error => {
      console.error('创建组件失败:', error);
      throw error;
    });
};

export const updateComponent = (id, data) => {
  return api.put(`/components/${id}`, data)
    .then(response => response.data)
    .catch(error => {
      console.error('更新组件失败:', error);
      throw error;
    });
};

export const deleteComponent = (id) => {
  return api.delete(`/components/${id}`)
    .then(response => response.data)
    .catch(error => {
      console.error('删除组件失败:', error);
      throw error;
    });
};

// 工作流相关API
export const fetchWorkflows = (agentId) => {
  const params = {};
  if (agentId) params.agent_id = agentId;
  
  return api.get('/workflows/', { params })
    .then(response => response.data)
    .catch(error => {
      console.error('获取工作流列表失败:', error);
      return [];
    });
};

export const fetchWorkflowDetail = (id) => {
  return api.get(`/workflows/${id}`)
    .then(response => response.data)
    .catch(error => {
      console.error('获取工作流详情失败:', error);
      return null;
    });
};

export const createWorkflow = (data) => {
  return api.post('/workflows/', data)
    .then(response => response.data)
    .catch(error => {
      console.error('创建工作流失败:', error);
      throw error;
    });
};

export const updateWorkflow = (id, data) => {
  return api.put(`/workflows/${id}`, data)
    .then(response => response.data)
    .catch(error => {
      console.error('更新工作流失败:', error);
      throw error;
    });
};

export const deleteWorkflow = (id) => {
  return api.delete(`/workflows/${id}`)
    .then(response => response.data)
    .catch(error => {
      console.error('删除工作流失败:', error);
      throw error;
    });
};

export const testWorkflow = (id, input) => {
  return api.post(`/workflows/${id}/test`, input)
    .then(response => response.data)
    .catch(error => {
      console.error('测试工作流失败:', error);
      throw error;
    });
};

export default api; 