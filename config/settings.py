"""
系统配置文件
"""

import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "data"
SAMPLE_DATA_DIR = DATA_DIR / "sample"
GENERATED_DATA_DIR = DATA_DIR / "generated"

# 日志配置
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 算法配置
ALGORITHM_SELECTION_THRESHOLD = 5000  # 任务频次阈值
DEFAULT_ALGORITHM = "decision_tree"
SUPPORTED_ALGORITHMS = ["decision_tree", "random_forest"]

# 特征配置
MAX_FEATURE_VECTOR_SIZE = 30
MIN_MISSIONS_FOR_ANALYSIS = 1

# 数据生成配置
DEFAULT_NUM_TARGETS = 20
DEFAULT_NUM_MISSIONS = 1000
DEFAULT_NUM_USERS = 10

# 标签配置
PERSONA_TAG_TYPES = [
    "activity_level",      # 用户活跃度
    "mission_preference",  # 任务偏好
    "area_coverage",       # 区域覆盖度
    "target_diversity",    # 目标多样性
    "time_pattern",        # 时间规律性
    "priority_tendency"    # 优先级倾向
]

# 置信度阈值
CONFIDENCE_THRESHOLD = 0.6
