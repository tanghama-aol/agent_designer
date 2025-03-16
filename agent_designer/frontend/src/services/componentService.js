import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// 获取组件树
export const getComponentTree = async () => {
  const response = await axios.get(`${API_BASE_URL}/components/tree`);
  return response.data;
};

// 获取组件详情
export const getComponentDetail = async (componentId) => {
  const response = await axios.get(`${API_BASE_URL}/components/${componentId}`);
  return response.data;
};

// 创建LPI组件
export const createLPI = async (data) => {
  const response = await axios.post(`${API_BASE_URL}/components/lpi`, data);
  return response.data;
};

// 更新LPI组件
export const updateLPI = async (componentId, data) => {
  const response = await axios.put(`${API_BASE_URL}/components/lpi/${componentId}`, data);
  return response.data;
};

// 创建Agent组件
export const createAgent = async (data) => {
  const response = await axios.post(`${API_BASE_URL}/components/agent`, data);
  return response.data;
};

// 更新Agent组件
export const updateAgent = async (componentId, data) => {
  const response = await axios.put(`${API_BASE_URL}/components/agent/${componentId}`, data);
  return response.data;
};

// 创建通用组件
export const createCommonComponent = async (data) => {
  const response = await axios.post(`${API_BASE_URL}/components/common`, data);
  return response.data;
};

// 更新通用组件
export const updateCommonComponent = async (componentId, data) => {
  const response = await axios.put(`${API_BASE_URL}/components/common/${componentId}`, data);
  return response.data;
};

// 删除组件
export const deleteComponent = async (componentId) => {
  const response = await axios.delete(`${API_BASE_URL}/components/${componentId}`);
  return response.data;
};

// 获取工作流详情
export const getWorkflowDetail = async (workflowId) => {
  const response = await axios.get(`${API_BASE_URL}/workflows/${workflowId}`);
  return response.data;
};

// 创建工作流
export const createWorkflow = async (data) => {
  const response = await axios.post(`${API_BASE_URL}/workflows`, data);
  return response.data;
};

// 更新工作流
export const updateWorkflow = async (workflowId, data) => {
  const response = await axios.put(`${API_BASE_URL}/workflows/${workflowId}`, data);
  return response.data;
};

// 删除工作流
export const deleteWorkflow = async (workflowId) => {
  const response = await axios.delete(`${API_BASE_URL}/workflows/${workflowId}`);
  return response.data;
};

// 测试工作流
export const testWorkflow = async (workflowId, data) => {
  const response = await axios.post(`${API_BASE_URL}/workflows/${workflowId}/test`, data);
  return response.data;
};

// 执行工作流
export const executeWorkflow = async (workflowId, data) => {
  const response = await axios.post(`${API_BASE_URL}/workflows/${workflowId}/execute`, data);
  return response.data;
};

// 发布工作流
export const publishWorkflow = async (workflowId) => {
  const response = await axios.post(`${API_BASE_URL}/workflows/${workflowId}/publish`);
  return response.data;
}; 