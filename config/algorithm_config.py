"""
算法参数配置
"""

# 决策树参数
DECISION_TREE_CONFIG = {
    "max_depth": 10,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "criterion": "gini",
    "random_state": 42
}

# 随机森林参数
RANDOM_FOREST_CONFIG = {
    "n_estimators": 100,
    "max_depth": 15,
    "min_samples_split": 5,
    "min_samples_leaf": 2,
    "criterion": "gini",
    "random_state": 42,
    "n_jobs": -1
}

# 特征提取参数
FEATURE_EXTRACTION_CONFIG = {
    "temporal_window_days": 30,
    "min_mission_sequence_length": 2,
    "entropy_calculation_method": "shannon",
    "diversity_metric": "unique_ratio"
}

# 自动选择规则
ALGORITHM_SELECTION_RULES = {
    "task_frequency_threshold": 5000,  # 任务频次阈值
    "high_frequency_algorithm": "random_forest",  # 高频次使用随机森林
    "low_frequency_algorithm": "decision_tree"    # 低频次使用决策树
}

# 标签生成规则
TAG_GENERATION_RULES = {
    "activity_level": {
        "high": {"min_tasks_per_period": 50},
        "medium": {"min_tasks_per_period": 10},
        "low": {"min_tasks_per_period": 0}
    },
    "mission_preference": {
        "emcon_focused": {"min_emcon_preference": 0.7},
        "mixed": {"min_emcon_preference": 0.3}
    },
    "area_coverage": {
        "wide": {"min_diversity": 0.6},
        "moderate": {"min_diversity": 0.3},
        "narrow": {"min_diversity": 0}
    },
    "target_diversity": {
        "high": {"min_entropy": 2.0},
        "medium": {"min_entropy": 1.0},
        "low": {"min_entropy": 0}
    },
    "time_pattern": {
        "regular": {"max_temporal_std": 0.3},
        "irregular": {"max_temporal_std": 1.0}
    },
    "priority_tendency": {
        "high_priority": {"min_avg_priority": 7},
        "medium_priority": {"min_avg_priority": 4},
        "low_priority": {"min_avg_priority": 0}
    }
}
