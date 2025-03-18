import os
import re
import json
import uuid

# 根据文件结构自动寻找工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
md_file = os.path.join(root_dir, 'design', 'DiagnoseAgentWorkFlow.md')

# 输出目录
data_dir = os.path.join(current_dir, 'data')
agent_dir = os.path.join(data_dir, 'agent')
lpi_busi_dir = os.path.join(data_dir, 'lpi', 'busi')
lpi_common_dir = os.path.join(data_dir, 'lpi', 'common')

# 确保目录存在
for dir_path in [data_dir, agent_dir, lpi_busi_dir, lpi_common_dir]:
    os.makedirs(dir_path, exist_ok=True)

def generate_id():
    """生成唯一ID"""
    return str(uuid.uuid4())

def to_snake_case(name):
    """将名称转换为下划线形式的文件名
    例如: "故障诊断Agent" -> "fault_diagnosis_agent"
    """
    # 将中文转为拼音或英文名称(简单处理，实际项目中可能需要更复杂的转换)
    english_names = {
        '故障': 'fault',
        '诊断': 'diagnosis',
        '闭环': 'closed_loop',
        '场景': 'scenario',
        '工作流': 'workflow',
        '主流程': 'main_process',
        '示例': 'example',
        '方案': 'solution',
        '执行': 'execution',
        '仿真': 'simulation',
        '业务': 'business',
        '恢复': 'recovery',
        '修复': 'repair',
        '验证': 'verification',
        '总结': 'summary',
        '用户': 'user',
        '介入': 'intervention',
        '报告': 'report',
        '相似': 'similar',
        '案例': 'case',
        '下载': 'download',
        '生成': 'generate',
        '显示': 'display',
        '思维链': 'chain_of_thought',
        '智能': 'intelligent'
    }
    
    # 替换中文为英文
    for cn, en in english_names.items():
        name = name.replace(cn, en)
    
    # 转为小写并替换非字母数字为下划线
    name = name.lower()
    name = re.sub(r'[^a-z0-9]+', '_', name)
    
    # 移除前后的下划线
    name = name.strip('_')
    
    return name

def read_markdown_file(file_path):
    """读取Markdown文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_markdown(content):
    """解析Markdown内容并提取结构化数据"""
    lines = content.split('\n')
    
    # 找出所有的场景Agent、专家Agent和工作流
    scenario_agents = []
    expert_agents = []
    workflows = {}
    
    current_scenario = None
    current_expert = None
    current_phase = None
    
    for line in lines:
        line = line.strip()
        
        # 跳过空行
        if not line:
            continue
        
        # 解析一级标题 - 场景Agent
        if line.startswith('# '):
            scenario_name = line[2:].strip()
            scenario_id = generate_id()
            current_scenario = {
                'id': scenario_id,
                'name': scenario_name,
                'description': f"{scenario_name}场景",
                'type': 'scenario',
                'expert_agents': [],
                'filename': f"scenario_{to_snake_case(scenario_name)}"
            }
            scenario_agents.append(current_scenario)
        
        # 解析二级标题 - 专家Agent
        elif line.startswith('## '):
            if current_scenario is None:
                continue
                
            expert_name = line[3:].strip()
            expert_id = generate_id()
            current_expert = {
                'id': expert_id,
                'name': expert_name,
                'description': f"{expert_name}专家",
                'english_description': f"{expert_name} Expert Agent",
                'type': 'expert',
                'category': current_scenario['name'],
                'phases': [],
                'filename': f"expert_{to_snake_case(expert_name)}"
            }
            expert_agents.append(current_expert)
            current_scenario['expert_agents'].append(expert_id)
            
            # 初始化工作流
            workflow_name = f"{expert_name}工作流"
            workflow_id = generate_id()
            workflows[expert_id] = {
                'id': workflow_id,
                'name': workflow_name,
                'description': f"{expert_name}的执行流程",
                'agent_id': expert_id,
                'phases': [],
                'filename': f"workflow_{to_snake_case(workflow_name)}"
            }
        
        # 解析三级标题 - 工作流阶段
        elif line.startswith('### '):
            if current_expert is None:
                continue
                
            phase_name = line[4:].strip()
            phase_id = generate_id()
            phase_parts = phase_name.split('.')
            phase_title = phase_parts[1] if len(phase_parts) > 1 else phase_name
            
            current_phase = {
                'id': phase_id,
                'name': phase_title,
                'full_name': phase_name,
                'tasks': []
            }
            
            current_expert['phases'].append(phase_id)
            workflows[current_expert['id']]['phases'].append({
                'id': phase_id,
                'name': phase_title,
                'full_name': phase_name,
                'tasks': []
            })
        
        # 解析任务列表（数字编号的列表项）
        elif re.match(r'^\d+\.', line):
            if current_phase is None:
                continue
                
            # 提取任务描述
            task_match = re.match(r'^\d+\.\s+(.*)', line)
            if task_match:
                task_desc = task_match.group(1).strip()
                task_id = generate_id()
                
                # 创建LPI
                lpi = {
                    'id': task_id,
                    'name': task_desc,
                    'description': task_desc,
                    'english_description': task_desc,
                    'category': current_expert['name'] if current_expert else "通用",
                    'filename': f"busi_{to_snake_case(task_desc)}"
                }
                
                # 将任务添加到当前阶段
                for phase in workflows[current_expert['id']]['phases']:
                    if phase['full_name'] == current_phase['full_name']:
                        phase['tasks'].append({
                            'id': task_id,
                            'name': task_desc,
                            'type': 'lpi',
                            'filename': lpi['filename']
                        })
    
    return {
        'scenario_agents': scenario_agents,
        'expert_agents': expert_agents,
        'workflows': workflows
    }

def generate_lpi_files(data):
    """生成业务LPI和通用LPI JSON文件"""
    # 收集所有专家Agent中的任务
    busi_lpis = []
    
    for expert in data['expert_agents']:
        for workflow in data['workflows'].values():
            if workflow['agent_id'] == expert['id']:
                for phase in workflow['phases']:
                    for task in phase['tasks']:
                        # 创建业务LPI
                        lpi = {
                            'id': task['id'],
                            'name': task['name'],
                            'description': task['name'],
                            'english_description': task['name'],
                            'type': 'business',
                            'category': expert['name'],
                            'filename': task.get('filename', f"busi_{to_snake_case(task['name'])}")
                        }
                        busi_lpis.append(lpi)
    
    # 生成通用LPI
    common_lpis = [
        {
            'id': generate_id(),
            'name': '思维链分析',
            'description': '通过思维链分析问题',
            'english_description': 'Chain of Thought Analysis',
            'type': 'common',
            'category': '思维链',
            'filename': 'common_chain_of_thought_analysis'
        },
        {
            'id': generate_id(),
            'name': '用户交互',
            'description': '与用户进行交互',
            'english_description': 'User Interaction',
            'type': 'common',
            'category': '交互',
            'filename': 'common_user_interaction'
        },
        {
            'id': generate_id(),
            'name': '结果展示',
            'description': '展示结果信息',
            'english_description': 'Result Display',
            'type': 'common',
            'category': '展示',
            'filename': 'common_result_display'
        }
    ]
    
    # 写入业务LPI文件
    for lpi in busi_lpis:
        file_path = os.path.join(lpi_busi_dir, f"{lpi['filename']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(lpi, f, ensure_ascii=False, indent=2)
    
    # 写入通用LPI文件
    for lpi in common_lpis:
        file_path = os.path.join(lpi_common_dir, f"{lpi['filename']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(lpi, f, ensure_ascii=False, indent=2)
    
    print(f"生成了 {len(busi_lpis)} 个业务LPI和 {len(common_lpis)} 个通用LPI")

def generate_agent_files(data):
    """生成场景Agent和专家Agent JSON文件"""
    # 写入场景Agent文件
    for agent in data['scenario_agents']:
        file_path = os.path.join(agent_dir, f"{agent['filename']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(agent, f, ensure_ascii=False, indent=2)
    
    # 写入专家Agent文件
    for agent in data['expert_agents']:
        file_path = os.path.join(agent_dir, f"{agent['filename']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(agent, f, ensure_ascii=False, indent=2)
    
    print(f"生成了 {len(data['scenario_agents'])} 个场景Agent和 {len(data['expert_agents'])} 个专家Agent")

def generate_workflow_files(data):
    """生成工作流JSON文件"""
    for agent_id, workflow in data['workflows'].items():
        file_path = os.path.join(agent_dir, f"{workflow['filename']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, ensure_ascii=False, indent=2)
    
    print(f"生成了 {len(data['workflows'])} 个工作流")

def generate_reactflow_data(data):
    """生成ReactFlow格式的工作流数据"""
    for agent_id, workflow in data['workflows'].items():
        # 转换为ReactFlow格式
        rf_nodes = []
        rf_edges = []
        
        # 计算阶段节点的位置 - 横向排列
        phase_count = len(workflow['phases'])
        phase_spacing = 300  # 阶段节点之间的水平间距
        
        # 先添加开始节点
        start_node = {
            'id': 'start',
            'type': 'start',
            'position': {'x': 50, 'y': 50},
            'data': {'name': '开始'}
        }
        rf_nodes.append(start_node)
        
        for i, phase in enumerate(workflow['phases']):
            # 计算阶段节点的位置
            x_pos = 50 + (i + 1) * phase_spacing
            y_pos = 50
            
            # 创建阶段节点
            phase_node = {
                'id': f"phase_{phase['id']}",
                'type': 'phase',
                'position': {'x': x_pos, 'y': y_pos},
                'data': {'name': phase['name']}
            }
            rf_nodes.append(phase_node)
            
            # 连接前一个节点到当前阶段节点
            if i == 0:
                # 第一个阶段连接到开始节点
                rf_edges.append({
                    'id': f"edge_start_to_{phase['id']}",
                    'source': 'start',
                    'target': f"phase_{phase['id']}",
                    'type': 'smoothstep'
                })
            else:
                # 连接到前一个阶段
                prev_phase = workflow['phases'][i-1]
                rf_edges.append({
                    'id': f"edge_{prev_phase['id']}_to_{phase['id']}",
                    'source': f"phase_{prev_phase['id']}",
                    'target': f"phase_{phase['id']}",
                    'type': 'smoothstep'
                })
            
            # 计算任务节点的位置 - 纵向排列
            for j, task in enumerate(phase['tasks']):
                # 每个任务垂直偏移
                task_y_pos = y_pos + 100 + j * 80
                
                # 创建任务节点
                task_node = {
                    'id': f"task_{task['id']}",
                    'type': 'lpi',
                    'position': {'x': x_pos, 'y': task_y_pos},
                    'data': {
                        'name': task['name'],
                        'component_id': task['id'],
                        'id': f"task_{task['id']}"
                    },
                    'parentNode': f"phase_{phase['id']}",
                    'extent': 'parent'
                }
                rf_nodes.append(task_node)
                
                # 连接任务节点
                if j == 0:
                    # 第一个任务连接到阶段节点
                    rf_edges.append({
                        'id': f"edge_{phase['id']}_to_{task['id']}",
                        'source': f"phase_{phase['id']}",
                        'target': f"task_{task['id']}",
                        'type': 'smoothstep'
                    })
                else:
                    # 连接到前一个任务
                    prev_task = phase['tasks'][j-1]
                    rf_edges.append({
                        'id': f"edge_{prev_task['id']}_to_{task['id']}",
                        'source': f"task_{prev_task['id']}",
                        'target': f"task_{task['id']}",
                        'type': 'smoothstep'
                    })
        
        # 添加结束节点
        end_node = {
            'id': 'end',
            'type': 'end',
            'position': {'x': 50 + (phase_count + 1) * phase_spacing, 'y': 50},
            'data': {'name': '结束'}
        }
        rf_nodes.append(end_node)
        
        # 连接最后一个阶段到结束节点
        if phase_count > 0:
            last_phase = workflow['phases'][phase_count-1]
            rf_edges.append({
                'id': f"edge_{last_phase['id']}_to_end",
                'source': f"phase_{last_phase['id']}",
                'target': 'end',
                'type': 'smoothstep'
            })
        
        # 更新工作流中的ReactFlow数据
        workflow['nodes'] = rf_nodes
        workflow['edges'] = rf_edges
        
        # 保存更新后的工作流
        file_path = os.path.join(agent_dir, f"{workflow['filename']}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, ensure_ascii=False, indent=2)

def main():
    """主函数，执行所有生成任务"""
    print(f"正在从 {md_file} 生成数据...")
    
    # 读取并解析Markdown内容
    content = read_markdown_file(md_file)
    data = parse_markdown(content)
    
    # 生成各种JSON文件
    generate_lpi_files(data)
    generate_agent_files(data)
    generate_workflow_files(data)
    generate_reactflow_data(data)
    
    print("所有数据生成完成！")

if __name__ == "__main__":
    main() 