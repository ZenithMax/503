"""
用户画像系统核心模块
"""

__version__ = "1.0.0"
__author__ = "ZhangJiaHao"

from .core.user_persona_algorithm import UserPersonaAlgorithm
from .core.persona_tag_calculator import PersonaTagCalculator

__all__ = [
    'UserPersonaAlgorithm',
    'PersonaTagCalculator'
]
