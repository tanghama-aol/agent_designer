import React from 'react';
import { Layout, ConfigProvider, theme } from 'antd';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import zhCN from 'antd/locale/zh_CN';
import './App.css';
import EditorPage from './pages/Editor';

const { Header, Content, Footer } = Layout;

function App() {
  return (
    <ConfigProvider
      locale={zhCN}
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#1890ff',
        },
      }}
    >
      <Router>
        <Layout style={{ minHeight: '100vh' }}>
          <Routes>
            <Route path="/" element={<EditorPage />} />
          </Routes>
        </Layout>
      </Router>
    </ConfigProvider>
  );
}

export default App; 