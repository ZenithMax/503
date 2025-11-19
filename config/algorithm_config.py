"""
算法参数配置 - 基于统计规则的用户画像
"""

# ==================== 偏好计算算法参数 ====================

# TF-IDF 算法参数
TFIDF_CONFIG = {
    "smoothing": 1,  # IDF平滑参数，避免log(0)
    "min_users_required": 5,  # 最少用户数要求
    "min_targets_required": 10  # 最少目标数要求
}

# BM25 算法参数
BM25_CONFIG = {
    "k1": 1.5,  # TF饱和度参数，控制词频的影响（1.2-2.0）
    "b": 0.75,  # 长度归一化参数（0-1，0=不归一化，1=完全归一化）
    "min_users_required": 5,  # 最少用户数要求
    "min_targets_required": 10  # 最少目标数要求
}

# Z-score 算法参数
ZSCORE_CONFIG = {
    "threshold": 1.0,  # Z-score阈值，>1.0为显著（常用：1.0, 1.5, 2.0）
    "min_std": 0.01,  # 最小标准差，避免除零
    "min_targets_required": 5  # 最少目标数要求
}

# Percentage 算法参数
PERCENTAGE_CONFIG = {
    "default_top_n": 3  # 默认返回前N个
}

# ==================== 集中度计算参数 ====================

# HHI（赫芬达尔-赫希曼指数）阈值
HHI_THRESHOLD = 0.05  # 分散/集中分界线，>0.05为集中

# 变异系数（CV）阈值
CV_THRESHOLD = 1.0  # 高变异阈值，>1.0使用BM25

# ==================== 自动算法选择规则 ====================

# 注：使用上面定义的HHI_THRESHOLD和CV_THRESHOLD
ALGORITHM_AUTO_SELECTION = {
    
    # TF-IDF 选择条件
    "tfidf_conditions": {
        "min_users": 10,  # 最少用户数
        "min_targets": 20  # 最少目标数
    },
    
    # BM25 选择条件（需先满足基本条件，CV阈值使用上面的CV_THRESHOLD）
    "bm25_conditions": {
        "min_users": 5,  # 最少用户数
        "min_targets": 10  # 最少目标数
    },
    
    # Z-score 选择条件
    "zscore_conditions": {
        "min_targets": 5  # 最少目标数
    },
    
    # 默认算法
    "default_algorithm": "percentage"
}

# ==================== 标签生成规则 ====================

TAG_GENERATION_RULES = {
    # 提报需求频率标签
    "request_frequency": {
        "high": {"min_tasks": 100},  # 高频用户
        "medium": {"min_tasks": 30},  # 中频用户
        "low": {"min_tasks": 0}  # 低频用户
    },
    
    # 目标占比阈值
    "target_proportion": {
        "dominant_threshold": 0.5,  # 单个目标占比>50%为主导
        "significant_threshold": 0.2  # 单个目标占比>20%为显著
    },
    
    # 区域占比阈值
    "region_proportion": {
        "focused_threshold": 0.6,  # 单个区域>60%为聚焦
        "balanced_threshold": 0.3  # 各区域<30%为均衡
    },
    
    # 目标多样性
    "target_diversity": {
        "high": {"min_unique_targets": 20},  # 高多样性
        "medium": {"min_unique_targets": 10},  # 中等多样性
        "low": {"min_unique_targets": 0}  # 低多样性
    },
    
    # 偏好强度（基于集中度）
    "preference_strength": {
        "strong": {"min_hhi": 0.15},  # 强偏好
        "moderate": {"min_hhi": 0.05},  # 中等偏好
        "weak": {"min_hhi": 0.0}  # 弱偏好（分散）
    }
}

# ==================== 输出控制参数 ====================

OUTPUT_CONFIG = {
    "default_top_n": 3,  # 默认输出前N个结果
    "max_top_n": 20,  # 最大允许的top_n值
    "min_top_n": 1,  # 最小允许的top_n值
    "precision": 2  # 百分比保留小数位数
}

# ==================== 算法性能参数 ====================

PERFORMANCE_CONFIG = {
    "enable_caching": True,  # 是否启用全局统计缓存
    "cache_ttl": 3600,  # 缓存生存时间（秒）
    "max_users_for_tfidf": 10000,  # TF-IDF最大用户数限制
    "max_targets_for_calculation": 1000  # 单次计算最大目标数
}
