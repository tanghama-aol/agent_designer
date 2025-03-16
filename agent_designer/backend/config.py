import os

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = 'sqlite:///agent_designer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    SECRET_KEY = 'agent-designer-secret-key'
    DEBUG = True
    
    # 跨域配置
    CORS_HEADERS = 'Content-Type'
    
    # 文件存储路径
    STORAGE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'storage')
    
    # 确保存储目录存在
    @staticmethod
    def init_app(app):
        os.makedirs(Config.STORAGE_DIR, exist_ok=True) 