"""
工具函数模块
"""

from .data_generator import (
    generate_sample_data,
    generate_target_info,
    generate_smart_data,
    save_data_to_files,
    print_data_statistics
)

__all__ = [
    'generate_sample_data',
    'generate_target_info',
    'generate_smart_data',
    'save_data_to_files',
    'print_data_statistics'
]
