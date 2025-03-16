from flask import Blueprint, request, jsonify
from models import db
from models.component import Component
from services.component_service import get_component_tree, get_component_detail

component_bp = Blueprint('component', __name__)

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
def get_tree():
    tree = get_component_tree()
    return jsonify(tree)

@component_bp.route('/<int:component_id>', methods=['GET'])
def get_component(component_id):
    component = Component.query.get_or_404(component_id)
    return jsonify(component.to_dict())

@component_bp.route('/', methods=['POST'])
def create_component():
    data = request.json
    component = Component(
        name=data.get('name'),
        description=data.get('description'),
        english_description=data.get('english_description'),
        component_type=data.get('component_type'),
        category=data.get('category')
    )
    
    if 'content' in data:
        component.content_obj = data['content']
    
    db.session.add(component)
    db.session.commit()
    
    return jsonify(component.to_dict()), 201

@component_bp.route('/<int:component_id>', methods=['PUT'])
def update_component(component_id):
    component = Component.query.get_or_404(component_id)
    data = request.json
    
    if 'name' in data:
        component.name = data['name']
    
    if 'description' in data:
        component.description = data['description']
    
    if 'english_description' in data:
        component.english_description = data['english_description']
    
    if 'component_type' in data:
        component.component_type = data['component_type']
    
    if 'category' in data:
        component.category = data['category']
    
    if 'content' in data:
        component.content_obj = data['content']
    
    db.session.commit()
    
    return jsonify(component.to_dict())

@component_bp.route('/<int:component_id>', methods=['DELETE'])
def delete_component(component_id):
    component = Component.query.get_or_404(component_id)
    db.session.delete(component)
    db.session.commit()
    
    return '', 204

@component_bp.route('/import', methods=['POST'])
def import_component():
    # 导入组件的逻辑
    return jsonify({'message': '组件导入成功'})

@component_bp.route('/<int:component_id>/export', methods=['GET'])
def export_component(component_id):
    # 导出组件的逻辑
    component = Component.query.get_or_404(component_id)
    return jsonify(component.to_dict()) 