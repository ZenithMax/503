class UserPersona:
    def __init__(self,
                 user_id: dict,
                 persona_tags: dict,
                 confidence_score: float,
                 feature_importance: dict,
                 algorithm_used: str,
                 generation_time: str,
                 target_id: str = None):
        """
        用户画像结果数据模型
        :param user_identity: 用户身份信息（req_unit和req_group）
        :param persona_tags: 画像标签字典，包含各种分类结果
        :param confidence_score: 置信度分数 (0-1)
        :param feature_importance: 特征重要性字典
        :param algorithm_used: 使用的算法类型
        :param generation_time: 生成时间
        :param target_id: 目标标识号（已废弃，保留用于兼容性）
        """
        self.user_id = user_id
        self.persona_tags = persona_tags
        self.confidence_score = confidence_score
        self.feature_importance = feature_importance
        self.algorithm_used = algorithm_used
        self.generation_time = generation_time
        self.target_id = target_id  # 保留用于向后兼容

    def to_dict(self):
        """转换为字典格式"""
        return {
            'user_id': self.user_id,
            'persona_tags': self.persona_tags,
            'confidence_score': self.confidence_score,
            'feature_importance': self.feature_importance,
            'algorithm_used': self.algorithm_used,
            'generation_time': self.generation_time
        }
