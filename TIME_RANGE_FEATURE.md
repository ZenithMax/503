# 时间范围过滤功能 ⏰

## 📋 功能说明

用户画像算法现在支持**时间范围过滤**，可以只计算指定时间段内的任务数据，生成该时间段的用户画像。

---

## 🎯 使用场景

### 场景1：分析特定时间段的用户行为
例如：分析2024年第一季度的用户画像

### 场景2：对比不同时间段的用户行为变化
例如：对比上半年和下半年的用户画像差异

### 场景3：只关注最近的用户行为
例如：只分析最近3个月的任务

### 场景4：历史数据分析
例如：分析2024年3月之前的历史行为

---

## 🔧 API 参数

### `generate_user_persona()` 方法

```python
def generate_user_persona(self,
                         target_info: List[TargetInfo],
                         mission: List[Mission],
                         algorithm: Dict[str, Any],
                         params: Dict[str, Any] = None,
                         start_time: str = None,      # 🆕 新增
                         end_time: str = None) -> List[UserPersona]:  # 🆕 新增
```

#### 新增参数说明

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `start_time` | `str` | 否 | 开始时间，格式：`YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS` |
| `end_time` | `str` | 否 | 结束时间，格式：`YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS` |

#### 参数组合说明

| start_time | end_time | 效果 |
|------------|----------|------|
| `None` | `None` | 不限制时间，使用所有任务数据 |
| `'2024-01-01'` | `'2024-12-31'` | 只使用2024年的任务数据 |
| `'2024-07-01'` | `None` | 使用2024年7月1日之后的任务数据 |
| `None` | `'2024-06-30'` | 使用2024年6月30日之前的任务数据 |

---

## 💻 使用示例

### 示例1：不限制时间范围（默认行为）

```python
from src.core.user_persona_algorithm import UserPersonaAlgorithm

algorithm = UserPersonaAlgorithm()

personas = algorithm.generate_user_persona(
    target_info=targets,
    mission=missions,
    algorithm={'classification_algorithm': 'auto'}
)
# 使用所有任务数据
```

### 示例2：指定时间范围（2024年上半年）

```python
personas = algorithm.generate_user_persona(
    target_info=targets,
    mission=missions,
    algorithm={'classification_algorithm': 'auto'},
    start_time='2024-01-01',
    end_time='2024-06-30'
)
# 只使用2024年1月1日到6月30日的任务数据
```

### 示例3：只限制开始时间（最近半年）

```python
personas = algorithm.generate_user_persona(
    target_info=targets,
    mission=missions,
    algorithm={'classification_algorithm': 'auto'},
    start_time='2024-07-01',
    end_time=None
)
# 只使用2024年7月1日之后的任务数据
```

### 示例4：只限制结束时间（历史数据）

```python
personas = algorithm.generate_user_persona(
    target_info=targets,
    mission=missions,
    algorithm={'classification_algorithm': 'auto'},
    start_time=None,
    end_time='2024-03-31'
)
# 只使用2024年3月31日之前的任务数据
```

### 示例5：精确到小时（包含时分秒）

```python
personas = algorithm.generate_user_persona(
    target_info=targets,
    mission=missions,
    algorithm={'classification_algorithm': 'auto'},
    start_time='2024-01-01 00:00:00',
    end_time='2024-01-31 23:59:59'
)
# 只使用2024年1月的任务数据（精确到秒）
```

---

## 🔍 工作原理

### 过滤逻辑

1. **基于任务开始时间** (`req_start_time`) 进行过滤
2. **字符串比较**：使用字符串比较进行时间过滤（要求时间格式统一）
3. **包含边界**：`start_time <= mission.req_start_time <= end_time`

### 过滤流程

```
输入任务列表 (50,000条)
    ↓
时间过滤 (start_time='2024-01-01', end_time='2024-06-30')
    ↓
保留符合条件的任务 (25,000条)
    ↓
按用户分组
    ↓
生成用户画像
```

---

## 📊 日志输出

使用时间范围时，日志会显示过滤信息：

```
2025-11-17 20:32:30 - UserPersonaAlgorithm - INFO - 开始生成用户画像
2025-11-17 20:32:30 - UserPersonaAlgorithm - INFO - 时间范围: 2024-01-01 至 2024-06-30
2025-11-17 20:32:30 - UserPersonaAlgorithm - INFO - 输入数据: 100 个目标, 50000 条历史需求
2025-11-17 20:32:30 - UserPersonaAlgorithm - INFO - 时间过滤后保留 25000 条需求
2025-11-17 20:32:30 - UserPersonaAlgorithm - INFO - 处理用户 第一情报部_华北区组, 相关需求数量: 450
...
```

---

## 🧪 测试脚本

### 运行演示脚本

```bash
python test_with_timerange.py
```

该脚本会测试4种场景：
1. 不限制时间范围
2. 限制时间范围（2024年上半年）
3. 只限制开始时间（2024年7月之后）
4. 只限制结束时间（2024年3月之前）

---

## ⚠️ 注意事项

### 1. 时间格式要求

- **标准格式**: `YYYY-MM-DD` 或 `YYYY-MM-DD HH:MM:SS`
- **必须一致**: 所有时间字符串必须使用相同的格式
- **字符串比较**: 使用字符串比较，确保格式正确

### 2. 时间范围有效性

```python
# ✅ 正确
start_time='2024-01-01'
end_time='2024-12-31'

# ❌ 错误（结束时间早于开始时间）
start_time='2024-12-31'
end_time='2024-01-01'
```

### 3. 空数据处理

如果时间范围内没有任务数据，会返回空的用户画像列表：

```python
personas = algorithm.generate_user_persona(
    ...,
    start_time='2025-01-01',  # 未来日期
    end_time='2025-12-31'
)
# personas = []  空列表
```

### 4. 性能考虑

- **过滤开销**: 时间过滤在内存中进行，性能开销很小
- **大数据集**: 对于超大数据集，建议在数据库层面先进行时间过滤

---

## 📈 应用场景示例

### 场景1：季度用户画像对比

```python
# Q1 画像
q1_personas = algorithm.generate_user_persona(
    ..., start_time='2024-01-01', end_time='2024-03-31'
)

# Q2 画像
q2_personas = algorithm.generate_user_persona(
    ..., start_time='2024-04-01', end_time='2024-06-30'
)

# Q3 画像
q3_personas = algorithm.generate_user_persona(
    ..., start_time='2024-07-01', end_time='2024-09-30'
)

# Q4 画像
q4_personas = algorithm.generate_user_persona(
    ..., start_time='2024-10-01', end_time='2024-12-31'
)

# 对比各季度用户行为变化
```

### 场景2：滚动窗口分析

```python
# 最近30天
recent_30d = algorithm.generate_user_persona(
    ..., start_time='2024-11-01', end_time='2024-11-30'
)

# 最近60天
recent_60d = algorithm.generate_user_persona(
    ..., start_time='2024-10-01', end_time='2024-11-30'
)

# 最近90天
recent_90d = algorithm.generate_user_persona(
    ..., start_time='2024-09-01', end_time='2024-11-30'
)
```

### 场景3：历史趋势分析

```python
# 按月生成画像，分析全年趋势
monthly_personas = {}
for month in range(1, 13):
    start = f'2024-{month:02d}-01'
    end = f'2024-{month:02d}-31'
    monthly_personas[month] = algorithm.generate_user_persona(
        ..., start_time=start, end_time=end
    )
```

---

## 🔄 API 函数支持

`user_persona_algorithm_api()` 函数同样支持时间范围参数：

```python
from src.core.user_persona_algorithm import user_persona_algorithm_api

personas = user_persona_algorithm_api(
    target_info=targets,
    mission=missions,
    algorithm={'classification_algorithm': 'auto'},
    params={},
    start_time='2024-01-01',
    end_time='2024-12-31'
)
```

---

## 📦 相关文件

| 文件 | 说明 |
|------|------|
| `src/core/user_persona_algorithm.py` | 核心实现（包含时间过滤逻辑） |
| `test_with_timerange.py` | 时间范围功能演示脚本 |
| `TIME_RANGE_FEATURE.md` | 本文档 |

---

## 🎉 总结

时间范围过滤功能让用户画像算法更加灵活：

- ✅ **灵活性**: 可以自由指定时间范围
- ✅ **易用性**: 简单的字符串参数
- ✅ **兼容性**: 不影响现有代码（参数可选）
- ✅ **高效性**: 内存过滤，性能优秀
- ✅ **可扩展**: 支持多种时间分析场景

---

**功能添加日期**: 2025-11-17  
**版本**: v1.1.0  
**状态**: ✅ 已完成并测试通过
