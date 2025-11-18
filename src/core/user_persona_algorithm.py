from typing import List, Dict, Any
from datetime import datetime
import logging

from src.models.mission import Mission
from src.models.target_info import TargetInfo
from src.models.user_persona import UserPersona
from src.core.persona_tag_calculator import PersonaTagCalculator


class UserPersonaAlgorithm:
    """用户画像算法主类"""
    
    def __init__(self):
        self.tag_calculator = PersonaTagCalculator()
        self.logger = self._setup_logger()
    
    def generate_user_persona(self,
                            target_info: List[TargetInfo],
                            mission: List[Mission],
                            start_time: str = None,
                            end_time: str = None,
                            algorithm: Dict[str, Any] = None,
                            params: Dict[str, Any] = None) -> List[UserPersona]:
        """
        生成用户画像
        :param target_info: 目标信息数据列表
        :param mission: 历史需求数据列表
        :param start_time: 开始时间（可选，格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS）
        :param end_time: 结束时间（可选，格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS）
        :param algorithm: 算法配置参数（可选，当前使用统计规则，此参数保留用于兼容性）
        :param params: 扩充参数
        :return: 用户画像结果列表
        """
        
        if params is None:
            params = {}
        
        self.logger.info("开始生成用户画像")
        if start_time or end_time:
            self.logger.info(f"时间范围: {start_time or '不限'} 至 {end_time or '不限'}")
        self.logger.info(f"输入数据: {len(target_info)} 个目标, {len(mission)} 条历史需求")
        
        try:
            # 1. 数据预处理和验证
            self._validate_input_data(target_info, mission)
            
            # 2. 根据时间范围过滤任务
            filtered_mission = self._filter_missions_by_time(mission, start_time, end_time)
            if len(filtered_mission) < len(mission):
                self.logger.info(f"时间过滤后保留 {len(filtered_mission)} 条需求")
            mission = filtered_mission
            
            # 3. 按用户分组处理
            user_personas = []
            user_groups = self._group_missions_by_user(mission, target_info)
            
            for user_key, (user_id, user_missions, related_targets) in user_groups.items():
                self.logger.info(f"处理用户 {user_key}, 相关需求数量: {len(user_missions)}")
                
                # 4. 使用统计规则生成画像标签
                persona_tags = self.tag_calculator.generate_persona_tags(
                    user_missions, related_targets
                )
                
                self.logger.info(f"用户 {user_key} 画像标签生成完成")
                
                # 5. 生成用户画像对象
                user_persona = UserPersona(
                    user_id=user_id,
                    persona_tags=persona_tags,
                    confidence_score=1.0,  # 统计规则100%置信度
                    feature_importance={},  # 不再需要特征重要性
                    algorithm_used='statistical_rules',  # 使用统计规则
                    generation_time=datetime.now().isoformat()
                )
                
                user_personas.append(user_persona)
                self.logger.info(f"用户 {user_key} 画像生成完成")
            
            self.logger.info(f"用户画像生成完成, 共生成 {len(user_personas)} 个画像")
            return user_personas
            
        except Exception as e:
            self.logger.error(f"用户画像生成失败: {str(e)}")
            raise
    
    def _validate_input_data(self, target_info: List[TargetInfo], mission: List[Mission]):
        """验证输入数据"""
        if not target_info:
            raise ValueError("目标信息数据列表不能为空")
        
        if not mission:
            raise ValueError("历史需求数据列表不能为空")
    
    def _group_missions_by_user(self, missions: List[Mission], targets: List[TargetInfo]) -> Dict[str, tuple]:
        """按用户分组需求数据"""
        target_dict = {target.target_id: target for target in targets}
        grouped_missions = {}
        
        for mission in missions:
            # 用户标识：部门+区组
            user_key = f"{mission.req_unit}_{mission.req_group}"
            
            if user_key not in grouped_missions:
                # 直接使用user_key作为user_id
                grouped_missions[user_key] = (user_key, [], [])
            
            # 添加任务到用户组
            grouped_missions[user_key][1].append(mission)
            
            # 添加相关目标到用户组（去重）
            if mission.target_id in target_dict:
                target = target_dict[mission.target_id]
                if target not in grouped_missions[user_key][2]:
                    grouped_missions[user_key][2].append(target)
        
        return grouped_missions
    
    def _filter_missions_by_time(self, 
                                  missions: List[Mission], 
                                  start_time: str = None, 
                                  end_time: str = None) -> List[Mission]:
        """
        根据时间范围过滤任务
        :param missions: 任务列表
        :param start_time: 开始时间（格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS）
        :param end_time: 结束时间（格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS）
        :return: 过滤后的任务列表
        """
        if not start_time and not end_time:
            return missions
        
        filtered_missions = []
        for mission in missions:
            # 获取任务的开始时间
            mission_time = mission.req_start_time
            
            # 检查时间范围
            if start_time and mission_time < start_time:
                continue
            if end_time and mission_time > end_time:
                continue
                
            filtered_missions.append(mission)
        
        return filtered_missions
    
    def _setup_logger(self) -> logging.Logger:
        """设置日志记录器"""
        logger = logging.getLogger('UserPersonaAlgorithm')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger


def user_persona_algorithm_api(target_info: List[TargetInfo],
                              mission: List[Mission],
                              start_time: str = None,
                              end_time: str = None,
                              algorithm: Dict[str, Any] = None,
                              params: Dict[str, Any] = None) -> List[UserPersona]:
    """
    用户画像算法API入口函数
    
    :param target_info: 目标信息数据列表
    :param mission: 历史需求数据列表
    :param start_time: 开始时间（可选，格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS）
    :param end_time: 结束时间（可选，格式：YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS）
    :param algorithm: 算法配置参数（可选，保留用于兼容性）
    :param params: 扩充参数
    :return: 用户画像结果列表
    """
    
    # 创建算法实例并执行
    persona_algorithm = UserPersonaAlgorithm()
    return persona_algorithm.generate_user_persona(
        target_info, mission, start_time, end_time, algorithm, params
    )
