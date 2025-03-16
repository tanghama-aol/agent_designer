from models.component import Component
from models import db
import json

def get_component_tree():
    components = Component.query.all()
    tree = []
    
    # 组织组件树结构
    lpi_general_components = []
    lpi_business_components = []
    agent_expert_components = []
    agent_scenario_components = []
    common_components = []
    
    for comp in components:
        node = {
            'title': comp.name,
            'key': f'{comp.component_type}-{comp.id}',
            'type': comp.component_type,
            'id': comp.id,
            'category': comp.category,  # 添加category字段
            'agent_type': comp.agent_type  # 添加agent_type字段
        }
        
        if comp.component_type == 'lpi':
            if comp.category in ['general', 'user_interaction', 'async_wait', 'memory_query', 'memory_modify', 'conditional_jump', 'unconditional_jump']:
                lpi_general_components.append(node)
            else:
                lpi_business_components.append(node)
        elif comp.component_type == 'agent':
            if comp.agent_type == 'expert':
                agent_expert_components.append(node)
            elif comp.agent_type == 'scenario':
                agent_scenario_components.append(node)
        else:
            common_components.append(node)
    
    if lpi_general_components:
        tree.append({
            'title': '通用LPI',
            'key': 'general_lpi',
            'children': lpi_general_components
        })
    
    if lpi_business_components:
        tree.append({
            'title': '业务LPI',
            'key': 'business_lpi',
            'children': lpi_business_components
        })
    
    if agent_expert_components:
        tree.append({
            'title': '专家Agent',
            'key': 'expert_agent',
            'children': agent_expert_components
        })
    
    if agent_scenario_components:
        tree.append({
            'title': '场景Agent',
            'key': 'scenario_agent',
            'children': agent_scenario_components
        })
    
    if common_components:
        tree.append({
            'title': '通用组件',
            'key': 'common',
            'children': common_components
        })
    
    return tree

def get_component_detail(component_id):
    component = Component.query.get_or_404(component_id)
    
    if component.component_type == 'lpi':
        return component.get_lpi_details()
    elif component.component_type == 'agent':
        return component.get_agent_details()
    else:
        return component.get_common_details()

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