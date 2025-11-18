#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户画像算法测试 - 带时间范围过滤
演示如何使用时间范围参数
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
    
    # 查看任务的时间范围
    if missions:
        time_list = sorted([m.req_start_time for m in missions])
        print(f"任务时间范围: {time_list[0]} 至 {time_list[-1]}")
        print(f"总任务数: {len(missions)}")
        print()
    
    # 2. 初始化算法
    algorithm = UserPersonaAlgorithm()
    algorithm_config = {'classification_algorithm': 'auto'}
    
    # 测试场景1: 不限制时间范围（获取所有数据）
    print("=" * 80)
    print("场景1: 不限制时间范围")
    print("=" * 80)
    personas_all = algorithm.generate_user_persona(
        target_info=targets,
        mission=missions,
        algorithm=algorithm_config,
        start_time=None,
        end_time=None
    )
    print(f"✓ 生成了 {len(personas_all)} 个用户画像")
    print()
    
    # 测试场景2: 限制时间范围（例如：2024年上半年）
    print("=" * 80)
    print("场景2: 限制时间范围（2024年上半年）")
    print("=" * 80)
    personas_filtered = algorithm.generate_user_persona(
        target_info=targets,
        mission=missions,
        algorithm=algorithm_config,
        start_time='2024-01-01',
        end_time='2024-06-30'
    )
    print(f"✓ 生成了 {len(personas_filtered)} 个用户画像")
    print()
    
    # 测试场景3: 只限制开始时间
    print("=" * 80)
    print("场景3: 只限制开始时间（2024年7月之后）")
    print("=" * 80)
    personas_after = algorithm.generate_user_persona(
        target_info=targets,
        mission=missions,
        algorithm=algorithm_config,
        start_time='2024-07-01',
        end_time=None
    )
    print(f"✓ 生成了 {len(personas_after)} 个用户画像")
    print()
    
    # 测试场景4: 只限制结束时间
    print("=" * 80)
    print("场景4: 只限制结束时间（2024年3月之前）")
    print("=" * 80)
    personas_before = algorithm.generate_user_persona(
        target_info=targets,
        mission=missions,
        algorithm=algorithm_config,
        start_time=None,
        end_time='2024-03-31'
    )
    print(f"✓ 生成了 {len(personas_before)} 个用户画像")
    print()
    
    # 保存场景1的结果
    result = {
        "test_info": {
            "num_targets": len(targets),
            "num_missions": len(missions),
            "test_date": datetime.now().isoformat(),
            "time_range": "不限制"
        },
        "personas": []
    }
    
    for persona in personas_all:
        persona_data = {
            "user_id": persona.user_id,
            "persona_tags": persona.persona_tags,
            "generation_time": persona.generation_time
        }
        result["personas"].append(persona_data)
    
    # 保存结果
    with open('test_result_timerange.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("=" * 80)
    print("测试完成!")
    print(f"完整结果已保存到: test_result_timerange.json")
    print("=" * 80)

if __name__ == "__main__":
    main()
