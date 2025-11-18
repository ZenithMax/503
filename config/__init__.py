"""
配置模块
"""

# 直接导入配置变量，而不是类
from . import settings
from . import algorithm_config

__all__ = [
    'settings',
    'algorithm_config'
]
