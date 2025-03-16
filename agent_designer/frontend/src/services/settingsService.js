import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

// 获取系统配置
export const getSettings = async () => {
  try {
    const response = await axios.get(`${API_BASE_URL}/settings`);
    return response.data;
  } catch (error) {
    console.error('获取配置失败:', error);
    // 返回默认配置
    return {
      model_name: '',
      model_type: 'openai',
      api_key: '',
      api_base_url: '',
      model_deployment_name: '',
      storage_dir: ''
    };
  }
};

// 保存系统配置
export const saveSettings = async (data) => {
  const response = await axios.post(`${API_BASE_URL}/settings`, data);
  return response.data;
};
