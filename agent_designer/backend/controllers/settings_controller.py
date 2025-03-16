from flask import Blueprint, request, jsonify
import os
import json

settings_bp = Blueprint('settings', __name__)

SETTINGS_FILE = 'settings.json'

def get_settings_file_path():
    """获取设置文件路径"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), SETTINGS_FILE)

def load_settings():
    """加载设置"""
    file_path = get_settings_file_path()
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        'model_name': '',
        'model_type': 'openai',
        'api_key': '',
        'api_base_url': '',
        'model_deployment_name': '',
        'storage_dir': ''
    }

def save_settings(settings):
    """保存设置"""
    file_path = get_settings_file_path()
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)

@settings_bp.route('/', methods=['GET'])
def get_settings():
    """获取设置"""
    settings = load_settings()
    return jsonify(settings)

@settings_bp.route('/', methods=['POST'])
def update_settings():
    """更新设置"""
    data = request.json
    save_settings(data)
    return jsonify({'message': '设置已保存'}) 