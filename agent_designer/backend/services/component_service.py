from models.component import Component

def get_component_tree():
    components = Component.query.all()
    tree = []
    
    # 组织组件树结构
    lpi_components = []
    agent_components = []
    common_components = []
    
    for comp in components:
        node = {
            'title': comp.name,
            'key': f'{comp.component_type}-{comp.id}',
            'type': comp.component_type
        }
        
        if comp.component_type == 'lpi':
            lpi_components.append(node)
        elif comp.component_type == 'agent':
            agent_components.append(node)
        else:
            common_components.append(node)
    
    if lpi_components:
        tree.append({
            'title': 'LPI组件',
            'key': 'lpi',
            'children': lpi_components
        })
    
    if agent_components:
        tree.append({
            'title': 'Agent组件',
            'key': 'agent',
            'children': agent_components
        })
    
    if common_components:
        tree.append({
            'title': '通用组件',
            'key': 'common',
            'children': common_components
        })
    
    return tree

def get_component_detail(component_id):
    return Component.query.get_or_404(component_id) 