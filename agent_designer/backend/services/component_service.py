from models.component import Component
from models import db
import json
import os
from pathlib import Path
import glob
import uuid
import re

# 获取后端目录路径
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BACKEND_DIR, 'data')
AGENT_DIR = os.path.join(DATA_DIR, 'agent')
LPI_BUSI_DIR = os.path.join(DATA_DIR, 'lpi', 'busi')
LPI_COMMON_DIR = os.path.join(DATA_DIR, 'lpi', 'common')

# 文件名前缀
FILE_PREFIX = {
    'scenario_agent': 'scenario_',
    'expert_agent': 'expert_',
    'workflow': 'workflow_',
    'busi_lpi': 'busi_',
    'common_lpi': 'common_'
}

def to_snake_case(name):
    """将名称转换为下划线形式的文件名"""
    # 转为小写并替换非字母数字为下划线
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    
    # 移除前后的下划线
    name = name.strip('_')
    
    return name

class ComponentService:
    """组件服务，用于处理Agent和LPI组件"""
    
    @staticmethod
    def get_component_tree():
        """获取组件树结构"""
        try:
            # 构建组件树
            tree = [
                {
            'title': '通用LPI',
            'key': 'general_lpi',
                    'children': ComponentService._get_common_lpis()
                },
                {
                    'title': '业务LPI',
                    'key': 'business_lpi',
                    'children': ComponentService._get_business_lpis()
                },
                {
                    'title': '专家Agent',
                    'key': 'expert_agent',
                    'children': ComponentService._get_expert_agents()
                },
                {
                    'title': '场景Agent',
                    'key': 'scenario_agent',
                    'children': ComponentService._get_scenario_agents()
                }
            ]
            return tree
        except Exception as e:
            print(f"获取组件树错误: {str(e)}")
            return []
    
    @staticmethod
    def _get_common_lpis():
        """获取通用LPI列表"""
        lpis = []
        try:
            for file_path in glob.glob(os.path.join(LPI_COMMON_DIR, 'common_*.json')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lpi = json.load(f)
                    lpis.append({
                        'title': lpi.get('name', ''),
                        'key': f"lpi_{lpi.get('id', '')}",
                        'id': lpi.get('id', ''),
                        'type': 'lpi',
                        'category': lpi.get('category', ''),
                        'filename': os.path.basename(file_path).replace('.json', '')
                    })
        except Exception as e:
            print(f"获取通用LPI错误: {str(e)}")
        return lpis
    
    @staticmethod
    def _get_business_lpis():
        """获取业务LPI列表"""
        lpis = []
        
        try:
            lpi_categories = {}
            
            # 读取所有业务LPI
            for file_path in glob.glob(os.path.join(LPI_BUSI_DIR, 'busi_*.json')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lpi = json.load(f)
                    category = lpi.get('category', '其他')
                    
                    if category not in lpi_categories:
                        lpi_categories[category] = []
                    
                    lpi_categories[category].append({
                        'title': lpi.get('name', ''),
                        'key': f"lpi_{lpi.get('id', '')}",
                        'id': lpi.get('id', ''),
                        'type': 'lpi',
                        'category': category,
                        'filename': os.path.basename(file_path).replace('.json', '')
                    })
            
            # 将分类添加到树中
            for category, category_lpis in lpi_categories.items():
                lpis.append({
                    'title': category,
                    'key': f"lpi_category_{category}",
                    'children': category_lpis
                })
        except Exception as e:
            print(f"获取业务LPI错误: {str(e)}")
        
        return lpis
    
    @staticmethod
    def _get_expert_agents():
        """获取专家Agent列表"""
        agents = []
        try:
            for file_path in glob.glob(os.path.join(AGENT_DIR, 'expert_*.json')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    agent = json.load(f)
                    agents.append({
                        'title': agent.get('name', ''),
                        'key': f"agent_{agent.get('id', '')}",
                        'id': agent.get('id', ''),
                        'type': 'agent',
                        'category': agent.get('category', ''),
                        'filename': os.path.basename(file_path).replace('.json', '')
                    })
        except Exception as e:
            print(f"获取专家Agent错误: {str(e)}")
        return agents
    
    @staticmethod
    def _get_scenario_agents():
        """获取场景Agent列表"""
        agents = []
        try:
            for file_path in glob.glob(os.path.join(AGENT_DIR, 'scenario_*.json')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    agent = json.load(f)
                    agents.append({
                        'title': agent.get('name', ''),
                        'key': f"agent_{agent.get('id', '')}",
                        'id': agent.get('id', ''),
                        'type': 'agent',
                        'category': 'scenario',
                        'filename': os.path.basename(file_path).replace('.json', '')
                    })
        except Exception as e:
            print(f"获取场景Agent错误: {str(e)}")
        return agents
    
    @staticmethod
    def get_component_detail(component_id, component_type):
        """获取组件详情"""
        try:
            if component_type == 'agent':
                # 查找所有Agent文件
                for file_pattern in ['expert_*.json', 'scenario_*.json']:
                    for file_path in glob.glob(os.path.join(AGENT_DIR, file_pattern)):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            agent = json.load(f)
                            if agent.get('id') == component_id:
                                # 获取工作流
                                agent['workflows'] = ComponentService._get_agent_workflows(component_id)
                                agent['filename'] = os.path.basename(file_path).replace('.json', '')
                                return agent
            
            elif component_type == 'lpi':
                # 检查通用LPI
                for file_path in glob.glob(os.path.join(LPI_COMMON_DIR, 'common_*.json')):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lpi = json.load(f)
                        if lpi.get('id') == component_id:
                            lpi['filename'] = os.path.basename(file_path).replace('.json', '')
                            return lpi
                
                # 检查业务LPI
                for file_path in glob.glob(os.path.join(LPI_BUSI_DIR, 'busi_*.json')):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lpi = json.load(f)
                        if lpi.get('id') == component_id:
                            lpi['filename'] = os.path.basename(file_path).replace('.json', '')
                            return lpi
            
            return None
        except Exception as e:
            print(f"获取组件详情错误: {str(e)}")
            return None
    
    @staticmethod
    def _get_agent_workflows(agent_id):
        """获取Agent的工作流"""
        workflows = []
        try:
            # 先查找文件名为workflow_开头的所有文件
            for file_path in glob.glob(os.path.join(AGENT_DIR, 'workflow_*.json')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    workflow = json.load(f)
                    if workflow.get('agent_id') == agent_id:
                        workflow['filename'] = os.path.basename(file_path).replace('.json', '')
                        workflows.append(workflow)
        except Exception as e:
            print(f"获取Agent工作流错误: {str(e)}")
        return workflows
    
    @staticmethod
    def update_component(component_id, component_type, updated_data):
        """更新组件信息"""
        try:
            file_path = None
            
            if component_type == 'agent':
                # 查找所有Agent文件
                for file_pattern in ['expert_*.json', 'scenario_*.json']:
                    for file_path_candidate in glob.glob(os.path.join(AGENT_DIR, file_pattern)):
                        with open(file_path_candidate, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if data.get('id') == component_id:
                                file_path = file_path_candidate
                                break
                    if file_path:
                        break
            
            elif component_type == 'lpi':
                # 查找所有LPI文件
                for dir_path, file_pattern in [(LPI_BUSI_DIR, 'busi_*.json'), (LPI_COMMON_DIR, 'common_*.json')]:
                    for file_path_candidate in glob.glob(os.path.join(dir_path, file_pattern)):
                        with open(file_path_candidate, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if data.get('id') == component_id:
                                file_path = file_path_candidate
                                break
                    if file_path:
                        break
            
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # 更新数据
                for key, value in updated_data.items():
                    if key != 'id' and key != 'workflows' and key != 'filename':  # 不更新ID和工作流
                        data[key] = value
                
                # 保存回文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                # 如果存在Markdown工作流，单独保存
                if 'workflow_markdown' in updated_data:
                    for workflow in ComponentService._get_agent_workflows(component_id):
                        workflow_file = os.path.join(AGENT_DIR, f"{workflow['filename']}.json")
                        with open(workflow_file, 'r', encoding='utf-8') as f:
                            workflow_data = json.load(f)
                        
                        workflow_data['markdown_content'] = updated_data['workflow_markdown']
                        
                        with open(workflow_file, 'w', encoding='utf-8') as f:
                            json.dump(workflow_data, f, ensure_ascii=False, indent=2)
                
                return True
            
            return False
        except Exception as e:
            print(f"更新组件错误: {str(e)}")
            return False
    
    @staticmethod
    def update_workflow(workflow_id, updated_data):
        """更新工作流"""
        try:
            # 查找工作流文件
            workflow_file = None
            for file_path in glob.glob(os.path.join(AGENT_DIR, 'workflow_*.json')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    workflow = json.load(f)
                    if workflow.get('id') == workflow_id:
                        workflow_file = file_path
                        break
            
            if workflow_file:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    workflow = json.load(f)
                
                # 更新节点和边
                if 'nodes' in updated_data:
                    workflow['nodes'] = updated_data['nodes']
                
                if 'edges' in updated_data:
                    workflow['edges'] = updated_data['edges']
                
                # 保存回文件
                with open(workflow_file, 'w', encoding='utf-8') as f:
                    json.dump(workflow, f, ensure_ascii=False, indent=2)
                
                return True
            
            return False
        except Exception as e:
            print(f"更新工作流错误: {str(e)}")
            return False
    
    @staticmethod
    def create_workflow(workflow_data):
        """创建新工作流"""
        try:
            # 确保有ID
            if 'id' not in workflow_data:
                workflow_data['id'] = str(uuid.uuid4())
            
            # 生成文件名
            workflow_name = workflow_data.get('name', f"Workflow_{workflow_data['id']}")
            filename = f"workflow_{to_snake_case(workflow_name)}"
            workflow_data['filename'] = filename
            
            file_path = os.path.join(AGENT_DIR, f"{filename}.json")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, ensure_ascii=False, indent=2)
            
            return workflow_data
        except Exception as e:
            print(f"创建工作流错误: {str(e)}")
            return None

# 导出服务实例
component_service = ComponentService()

def create_lpi(data):
    """创建LPI组件"""
    lpi = Component(
        name=data.get('name'),
        description=data.get('description'),
        english_description=data.get('english_description'),
        component_type='lpi',
        category=data.get('category', '默认分类')
    )
    
    # 构建LPI内容
    content = {
        'api_type': data.get('api_type'),
        'endpoint': data.get('endpoint'),
        'method': data.get('method'),
        'input_params': data.get('input_params', []),
        'output_params': data.get('output_params', []),
        'examples': data.get('examples', [])
    }
    
    lpi.content_obj = content
    
    db.session.add(lpi)
    db.session.commit()
    
    return lpi

def update_lpi(component_id, data):
    """更新LPI组件"""
    lpi = Component.query.get_or_404(component_id)
    
    if lpi.component_type != 'lpi':
        raise ValueError("指定的组件不是LPI类型")
    
    lpi.name = data.get('name', lpi.name)
    lpi.description = data.get('description', lpi.description)
    lpi.english_description = data.get('english_description', lpi.english_description)
    lpi.category = data.get('category', lpi.category)
    
    # 更新LPI内容
    content = lpi.content_obj
    content['api_type'] = data.get('api_type', content.get('api_type'))
    content['endpoint'] = data.get('endpoint', content.get('endpoint'))
    content['method'] = data.get('method', content.get('method'))
    content['input_params'] = data.get('input_params', content.get('input_params', []))
    content['output_params'] = data.get('output_params', content.get('output_params', []))
    content['examples'] = data.get('examples', content.get('examples', []))
    
    lpi.content_obj = content
    
    db.session.commit()
    
    return lpi

def create_agent(data):
    """创建Agent组件"""
    agent = Component(
        name=data.get('name'),
        description=data.get('description'),
        english_description=data.get('english_description'),
        component_type='agent',
        category=data.get('category', '默认分类')
    )
    
    # 构建Agent内容
    content = {
        'input_params': data.get('input_params', []),
        'output_params': data.get('output_params', []),
        'examples': data.get('examples', [])
    }
    
    agent.content_obj = content
    
    db.session.add(agent)
    db.session.commit()
    
    return agent

def update_agent(component_id, data):
    """更新Agent组件"""
    agent = Component.query.get_or_404(component_id)
    
    if agent.component_type != 'agent':
        raise ValueError("指定的组件不是Agent类型")
    
    agent.name = data.get('name', agent.name)
    agent.description = data.get('description', agent.description)
    agent.english_description = data.get('english_description', agent.english_description)
    agent.category = data.get('category', agent.category)
    
    # 更新Agent内容
    content = agent.content_obj
    content['input_params'] = data.get('input_params', content.get('input_params', []))
    content['output_params'] = data.get('output_params', content.get('output_params', []))
    content['examples'] = data.get('examples', content.get('examples', []))
    
    agent.content_obj = content
    
    db.session.commit()
    
    return agent

def create_common_component(data):
    """创建通用组件"""
    component = Component(
        name=data.get('name'),
        description=data.get('description'),
        english_description=data.get('english_description'),
        component_type='common',
        category=data.get('category', '默认分类')
    )
    
    # 构建通用组件内容
    content = {
        'component_subtype': data.get('component_subtype'),  # condition, executor
        'config': data.get('config', {})
    }
    
    component.content_obj = content
    
    db.session.add(component)
    db.session.commit()
    
    return component

def update_common_component(component_id, data):
    """更新通用组件"""
    component = Component.query.get_or_404(component_id)
    
    if component.component_type != 'common':
        raise ValueError("指定的组件不是通用组件类型")
    
    component.name = data.get('name', component.name)
    component.description = data.get('description', component.description)
    component.english_description = data.get('english_description', component.english_description)
    component.category = data.get('category', component.category)
    
    # 更新通用组件内容
    content = component.content_obj
    content['component_subtype'] = data.get('component_subtype', content.get('component_subtype'))
    content['config'] = data.get('config', content.get('config', {}))
    
    component.content_obj = content
    
    db.session.commit()
    
    return component

def delete_component(component_id):
    """删除组件"""
    component = Component.query.get_or_404(component_id)
    db.session.delete(component)
    db.session.commit()
    return True 