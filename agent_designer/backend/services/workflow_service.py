from models.workflow import Workflow
from models.component import Component
from models import db
import json
import requests
import importlib.util
import sys
from pathlib import Path

def get_workflow_detail(workflow_id):
    """获取工作流详情"""
    workflow = Workflow.query.get_or_404(workflow_id)
    return workflow.to_dict()

def create_workflow(data):
    """创建工作流"""
    workflow = Workflow(
        name=data.get('name'),
        description=data.get('description'),
        agent_id=data.get('agent_id')
    )
    
    # 设置节点和边
    if 'nodes' in data:
        workflow.nodes_obj = data['nodes']
    if 'edges' in data:
        workflow.edges_obj = data['edges']
    
    db.session.add(workflow)
    db.session.commit()
    
    return workflow

def update_workflow(workflow_id, data):
    """更新工作流"""
    workflow = Workflow.query.get_or_404(workflow_id)
    
    workflow.name = data.get('name', workflow.name)
    workflow.description = data.get('description', workflow.description)
    
    # 更新节点和边
    if 'nodes' in data:
        workflow.nodes_obj = data['nodes']
    if 'edges' in data:
        workflow.edges_obj = data['edges']
    if 'status' in data:
        workflow.status = data['status']
    if 'version' in data:
        workflow.version = data['version']
    
    db.session.commit()
    
    return workflow

def delete_workflow(workflow_id):
    """删除工作流"""
    workflow = Workflow.query.get_or_404(workflow_id)
    db.session.delete(workflow)
    db.session.commit()
    return True

def execute_workflow(workflow_id, input_data):
    """执行工作流"""
    workflow = Workflow.query.get_or_404(workflow_id)
    
    # 获取开始节点
    start_node = workflow.get_start_node()
    if not start_node:
        raise ValueError("工作流没有开始节点")
    
    # 执行结果
    result = {
        'workflow_id': workflow_id,
        'workflow_name': workflow.name,
        'steps': [],
        'final_result': None
    }
    
    # 当前节点和数据
    current_node = start_node
    current_data = input_data
    
    # 执行工作流
    while current_node:
        # 执行当前节点
        node_result = execute_node(current_node, current_data)
        
        # 记录步骤
        step = {
            'node_id': current_node.get('id'),
            'node_name': current_node.get('data', {}).get('name', '未命名节点'),
            'node_type': current_node.get('type'),
            'input': current_data,
            'output': node_result
        }
        result['steps'].append(step)
        
        # 更新当前数据
        current_data = node_result
        
        # 如果是结束节点，则结束执行
        if current_node.get('type') == 'end':
            result['final_result'] = current_data
            break
        
        # 获取下一个节点
        next_node = get_next_node(workflow, current_node.get('id'), current_data)
        current_node = next_node
    
    return result

def execute_node(node, input_data):
    """执行节点"""
    node_type = node.get('type')
    node_data = node.get('data', {})
    
    # 开始节点
    if node_type == 'start':
        return input_data
    
    # 结束节点
    if node_type == 'end':
        return input_data
    
    # 执行LPI节点
    if node_type == 'lpi':
        return execute_lpi_node(node_data, input_data)
    
    # 执行Agent节点
    if node_type == 'agent':
        return execute_agent_node(node_data, input_data)
    
    # 执行通用组件节点
    if node_type == 'common':
        return execute_common_node(node_data, input_data)
    
    # 未知节点类型
    return input_data

def execute_lpi_node(node_data, input_data):
    """执行LPI节点"""
    component_id = node_data.get('component_id')
    if not component_id:
        raise ValueError("LPI节点没有指定组件ID")
    
    # 获取LPI组件
    component = Component.query.get_or_404(component_id)
    if component.component_type != 'lpi':
        raise ValueError("指定的组件不是LPI类型")
    
    lpi_details = component.get_lpi_details()
    api_type = lpi_details.get('api_type')
    
    # REST API
    if api_type == 'rest':
        endpoint = lpi_details.get('endpoint')
        method = lpi_details.get('method', 'POST').lower()
        
        # 调用REST API
        if method == 'get':
            response = requests.get(endpoint, params=input_data)
        else:
            response = requests.post(endpoint, json=input_data)
        
        if response.status_code != 200:
            raise Exception(f"API调用失败: {response.status_code} - {response.text}")
        
        return response.json()
    
    # Python API
    elif api_type == 'python':
        module_path = lpi_details.get('endpoint')
        if not module_path:
            raise ValueError("Python API没有指定模块路径")
        
        # 加载Python模块
        module_name = Path(module_path).stem
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        
        # 调用函数
        function_name = lpi_details.get('method', 'main')
        if not hasattr(module, function_name):
            raise ValueError(f"Python模块中没有找到函数: {function_name}")
        
        function = getattr(module, function_name)
        return function(input_data)
    
    else:
        raise ValueError(f"不支持的API类型: {api_type}")

def execute_agent_node(node_data, input_data):
    """执行Agent节点"""
    component_id = node_data.get('component_id')
    if not component_id:
        raise ValueError("Agent节点没有指定组件ID")
    
    # 获取Agent组件
    component = Component.query.get_or_404(component_id)
    if component.component_type != 'agent':
        raise ValueError("指定的组件不是Agent类型")
    
    # 获取Agent的工作流
    workflows = Workflow.query.filter_by(agent_id=component_id, status='published').all()
    if not workflows:
        raise ValueError("Agent没有已发布的工作流")
    
    # 使用最新版本的工作流
    workflow = max(workflows, key=lambda w: w.version)
    
    # 执行工作流
    result = execute_workflow(workflow.id, input_data)
    return result.get('final_result')

def execute_common_node(node_data, input_data):
    """执行通用组件节点"""
    component_id = node_data.get('component_id')
    if not component_id:
        raise ValueError("通用组件节点没有指定组件ID")
    
    # 获取通用组件
    component = Component.query.get_or_404(component_id)
    if component.component_type != 'common':
        raise ValueError("指定的组件不是通用组件类型")
    
    common_details = component.get_common_details()
    subtype = common_details.get('component_subtype')
    
    # 条件组件
    if subtype == 'condition':
        return execute_condition_component(common_details, input_data)
    
    # 执行器组件
    elif subtype == 'executor':
        return execute_executor_component(common_details, input_data)
    
    else:
        raise ValueError(f"不支持的通用组件子类型: {subtype}")

def execute_condition_component(component_details, input_data):
    """执行条件组件"""
    config = component_details.get('config', {})
    condition_type = config.get('condition_type')
    
    # 简单条件判断
    if condition_type == 'simple':
        field = config.get('field')
        operator = config.get('operator')
        value = config.get('value')
        
        if field not in input_data:
            return False
        
        field_value = input_data[field]
        
        if operator == 'eq':
            return field_value == value
        elif operator == 'ne':
            return field_value != value
        elif operator == 'gt':
            return field_value > value
        elif operator == 'lt':
            return field_value < value
        elif operator == 'contains':
            return value in field_value
        else:
            return False
    
    # 复杂条件判断
    elif condition_type == 'complex':
        expression = config.get('expression')
        # 这里可以使用eval或者更安全的方式执行表达式
        # 简化实现，实际应用中应该使用更安全的方式
        locals_dict = {'input': input_data}
        try:
            return eval(expression, {"__builtins__": {}}, locals_dict)
        except:
            return False
    
    return False

def execute_executor_component(component_details, input_data):
    """执行执行器组件"""
    config = component_details.get('config', {})
    executor_type = config.get('executor_type')
    
    # 数据转换
    if executor_type == 'transform':
        transform_type = config.get('transform_type')
        
        if transform_type == 'map':
            mapping = config.get('mapping', {})
            result = {}
            for target_key, source_path in mapping.items():
                # 简单实现，支持点号路径
                value = input_data
                for key in source_path.split('.'):
                    if isinstance(value, dict) and key in value:
                        value = value[key]
                    else:
                        value = None
                        break
                result[target_key] = value
            return result
        
        elif transform_type == 'filter':
            fields = config.get('fields', [])
            result = {}
            for field in fields:
                if field in input_data:
                    result[field] = input_data[field]
            return result
        
        else:
            return input_data
    
    # 外部调用
    elif executor_type == 'external':
        url = config.get('url')
        method = config.get('method', 'POST').lower()
        
        if not url:
            return input_data
        
        try:
            if method == 'get':
                response = requests.get(url, params=input_data)
            else:
                response = requests.post(url, json=input_data)
            
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return input_data
    
    return input_data

def get_next_node(workflow, current_node_id, current_data):
    """获取下一个节点"""
    # 获取所有从当前节点出发的边
    outgoing_edges = []
    for edge in workflow.edges_obj:
        if edge.get('source') == current_node_id:
            outgoing_edges.append(edge)
    
    if not outgoing_edges:
        return None
    
    # 如果只有一条边，直接返回目标节点
    if len(outgoing_edges) == 1:
        target_id = outgoing_edges[0].get('target')
        return workflow.get_node_by_id(target_id)
    
    # 如果有多条边，需要根据条件判断
    for edge in outgoing_edges:
        edge_data = edge.get('data', {})
        condition = edge_data.get('condition')
        
        # 如果没有条件，默认选择这条边
        if not condition:
            target_id = edge.get('target')
            return workflow.get_node_by_id(target_id)
        
        # 执行条件判断
        try:
            locals_dict = {'input': current_data}
            result = eval(condition, {"__builtins__": {}}, locals_dict)
            if result:
                target_id = edge.get('target')
                return workflow.get_node_by_id(target_id)
        except:
            continue
    
    # 如果所有条件都不满足，返回None
    return None

def test_workflow(workflow_id, input_data):
    workflow = Workflow.query.get_or_404(workflow_id)
    # 这里实现工作流测试逻辑
    return {
        'success': True,
        'result': '工作流测试结果'
    } 