from flask import Blueprint, request, jsonify
from models import db
from models.workflow import Workflow
from services.workflow_service import (
    get_workflow_detail, create_workflow, update_workflow, 
    delete_workflow, execute_workflow, test_workflow
)

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
    workflow_detail = get_workflow_detail(workflow_id)
    return jsonify(workflow_detail)

@workflow_bp.route('/', methods=['POST'])
def create_workflow_route():
    data = request.json
    workflow = create_workflow(data)
    return jsonify(workflow.to_dict()), 201

@workflow_bp.route('/<int:workflow_id>', methods=['PUT'])
def update_workflow_route(workflow_id):
    data = request.json
    workflow = update_workflow(workflow_id, data)
    return jsonify(workflow.to_dict())

@workflow_bp.route('/<int:workflow_id>', methods=['DELETE'])
def delete_workflow_route(workflow_id):
    delete_workflow(workflow_id)
    return '', 204

@workflow_bp.route('/<int:workflow_id>/test', methods=['POST'])
def test_workflow_endpoint(workflow_id):
    input_data = request.json
    
    try:
        result = test_workflow(workflow_id, input_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@workflow_bp.route('/<int:workflow_id>/execute', methods=['POST'])
def execute_workflow_endpoint(workflow_id):
    input_data = request.json
    
    try:
        result = execute_workflow(workflow_id, input_data)
        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@workflow_bp.route('/<int:workflow_id>/publish', methods=['POST'])
def publish_workflow(workflow_id):
    workflow = Workflow.query.get_or_404(workflow_id)
    workflow.status = 'published'
    
    # 更新版本号
    version_parts = workflow.version.split('.')
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    workflow.version = '.'.join(version_parts)
    
    db.session.commit()
    
    return jsonify(workflow.to_dict())


