from flask import Blueprint, request, jsonify
from models import db
from models.workflow import Workflow
from services.workflow_service import test_workflow

workflow_bp = Blueprint('workflow', __name__)

@workflow_bp.route('/', methods=['GET'])
def list_workflows():
    agent_id = request.args.get('agent_id', type=int)
    
    query = Workflow.query
    
    if agent_id:
        query = query.filter_by(agent_id=agent_id)
    
    workflows = query.all()
    return jsonify([w.to_dict() for w in workflows])

@workflow_bp.route('/<int:workflow_id>', methods=['GET'])
def get_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    return jsonify(workflow.to_dict())

@workflow_bp.route('/', methods=['POST'])
def create_workflow():
    data = request.json
    workflow = Workflow(
        name=data.get('name'),
        description=data.get('description'),
        agent_id=data.get('agent_id')
    )
    
    if 'nodes' in data:
        workflow.nodes_obj = data['nodes']
    
    if 'edges' in data:
        workflow.edges_obj = data['edges']
    
    db.session.add(workflow)
    db.session.commit()
    
    return jsonify(workflow.to_dict()), 201

@workflow_bp.route('/<int:workflow_id>', methods=['PUT'])
def update_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    data = request.json
    
    if 'name' in data:
        workflow.name = data['name']
    
    if 'description' in data:
        workflow.description = data['description']
    
    if 'agent_id' in data:
        workflow.agent_id = data['agent_id']
    
    if 'nodes' in data:
        workflow.nodes_obj = data['nodes']
    
    if 'edges' in data:
        workflow.edges_obj = data['edges']
    
    db.session.commit()
    
    return jsonify(workflow.to_dict())

@workflow_bp.route('/<int:workflow_id>', methods=['DELETE'])
def delete_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    db.session.delete(workflow)
    db.session.commit()
    
    return '', 204

@workflow_bp.route('/<int:workflow_id>/test', methods=['POST'])
def test_workflow_endpoint(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    input_data = request.json
    
    try:
        result = test_workflow(workflow_id, input_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


