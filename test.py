#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目功能测试 - 基于统计规则的用户画像
"""

import json
import sys
import io
from datetime import datetime
from src.core.user_persona_algorithm import UserPersonaAlgorithm
from src.utils.data_generator import generate_sample_data

# 设置输出编码
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def main():
    # 1. 生成测试数据
    try:
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        targets, missions = generate_sample_data(num_targets=100, num_missions=50000)
        sys.stdout = old_stdout
    except Exception as e:
        sys.stdout = old_stdout
        print(f"警告: 使用data_generator失败 ({e})，使用备用方案...")
        raise
    
    # 统计用户数
    users = set()
    for mission in missions:
        users.add(f"{mission.req_unit}_{mission.req_group}")
    
    # 2. 初始化算法并生成用户画像
    algorithm = UserPersonaAlgorithm()
    algorithm_config = {'classification_algorithm': 'auto'}
    
    # 可选：指定时间范围（留空表示不限制）
    # 示例：start_time='2024-01-01', end_time='2024-12-31'
    personas = algorithm.generate_user_persona(
        target_info=targets,
        mission=missions,
        algorithm=algorithm_config,
        start_time=None,  # 不限制开始时间
        end_time=None     # 不限制结束时间
    )
    
    # 3. 构建JSON结果
    result = {
        "test_info": {
            "num_targets": len(targets),
            "num_missions": len(missions),
            "num_users": len(users),
            "test_date": datetime.now().isoformat()
        },
        "personas": [],
        "statistics": {
            "total_personas": len(personas)
        }
    }
    
    # 添加用户画像数据
    for persona in personas:
        persona_data = {
            "user_id": persona.user_id,
            "persona_tags": persona.persona_tags,
            "generation_time": persona.generation_time
        }
        result["personas"].append(persona_data)
    
    # 4. 输出JSON结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 5. 保存结果到文件
    with open('test_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print("\n结果已保存到: test_result.json")

if __name__ == "__main__":
    main()
