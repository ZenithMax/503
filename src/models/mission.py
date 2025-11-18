class Mission:
    def __init__(self,
                 req_id: str,
                 topic_id: str,
                 req_unit: str,
                 req_group: str,
                 req_start_time: str,
                 req_end_time: str,
                 task_type: str,
                 target_id: str,
                 country_name: str,
                 target_priority: float,
                 is_emcon: str,
                 scout_type: str):
        """
        历史需求数据列表
        :param req_id: 需求标识号
        :param topic_id: 专题标识号
        :param req_unit: 提出部门
        :param req_group: 提出区组
        :param req_start_time: 需求有效开始时间
        :param req_end_time: 需求结束时间
        :param task_type: 任务类型
        :param target_id: 目标标识号
        :param country_name: 国家名称
        :param target_priority: 目标优先级
        :param is_emcon: 是否电磁管制
        :param scout_type: 侦察类型
        """
        self.req_id = req_id
        self.topic_id = topic_id
        self.req_unit = req_unit
        self.req_group = req_group
        self.req_start_time = req_start_time
        self.req_end_time = req_end_time
        self.task_type = task_type
        self.target_id = target_id
        self.country_name = country_name
        self.target_priority = target_priority
        self.is_emcon = is_emcon
        self.scout_type = scout_type

