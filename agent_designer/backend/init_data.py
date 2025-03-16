import os
import sys
import json
from datetime import datetime

# 添加项目根目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

from flask import Flask
from config import Config
from models import db
from models.component import Component
from models.workflow import Workflow

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    return app

def init_db(app):
    with app.app_context():
        db.create_all()
        print("数据库表创建完成")

def create_fault_diagnosis_lpi(app):
    with app.app_context():
        # 检查是否已存在
        existing = Component.query.filter_by(name='故障诊断API').first()
        if existing:
            print("故障诊断API已存在，跳过创建")
            return existing

        lpi = Component(
            name='故障诊断API',
            description='根据故障现象和业务对象，诊断故障原因、位置，并提供修复和恢复建议',
            english_description='Diagnose fault reason and location based on fault phenomenon and business object, and provide repair and recovery suggestions',
            component_type='lpi',
            category='故障处理'
        )
        
        content = {
            'api_type': 'rest',
            'endpoint': 'http://localhost:8000/fault-diagnosis',
            'method': 'POST',
            'input_params': [
                {
                    'name': 'fault_phenomenon',
                    'type': 'string',
                    'description': '故障现象描述',
                    'required': True
                },
                {
                    'name': 'business_object',
                    'type': 'string',
                    'description': '发生故障的业务对象',
                    'required': True
                }
            ],
            'output_params': [
                {
                    'name': 'fault_reason',
                    'type': 'string',
                    'description': '故障原因'
                },
                {
                    'name': 'fault_location',
                    'type': 'string',
                    'description': '故障位置'
                },
                {
                    'name': 'repair_suggestion',
                    'type': 'string',
                    'description': '修复建议'
                },
                {
                    'name': 'recovery_suggestion',
                    'type': 'string',
                    'description': '恢复建议'
                }
            ],
            'examples': [
                {
                    'input': {
                        'fault_phenomenon': '数据库连接超时',
                        'business_object': '订单系统'
                    },
                    'output': {
                        'fault_reason': '数据库连接超时',
                        'fault_location': '数据库服务器192.168.1.100',
                        'repair_suggestion': '重启数据库服务或检查网络连接',
                        'recovery_suggestion': '启用备用数据库服务器'
                    }
                }
            ]
        }
        
        lpi.content_obj = content
        db.session.add(lpi)
        db.session.commit()
        print(f"创建LPI组件: {lpi.name}")
        return lpi

def create_business_recovery_lpi(app):
    with app.app_context():
        # 检查是否已存在
        existing = Component.query.filter_by(name='业务恢复API').first()
        if existing:
            print("业务恢复API已存在，跳过创建")
            return existing

        lpi = Component(
            name='业务恢复API',
            description='根据故障原因、位置和恢复建议，执行业务恢复操作',
            english_description='Execute business recovery operations based on fault reason, location and recovery suggestions',
            component_type='lpi',
            category='故障处理'
        )
        
        content = {
            'api_type': 'rest',
            'endpoint': 'http://localhost:8000/business-recovery',
            'method': 'POST',
            'input_params': [
                {
                    'name': 'fault_reason',
                    'type': 'string',
                    'description': '故障原因',
                    'required': True
                },
                {
                    'name': 'fault_location',
                    'type': 'string',
                    'description': '故障位置',
                    'required': True
                },
                {
                    'name': 'recovery_suggestion',
                    'type': 'string',
                    'description': '恢复建议',
                    'required': True
                }
            ],
            'output_params': [
                {
                    'name': 'recovery_plan',
                    'type': 'string',
                    'description': '恢复方案'
                },
                {
                    'name': 'business_recovery_result',
                    'type': 'string',
                    'description': '业务恢复结果'
                }
            ],
            'examples': [
                {
                    'input': {
                        'fault_reason': '数据库连接超时',
                        'fault_location': '数据库服务器192.168.1.100',
                        'recovery_suggestion': '启用备用数据库服务器'
                    },
                    'output': {
                        'recovery_plan': '启用备用数据库服务器192.168.1.101，并切换业务连接',
                        'business_recovery_result': '业务已成功切换到备用数据库，服务恢复正常'
                    }
                }
            ]
        }
        
        lpi.content_obj = content
        db.session.add(lpi)
        db.session.commit()
        print(f"创建LPI组件: {lpi.name}")
        return lpi

def create_fault_repair_lpi(app):
    with app.app_context():
        # 检查是否已存在
        existing = Component.query.filter_by(name='故障修复API').first()
        if existing:
            print("故障修复API已存在，跳过创建")
            return existing

        lpi = Component(
            name='故障修复API',
            description='根据故障原因、位置和修复建议，执行故障修复操作',
            english_description='Execute fault repair operations based on fault reason, location and repair suggestions',
            component_type='lpi',
            category='故障处理'
        )
        
        content = {
            'api_type': 'rest',
            'endpoint': 'http://localhost:8000/fault-repair',
            'method': 'POST',
            'input_params': [
                {
                    'name': 'fault_reason',
                    'type': 'string',
                    'description': '故障原因',
                    'required': True
                },
                {
                    'name': 'fault_location',
                    'type': 'string',
                    'description': '故障位置',
                    'required': True
                },
                {
                    'name': 'repair_suggestion',
                    'type': 'string',
                    'description': '修复建议',
                    'required': True
                }
            ],
            'output_params': [
                {
                    'name': 'repair_plan',
                    'type': 'string',
                    'description': '修复方案'
                },
                {
                    'name': 'repair_result',
                    'type': 'string',
                    'description': '修复结果'
                }
            ],
            'examples': [
                {
                    'input': {
                        'fault_reason': '数据库连接超时',
                        'fault_location': '数据库服务器192.168.1.100',
                        'repair_suggestion': '重启数据库服务或检查网络连接'
                    },
                    'output': {
                        'repair_plan': '重启数据库服务并检查网络连接状态',
                        'repair_result': '数据库服务已重启，网络连接恢复正常'
                    }
                }
            ]
        }
        
        lpi.content_obj = content
        db.session.add(lpi)
        db.session.commit()
        print(f"创建LPI组件: {lpi.name}")
        return lpi

def create_repair_verification_lpi(app):
    with app.app_context():
        # 检查是否已存在
        existing = Component.query.filter_by(name='修复验证API').first()
        if existing:
            print("修复验证API已存在，跳过创建")
            return existing

        lpi = Component(
            name='修复验证API',
            description='根据修复结果，验证故障是否已修复',
            english_description='Verify if the fault has been repaired based on repair result',
            component_type='lpi',
            category='故障处理'
        )
        
        content = {
            'api_type': 'rest',
            'endpoint': 'http://localhost:8000/repair-verification',
            'method': 'POST',
            'input_params': [
                {
                    'name': 'repair_result',
                    'type': 'string',
                    'description': '修复结果',
                    'required': True
                }
            ],
            'output_params': [
                {
                    'name': 'verification_result',
                    'type': 'string',
                    'description': '验证结果'
                }
            ],
            'examples': [
                {
                    'input': {
                        'repair_result': '数据库服务已重启，网络连接恢复正常'
                    },
                    'output': {
                        'verification_result': '验证通过，数据库服务运行正常，连接稳定'
                    }
                }
            ]
        }
        
        lpi.content_obj = content
        db.session.add(lpi)
        db.session.commit()
        print(f"创建LPI组件: {lpi.name}")
        return lpi

def create_fault_summary_lpi(app):
    with app.app_context():
        # 检查是否已存在
        existing = Component.query.filter_by(name='故障总结API').first()
        if existing:
            print("故障总结API已存在，跳过创建")
            return existing

        lpi = Component(
            name='故障总结API',
            description='根据故障处理的历史记录，生成故障总结',
            english_description='Generate fault summary based on fault handling history records',
            component_type='lpi',
            category='故障处理'
        )
        
        content = {
            'api_type': 'rest',
            'endpoint': 'http://localhost:8000/fault-summary',
            'method': 'POST',
            'input_params': [
                {
                    'name': 'history_records',
                    'type': 'array',
                    'description': '故障处理历史记录',
                    'required': True
                }
            ],
            'output_params': [
                {
                    'name': 'fault_summary',
                    'type': 'string',
                    'description': '故障总结'
                }
            ],
            'examples': [
                {
                    'input': {
                        'history_records': [
                            {
                                'step': '故障诊断',
                                'input': {
                                    'fault_phenomenon': '数据库连接超时',
                                    'business_object': '订单系统'
                                },
                                'output': {
                                    'fault_reason': '数据库连接超时',
                                    'fault_location': '数据库服务器192.168.1.100',
                                    'repair_suggestion': '重启数据库服务或检查网络连接',
                                    'recovery_suggestion': '启用备用数据库服务器'
                                }
                            },
                            {
                                'step': '业务恢复',
                                'input': {
                                    'fault_reason': '数据库连接超时',
                                    'fault_location': '数据库服务器192.168.1.100',
                                    'recovery_suggestion': '启用备用数据库服务器'
                                },
                                'output': {
                                    'recovery_plan': '启用备用数据库服务器192.168.1.101，并切换业务连接',
                                    'business_recovery_result': '业务已成功切换到备用数据库，服务恢复正常'
                                }
                            },
                            {
                                'step': '故障修复',
                                'input': {
                                    'fault_reason': '数据库连接超时',
                                    'fault_location': '数据库服务器192.168.1.100',
                                    'repair_suggestion': '重启数据库服务或检查网络连接'
                                },
                                'output': {
                                    'repair_plan': '重启数据库服务并检查网络连接状态',
                                    'repair_result': '数据库服务已重启，网络连接恢复正常'
                                }
                            },
                            {
                                'step': '修复验证',
                                'input': {
                                    'repair_result': '数据库服务已重启，网络连接恢复正常'
                                },
                                'output': {
                                    'verification_result': '验证通过，数据库服务运行正常，连接稳定'
                                }
                            }
                        ]
                    },
                    'output': {
                        'fault_summary': '本次故障为数据库连接超时，通过重启数据库服务解决。期间通过备用数据库保证了业务连续性。建议加强数据库监控，提前发现连接异常。'
                    }
                }
            ]
        }
        
        lpi.content_obj = content
        db.session.add(lpi)
        db.session.commit()
        print(f"创建LPI组件: {lpi.name}")
        return lpi

def create_fault_handling_agent(app, lpi_components):
    with app.app_context():
        # 检查是否已存在
        existing = Component.query.filter_by(name='故障处理Agent').first()
        if existing:
            print("故障处理Agent已存在，跳过创建")
            return existing

        agent = Component(
            name='故障处理Agent',
            description='自动化故障处理流程，包括故障诊断、业务恢复、故障修复、修复验证和故障总结',
            english_description='Automated fault handling process, including fault diagnosis, business recovery, fault repair, repair verification and fault summary',
            component_type='agent',
            category='故障处理'
        )
        
        content = {
            'input_params': [
                {
                    'name': 'fault_phenomenon',
                    'type': 'string',
                    'description': '故障现象描述',
                    'required': True
                },
                {
                    'name': 'business_object',
                    'type': 'string',
                    'description': '发生故障的业务对象',
                    'required': True
                }
            ],
            'output_params': [
                {
                    'name': 'fault_summary',
                    'type': 'string',
                    'description': '故障总结'
                },
                {
                    'name': 'history_records',
                    'type': 'array',
                    'description': '故障处理历史记录'
                }
            ],
            'examples': [
                {
                    'input': {
                        'fault_phenomenon': '数据库连接超时',
                        'business_object': '订单系统'
                    },
                    'output': {
                        'fault_summary': '本次故障为数据库连接超时，通过重启数据库服务解决。期间通过备用数据库保证了业务连续性。建议加强数据库监控，提前发现连接异常。',
                        'history_records': [
                            {
                                'step': '故障诊断',
                                'input': {
                                    'fault_phenomenon': '数据库连接超时',
                                    'business_object': '订单系统'
                                },
                                'output': {
                                    'fault_reason': '数据库连接超时',
                                    'fault_location': '数据库服务器192.168.1.100',
                                    'repair_suggestion': '重启数据库服务或检查网络连接',
                                    'recovery_suggestion': '启用备用数据库服务器'
                                }
                            },
                            {
                                'step': '业务恢复',
                                'input': {
                                    'fault_reason': '数据库连接超时',
                                    'fault_location': '数据库服务器192.168.1.100',
                                    'recovery_suggestion': '启用备用数据库服务器'
                                },
                                'output': {
                                    'recovery_plan': '启用备用数据库服务器192.168.1.101，并切换业务连接',
                                    'business_recovery_result': '业务已成功切换到备用数据库，服务恢复正常'
                                }
                            },
                            {
                                'step': '故障修复',
                                'input': {
                                    'fault_reason': '数据库连接超时',
                                    'fault_location': '数据库服务器192.168.1.100',
                                    'repair_suggestion': '重启数据库服务或检查网络连接'
                                },
                                'output': {
                                    'repair_plan': '重启数据库服务并检查网络连接状态',
                                    'repair_result': '数据库服务已重启，网络连接恢复正常'
                                }
                            },
                            {
                                'step': '修复验证',
                                'input': {
                                    'repair_result': '数据库服务已重启，网络连接恢复正常'
                                },
                                'output': {
                                    'verification_result': '验证通过，数据库服务运行正常，连接稳定'
                                }
                            },
                            {
                                'step': '故障总结',
                                'input': {
                                    'history_records': '...'
                                },
                                'output': {
                                    'fault_summary': '本次故障为数据库连接超时，通过重启数据库服务解决。期间通过备用数据库保证了业务连续性。建议加强数据库监控，提前发现连接异常。'
                                }
                            }
                        ]
                    }
                }
            ]
        }
        
        agent.content_obj = content
        db.session.add(agent)
        db.session.commit()
        print(f"创建Agent组件: {agent.name}")
        
        # 创建工作流
        create_fault_handling_workflow(app, agent, lpi_components)
        
        return agent

def create_fault_handling_workflow(app, agent, lpi_components):
    with app.app_context():
        # 检查是否已存在
        existing = Workflow.query.filter_by(agent_id=agent.id).first()
        if existing:
            print("故障处理工作流已存在，跳过创建")
            return existing

        workflow = Workflow(
            name='故障处理工作流',
            description='自动化故障处理流程工作流',
            agent_id=agent.id,
            status='published',
            version='1.0.0'
        )
        
        # 创建节点
        nodes = [
            {
                'id': 'start_node',
                'type': 'start',
                'position': {'x': 250, 'y': 50},
                'data': {'name': '开始'}
            },
            {
                'id': 'diagnosis_node',
                'type': 'lpi',
                'position': {'x': 250, 'y': 150},
                'data': {
                    'name': '故障诊断',
                    'component_id': lpi_components['故障诊断API'].id
                }
            },
            {
                'id': 'recovery_node',
                'type': 'lpi',
                'position': {'x': 100, 'y': 250},
                'data': {
                    'name': '业务恢复',
                    'component_id': lpi_components['业务恢复API'].id
                }
            },
            {
                'id': 'repair_node',
                'type': 'lpi',
                'position': {'x': 400, 'y': 250},
                'data': {
                    'name': '故障修复',
                    'component_id': lpi_components['故障修复API'].id
                }
            },
            {
                'id': 'verification_node',
                'type': 'lpi',
                'position': {'x': 400, 'y': 350},
                'data': {
                    'name': '修复验证',
                    'component_id': lpi_components['修复验证API'].id
                }
            },
            {
                'id': 'summary_node',
                'type': 'lpi',
                'position': {'x': 250, 'y': 450},
                'data': {
                    'name': '故障总结',
                    'component_id': lpi_components['故障总结API'].id
                }
            },
            {
                'id': 'end_node',
                'type': 'end',
                'position': {'x': 250, 'y': 550},
                'data': {'name': '结束'}
            }
        ]
        
        # 创建边
        edges = [
            {
                'id': 'edge_start_diagnosis',
                'source': 'start_node',
                'target': 'diagnosis_node'
            },
            {
                'id': 'edge_diagnosis_recovery',
                'source': 'diagnosis_node',
                'target': 'recovery_node'
            },
            {
                'id': 'edge_diagnosis_repair',
                'source': 'diagnosis_node',
                'target': 'repair_node'
            },
            {
                'id': 'edge_repair_verification',
                'source': 'repair_node',
                'target': 'verification_node'
            },
            {
                'id': 'edge_recovery_summary',
                'source': 'recovery_node',
                'target': 'summary_node'
            },
            {
                'id': 'edge_verification_summary',
                'source': 'verification_node',
                'target': 'summary_node'
            },
            {
                'id': 'edge_summary_end',
                'source': 'summary_node',
                'target': 'end_node'
            }
        ]
        
        workflow.nodes_obj = nodes
        workflow.edges_obj = edges
        
        db.session.add(workflow)
        db.session.commit()
        print(f"创建工作流: {workflow.name}")
        return workflow

def main():
    app = create_app()
    
    # 确保数据库文件存在
    db_path = os.path.join(current_dir, 'agent_designer.db')
    if os.path.exists(db_path):
        print(f"数据库文件已存在: {db_path}")
    
    init_db(app)
    
    # 创建LPI组件
    lpi_components = {}
    lpi_components['故障诊断API'] = create_fault_diagnosis_lpi(app)
    lpi_components['业务恢复API'] = create_business_recovery_lpi(app)
    lpi_components['故障修复API'] = create_fault_repair_lpi(app)
    lpi_components['修复验证API'] = create_repair_verification_lpi(app)
    lpi_components['故障总结API'] = create_fault_summary_lpi(app)
    
    # 创建Agent组件
    create_fault_handling_agent(app, lpi_components)
    
    print("初始化数据完成")
    print(f"数据库文件路径: {db_path}")

if __name__ == '__main__':
    main() 