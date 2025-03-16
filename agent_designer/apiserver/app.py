from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import random

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Agent设计器示例API服务"

@app.route('/fault-diagnosis', methods=['POST'])
def fault_diagnosis():
    """故障诊断API"""
    data = request.json
    fault_phenomenon = data.get('fault_phenomenon', '')
    business_object = data.get('business_object', '')
    
    # 模拟处理时间
    time.sleep(1)
    
    # 根据输入生成诊断结果
    if '数据库' in fault_phenomenon:
        return jsonify({
            'fault_reason': f'{business_object}数据库连接超时',
            'fault_location': '数据库服务器192.168.1.100',
            'repair_suggestion': '重启数据库服务或检查网络连接',
            'recovery_suggestion': '启用备用数据库服务器'
        })
    elif '网络' in fault_phenomenon:
        return jsonify({
            'fault_reason': f'{business_object}网络连接异常',
            'fault_location': '网络交换机192.168.0.1',
            'repair_suggestion': '重启网络设备或检查网络配置',
            'recovery_suggestion': '启用备用网络链路'
        })
    elif '服务器' in fault_phenomenon:
        return jsonify({
            'fault_reason': f'{business_object}服务器CPU使用率过高',
            'fault_location': '应用服务器192.168.1.50',
            'repair_suggestion': '重启应用服务或优化代码',
            'recovery_suggestion': '启用负载均衡'
        })
    else:
        return jsonify({
            'fault_reason': f'{business_object}未知故障',
            'fault_location': '未确定',
            'repair_suggestion': '联系技术支持',
            'recovery_suggestion': '使用备用系统'
        })

@app.route('/business-recovery', methods=['POST'])
def business_recovery():
    """业务恢复API"""
    data = request.json
    fault_reason = data.get('fault_reason', '')
    fault_location = data.get('fault_location', '')
    recovery_suggestion = data.get('recovery_suggestion', '')
    
    # 模拟处理时间
    time.sleep(1.5)
    
    # 根据输入生成恢复结果
    if '数据库' in fault_reason:
        return jsonify({
            'recovery_plan': f'启用备用数据库服务器{fault_location.replace("100", "101")}，并切换业务连接',
            'business_recovery_result': '业务已成功切换到备用数据库，服务恢复正常'
        })
    elif '网络' in fault_reason:
        return jsonify({
            'recovery_plan': '启用备用网络链路，并切换业务流量',
            'business_recovery_result': '业务已成功切换到备用网络，连接恢复正常'
        })
    elif '服务器' in fault_reason:
        return jsonify({
            'recovery_plan': '启用负载均衡，分散业务请求到其他服务器',
            'business_recovery_result': '业务已成功分散到其他服务器，性能恢复正常'
        })
    else:
        return jsonify({
            'recovery_plan': f'根据建议"{recovery_suggestion}"执行恢复操作',
            'business_recovery_result': '业务已部分恢复，持续监控中'
        })

@app.route('/fault-repair', methods=['POST'])
def fault_repair():
    """故障修复API"""
    data = request.json
    fault_reason = data.get('fault_reason', '')
    fault_location = data.get('fault_location', '')
    repair_suggestion = data.get('repair_suggestion', '')
    
    # 模拟处理时间
    time.sleep(2)
    
    # 根据输入生成修复结果
    if '数据库' in fault_reason:
        return jsonify({
            'repair_plan': '重启数据库服务并检查网络连接状态',
            'repair_result': '数据库服务已重启，网络连接恢复正常'
        })
    elif '网络' in fault_reason:
        return jsonify({
            'repair_plan': '重启网络设备并更新网络配置',
            'repair_result': '网络设备已重启，配置已更新，连接恢复正常'
        })
    elif '服务器' in fault_reason:
        return jsonify({
            'repair_plan': '重启应用服务并优化代码',
            'repair_result': '应用服务已重启，性能监控正常'
        })
    else:
        return jsonify({
            'repair_plan': f'根据建议"{repair_suggestion}"执行修复操作',
            'repair_result': '修复操作已完成，等待验证'
        })

@app.route('/repair-verification', methods=['POST'])
def repair_verification():
    """修复验证API"""
    data = request.json
    repair_result = data.get('repair_result', '')
    
    # 模拟处理时间
    time.sleep(1)
    
    # 随机生成验证结果，90%成功率
    success = random.random() < 0.9
    
    if success:
        if '数据库' in repair_result:
            return jsonify({
                'verification_result': '验证通过，数据库服务运行正常，连接稳定'
            })
        elif '网络' in repair_result:
            return jsonify({
                'verification_result': '验证通过，网络连接稳定，延迟正常'
            })
        elif '服务器' in repair_result:
            return jsonify({
                'verification_result': '验证通过，服务器负载正常，响应时间达标'
            })
        else:
            return jsonify({
                'verification_result': '验证通过，系统运行正常'
            })
    else:
        return jsonify({
            'verification_result': '验证失败，需要进一步修复'
        })

@app.route('/fault-summary', methods=['POST'])
def fault_summary():
    """故障总结API"""
    data = request.json
    history_records = data.get('history_records', [])
    
    # 模拟处理时间
    time.sleep(1.5)
    
    # 提取关键信息
    fault_info = {}
    for record in history_records:
        if record.get('step') == '故障诊断':
            fault_info['phenomenon'] = record.get('input', {}).get('fault_phenomenon', '')
            fault_info['reason'] = record.get('output', {}).get('fault_reason', '')
        elif record.get('step') == '故障修复':
            fault_info['repair'] = record.get('output', {}).get('repair_result', '')
        elif record.get('step') == '业务恢复':
            fault_info['recovery'] = record.get('output', {}).get('business_recovery_result', '')
    
    # 生成总结
    if '数据库' in fault_info.get('reason', ''):
        summary = f"本次故障为{fault_info.get('reason', '未知故障')}，通过{fault_info.get('repair', '修复操作')}解决。期间通过{fault_info.get('recovery', '恢复操作')}保证了业务连续性。建议加强数据库监控，提前发现连接异常。"
    elif '网络' in fault_info.get('reason', ''):
        summary = f"本次故障为{fault_info.get('reason', '未知故障')}，通过{fault_info.get('repair', '修复操作')}解决。期间通过{fault_info.get('recovery', '恢复操作')}保证了业务连续性。建议加强网络监控，提前发现连接异常。"
    elif '服务器' in fault_info.get('reason', ''):
        summary = f"本次故障为{fault_info.get('reason', '未知故障')}，通过{fault_info.get('repair', '修复操作')}解决。期间通过{fault_info.get('recovery', '恢复操作')}保证了业务连续性。建议加强服务器性能监控，提前发现负载异常。"
    else:
        summary = f"本次故障原因为{fault_info.get('reason', '未知')}，已通过相应措施解决。建议加强系统监控，提前发现潜在问题。"
    
    return jsonify({
        'fault_summary': summary
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 