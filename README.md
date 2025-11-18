# 用户画像算法

用户画像分析系统，基于`req_unit`和`req_group`标识用户。

## 使用

```python
from src.core.user_persona_algorithm import UserPersonaAlgorithm
from src.utils.data_generator import generate_sample_data

# 生成数据
targets, missions = generate_sample_data(num_targets=5, num_missions=100)

# 生成画像
algorithm = UserPersonaAlgorithm()
personas = algorithm.generate_user_persona(
    target_info=targets,
    mission=missions,
    algorithm={'classification_algorithm': 'auto'}
)
```

## 项目结构

- `config/` - 配置文件
- `src/core/` - 核心算法
- `src/models/` - 数据模型
- `src/utils/` - 工具函数

## 算法

- 任务≤5000：决策树
- 任务>5000：随机森林
