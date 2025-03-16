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
        # 创建所有表
        db.create_all()
        
        # 删除所有表数据
        db.session.query(Component).delete()
        db.session.query(Workflow).delete()
        db.session.commit()
        print("数据库表数据已清除并重新创建")

# 创建通用LPI组件
def create_common_lpis(app):
    with app.app_context():
        common_lpis = {
            'user_interaction': {
                'name': '用户介入LPI',
                'description': '需要用户介入处理的操作',
                'english_description': 'Operations that require user intervention',
                'category': 'user_interaction'
            },
            'async_wait': {
                'name': '异步等待LPI',
                'description': '等待异步操作完成',
                'english_description': 'Wait for asynchronous operation to complete',
                'category': 'async_wait'
            },
            'memory_query': {
                'name': '记忆查询LPI',
                'description': '查询系统记忆中的数据',
                'english_description': 'Query data from system memory',
                'category': 'memory_query'
            },
            'memory_modify': {
                'name': '记忆修改LPI',
                'description': '修改系统记忆中的数据',
                'english_description': 'Modify data in system memory',
                'category': 'memory_modify'
            },
            'conditional_jump': {
                'name': '条件跳转LPI',
                'description': '根据条件跳转到不同的执行路径',
                'english_description': 'Jump to different execution paths based on conditions',
                'category': 'conditional_jump'
            },
            'unconditional_jump': {
                'name': '无条件跳转LPI',
                'description': '无条件跳转到指定的执行路径',
                'english_description': 'Jump to specified execution path unconditionally',
                'category': 'unconditional_jump'
            },
            # 添加业务LPI组件
            'fault_diagnosis_lpi': {
                'name': '故障诊断LPI',
                'description': '诊断系统故障的原因和位置',
                'english_description': 'Diagnose system fault reasons and locations',
                'category': 'business'
            },
            'diagnosis_summary_lpi': {
                'name': '诊断总结LPI',
                'description': '总结故障诊断过程和结果',
                'english_description': 'Summarize the fault diagnosis process and results',
                'category': 'business'
            },
            'recovery_simulation_lpi': {
                'name': '恢复方案仿真LPI',
                'description': '仿真恢复方案的效果',
                'english_description': 'Simulate the effectiveness of the recovery plan',
                'category': 'business'
            },
            'recovery_plan_lpi': {
                'name': '恢复方案LPI',
                'description': '制定恢复方案',
                'english_description': 'Develop a recovery plan',
                'category': 'business'
            },
            'recovery_execution_lpi': {
                'name': '恢复执行LPI',
                'description': '执行恢复方案',
                'english_description': 'Execute the recovery plan',
                'category': 'business'
            },
            'repair_plan_lpi': {
                'name': '修复方案LPI',
                'description': '制定修复方案',
                'english_description': 'Develop a repair plan',
                'category': 'business'
            },
            'repair_simulation_lpi': {
                'name': '修复仿真LPI',
                'description': '仿真修复方案的效果',
                'english_description': 'Simulate the effectiveness of the repair plan',
                'category': 'business'
            },
            'repair_execution_lpi': {
                'name': '修复执行LPI',
                'description': '执行修复方案',
                'english_description': 'Execute the repair plan',
                'category': 'business'
            },
            'fault_verification_lpi': {
                'name': '故障验证LPI',
                'description': '验证故障是否修复成功',
                'english_description': 'Verify if the fault is repaired successfully',
                'category': 'business'
            },
            'fault_summary_lpi': {
                'name': '故障总结LPI',
                'description': '总结故障处理过程和经验',
                'english_description': 'Summarize the fault handling process and experience',
                'category': 'business'
            }
        }
        
        created_lpis = {}
        for key, lpi_data in common_lpis.items():
            existing = Component.query.filter_by(name=lpi_data['name']).first()
            if existing:
                print(f"{lpi_data['name']}已存在，跳过创建")
                created_lpis[key] = existing
                continue
                
            lpi = Component(
                name=lpi_data['name'],
                description=lpi_data['description'],
                english_description=lpi_data['english_description'],
                component_type='lpi',
                category=lpi_data['category']
            )
            db.session.add(lpi)
            db.session.commit()
            print(f"创建通用LPI组件: {lpi.name}")
            created_lpis[key] = lpi
            
        return created_lpis

# 创建专家Agent组件
def create_expert_agents(app, common_lpis):
    with app.app_context():
        # 重新查询common_lpis组件
        async_wait_lpi = Component.query.filter_by(name='异步等待LPI').first()
        user_interaction_lpi = Component.query.filter_by(name='用户介入LPI').first()
        conditional_jump_lpi = Component.query.filter_by(name='条件跳转LPI').first()
        
        expert_agents = {
            'fault_diagnosis': {
                'name': '故障诊断专家',
                'description': '诊断系统故障的原因和位置',
                'english_description': 'Diagnose system fault reasons and locations',
                'workflow_nodes': [
                    {
                        'id': 'start',
                        'type': 'start',
                        'position': {'x': 250, 'y': 50},
                        'data': {'name': '开始'}
                    },
                    {
                        'id': 'diagnosis',
                        'type': 'lpi',
                        'position': {'x': 250, 'y': 150},
                        'data': {
                            'name': '故障诊断',
                            'component_id': None  # 将在后面设置
                        }
                    },
                    {
                        'id': 'async_wait',
                        'type': 'lpi',
                        'position': {'x': 250, 'y': 250},
                        'data': {
                            'name': '等待诊断完成',
                            'component_id': async_wait_lpi.id if async_wait_lpi else None
                        }
                    },
                    {
                        'id': 'diagnosis_report',
                        'type': 'lpi',
                        'position': {'x': 250, 'y': 350},
                        'data': {
                            'name': '诊断报告',
                            'component_id': None  # 将在后面设置
                        }
                    },
                    {
                        'id': 'user_confirm',
                        'type': 'lpi',
                        'position': {'x': 250, 'y': 450},
                        'data': {
                            'name': '用户确认',
                            'component_id': user_interaction_lpi.id if user_interaction_lpi else None
                        }
                    },
                    {
                        'id': 'condition',
                        'type': 'lpi',
                        'position': {'x': 250, 'y': 550},
                        'data': {
                            'name': '判断确认结果',
                            'component_id': conditional_jump_lpi.id if conditional_jump_lpi else None
                        }
                    },
                    {
                        'id': 'end',
                        'type': 'end',
                        'position': {'x': 250, 'y': 650},
                        'data': {'name': '结束'}
                    }
                ],
                'workflow_edges': [
                    {'id': 'e1', 'source': 'start', 'target': 'diagnosis'},
                    {'id': 'e2', 'source': 'diagnosis', 'target': 'async_wait'},
                    {'id': 'e3', 'source': 'async_wait', 'target': 'diagnosis_report'},
                    {'id': 'e4', 'source': 'diagnosis_report', 'target': 'user_confirm'},
                    {'id': 'e5', 'source': 'user_confirm', 'target': 'condition'},
                    {'id': 'e6', 'source': 'condition', 'target': 'end'}
                ]
            },
            'fault_repair': {
                'name': '故障修复专家',
                'description': '执行故障修复操作',
                'english_description': 'Execute fault repair operations'
            },
            'business_recovery': {
                'name': '业务恢复专家',
                'description': '执行业务恢复操作',
                'english_description': 'Execute business recovery operations'
            },
            'repair_verification': {
                'name': '修复验证专家',
                'description': '验证故障是否修复成功',
                'english_description': 'Verify if the fault is repaired successfully'
            },
            'fault_summary': {
                'name': '故障总结专家',
                'description': '总结故障处理过程和经验',
                'english_description': 'Summarize fault handling process and experience'
            }
        }
        
        created_agents = {}
        for key, agent_data in expert_agents.items():
            existing = Component.query.filter_by(name=agent_data['name']).first()
            if existing:
                print(f"{agent_data['name']}已存在，跳过创建")
                created_agents[key] = existing
                continue
                
            agent = Component(
                name=agent_data['name'],
                description=agent_data['description'],
                english_description=agent_data['english_description'],
                component_type='agent',
                category='expert',
                agent_type='expert'
            )
            db.session.add(agent)
            db.session.commit()
            print(f"创建专家Agent组件: {agent.name}")
            
            # 创建工作流
            if 'workflow_nodes' in agent_data:
                workflow = Workflow(
                    name=f"{agent.name}工作流",
                    description=f"{agent.name}的标准工作流程",
                    agent_id=agent.id,
                    status='published',
                    version='1.0.0'
                )
                
                workflow.nodes_obj = agent_data['workflow_nodes']
                workflow.edges_obj = agent_data['workflow_edges']
                
                db.session.add(workflow)
                db.session.commit()
                print(f"创建工作流: {workflow.name}")
            
            created_agents[key] = agent
            
        return created_agents

# 创建场景Agent组件
def create_scenario_agents(app, expert_agents):
    with app.app_context():
        # 重新查询expert_agents组件以确保它们仍然绑定到当前会话
        expert_agents = {
            'fault_diagnosis': Component.query.filter_by(name='故障诊断专家').first(),
            'fault_repair': Component.query.filter_by(name='故障修复专家').first(),
            'business_recovery': Component.query.filter_by(name='业务恢复专家').first(),
            'repair_verification': Component.query.filter_by(name='修复验证专家').first(),
            'fault_summary': Component.query.filter_by(name='故障总结专家').first()
        }

        scenario_agents = {
            'fault_handling': {
                'name': '故障处理闭环',
                'description': '完整的故障处理流程，包括诊断、修复、恢复、验证和总结',
                'english_description': 'Complete fault handling process including diagnosis, repair, recovery, verification and summary',
                'workflow_nodes': [
                    {
                        'id': 'start',
                        'type': 'start',
                        'position': {'x': 250, 'y': 50},
                        'data': {'name': '开始'}
                    },
                    {
                        'id': 'diagnosis',
                        'type': 'agent',
                        'position': {'x': 250, 'y': 150},
                        'data': {
                            'name': '故障诊断',
                            'component_id': expert_agents['fault_diagnosis'].id
                        }
                    },
                    {
                        'id': 'repair',
                        'type': 'agent',
                        'position': {'x': 100, 'y': 250},
                        'data': {
                            'name': '故障修复',
                            'component_id': expert_agents['fault_repair'].id
                        }
                    },
                    {
                        'id': 'recovery',
                        'type': 'agent',
                        'position': {'x': 400, 'y': 250},
                        'data': {
                            'name': '业务恢复',
                            'component_id': expert_agents['business_recovery'].id
                        }
                    },
                    {
                        'id': 'verification',
                        'type': 'agent',
                        'position': {'x': 250, 'y': 350},
                        'data': {
                            'name': '修复验证',
                            'component_id': expert_agents['repair_verification'].id
                        }
                    },
                    {
                        'id': 'summary',
                        'type': 'agent',
                        'position': {'x': 250, 'y': 450},
                        'data': {
                            'name': '故障总结',
                            'component_id': expert_agents['fault_summary'].id
                        }
                    },
                    {
                        'id': 'end',
                        'type': 'end',
                        'position': {'x': 250, 'y': 550},
                        'data': {'name': '结束'}
                    }
                ],
                'workflow_edges': [
                    {'id': 'e1', 'source': 'start', 'target': 'diagnosis'},
                    {'id': 'e2', 'source': 'diagnosis', 'target': 'repair'},
                    {'id': 'e3', 'source': 'diagnosis', 'target': 'recovery'},
                    {'id': 'e4', 'source': 'repair', 'target': 'verification'},
                    {'id': 'e5', 'source': 'recovery', 'target': 'verification'},
                    {'id': 'e6', 'source': 'verification', 'target': 'summary'},
                    {'id': 'e7', 'source': 'summary', 'target': 'end'}
                ]
            }
        }
        
        created_agents = {}
        for key, agent_data in scenario_agents.items():
            existing = Component.query.filter_by(name=agent_data['name']).first()
            if existing:
                print(f"{agent_data['name']}已存在，跳过创建")
                created_agents[key] = existing
                continue
                
            agent = Component(
                name=agent_data['name'],
                description=agent_data['description'],
                english_description=agent_data['english_description'],
                component_type='agent',
                category='scenario',
                agent_type='scenario'
            )
            db.session.add(agent)
            db.session.commit()
            print(f"创建场景Agent组件: {agent.name}")
            
            # 创建工作流
            if 'workflow_nodes' in agent_data:
                workflow = Workflow(
                    name=f"{agent.name}工作流",
                    description=f"{agent.name}的标准工作流程",
                    agent_id=agent.id,
                    status='published',
                    version='1.0.0'
                )
                
                workflow.nodes_obj = agent_data['workflow_nodes']
                workflow.edges_obj = agent_data['workflow_edges']
                
                db.session.add(workflow)
                db.session.commit()
                print(f"创建工作流: {workflow.name}")
            
            created_agents[key] = agent
            
        return created_agents

def main():
    app = create_app()
    
    # 确保数据库文件存在
    db_path = os.path.join(current_dir, 'agent_designer.db')
    if os.path.exists(db_path):
        print(f"数据库文件已存在: {db_path}")
    
    init_db(app)
    
    # 创建通用LPI组件
    common_lpis = create_common_lpis(app)
    
    # 创建专家Agent组件
    expert_agents = create_expert_agents(app, common_lpis)
    
    # 创建场景Agent组件
    scenario_agents = create_scenario_agents(app, expert_agents)
    
    print("初始化数据完成")
    print(f"数据库文件路径: {db_path}")

if __name__ == '__main__':
    main()