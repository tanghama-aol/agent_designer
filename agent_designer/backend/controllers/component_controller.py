from flask import Blueprint, request, jsonify
from models import db
from models.component import Component
from services.component_service import (
    get_component_tree, get_component_detail, 
    create_lpi, update_lpi, 
    create_agent, update_agent,
    create_common_component, update_common_component,
    delete_component, component_service
)

component_bp = Blueprint('component', __name__, url_prefix='/api/component')

@component_bp.route('/', methods=['GET'])
def list_components():
    component_type = request.args.get('type')
    category = request.args.get('category')
    
    query = Component.query
    
    if component_type:
        query = query.filter_by(component_type=component_type)
    
    if category:
        query = query.filter_by(category=category)
    
    components = query.all()
    return jsonify([c.to_dict() for c in components])

@component_bp.route('/tree', methods=['GET'])
def get_component_tree():
    """获取组件树"""
    tree = component_service.get_component_tree()
    return jsonify(tree)

@component_bp.route('/<component_type>/<component_id>', methods=['GET'])
def get_component_detail(component_type, component_id):
    """获取组件详情"""
    detail = component_service.get_component_detail(component_id, component_type)
    if detail:
        return jsonify(detail)
    return jsonify({'error': '未找到组件'}), 404

@component_bp.route('/lpi', methods=['POST'])
def create_lpi_component():
    data = request.json
    lpi = create_lpi(data)
    return jsonify(lpi.get_lpi_details()), 201

@component_bp.route('/lpi/<int:component_id>', methods=['PUT'])
def update_lpi_component(component_id):
    data = request.json
    lpi = update_lpi(component_id, data)
    return jsonify(lpi.get_lpi_details())

@component_bp.route('/agent', methods=['POST'])
def create_agent_component():
    data = request.json
    agent = create_agent(data)
    return jsonify(agent.get_agent_details()), 201

@component_bp.route('/agent/<int:component_id>', methods=['PUT'])
def update_agent_component(component_id):
    data = request.json
    agent = update_agent(component_id, data)
    return jsonify(agent.get_agent_details())

@component_bp.route('/common', methods=['POST'])
def create_common_component_route():
    data = request.json
    component = create_common_component(data)
    return jsonify(component.get_common_details()), 201

@component_bp.route('/common/<int:component_id>', methods=['PUT'])
def update_common_component_route(component_id):
    data = request.json
    component = update_common_component(component_id, data)
    return jsonify(component.get_common_details())

@component_bp.route('/<int:component_id>', methods=['DELETE'])
def delete_component_route(component_id):
    delete_component(component_id)
    return '', 204

@component_bp.route('/import', methods=['POST'])
def import_component():
    data = request.json
    component_type = data.get('component_type')
    
    if component_type == 'lpi':
        component = create_lpi(data)
    elif component_type == 'agent':
        component = create_agent(data)
    elif component_type == 'common':
        component = create_common_component(data)
    else:
        return jsonify({'error': '不支持的组件类型'}), 400
    
    return jsonify(component.to_dict()), 201

@component_bp.route('/<int:component_id>/export', methods=['GET'])
def export_component(component_id):
    component = Component.query.get_or_404(component_id)
    export_data = component.to_dict()
    
    # 如果是Agent，添加工作流信息
    if component.component_type == 'agent':
        export_data['workflows'] = [w.to_dict() for w in component.workflows]
    
    return jsonify(export_data)

@component_bp.route('/<component_type>/<component_id>', methods=['PUT'])
def update_component(component_type, component_id):
    """更新组件"""
    data = request.json
    success = component_service.update_component(component_id, component_type, data)
    if success:
        return jsonify({'message': '更新成功'})
    return jsonify({'error': '更新失败'}), 400

@component_bp.route('/workflow/<workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    """更新工作流"""
    data = request.json
    success = component_service.update_workflow(workflow_id, data)
    if success:
        return jsonify({'message': '更新成功'})
    return jsonify({'error': '更新失败'}), 400

@component_bp.route('/workflow', methods=['POST'])
def create_workflow():
    """创建工作流"""
    data = request.json
    workflow = component_service.create_workflow(data)
    if workflow:
        return jsonify(workflow)
    return jsonify({'error': '创建失败'}), 400 