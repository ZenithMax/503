from typing import List, Dict, Any
from collections import Counter


class PersonaTagCalculator:
    """用户画像标签计算器 - 基于统计规则"""
    
    def __init__(self):
        pass
    
    def generate_persona_tags(self, 
                             missions: List[Any],
                             target_info: List[Any]) -> Dict[str, Any]:
        """
        基于统计规则生成用户画像标签
        :param missions: 用户的历史任务列表
        :param target_info: 目标信息列表
        :return: 画像标签字典
        """
        persona_tags = {}
        
        # 创建目标信息字典，便于查找
        target_dict = {t.target_id: t for t in target_info}
        
        # 1. 提报需求频率标签
        persona_tags['request_frequency'] = self._calculate_request_frequency(missions)
        
        # 2. 侦察目标占比标签
        persona_tags['target_proportion'] = self._calculate_target_proportion(missions)
        
        # 3. 侦察区域占比标签
        persona_tags['region_proportion'] = self._calculate_region_proportion(missions, target_dict)
        
        # 4. 偏爱目标类别标签
        persona_tags['preferred_target_category'] = self._calculate_target_category(missions, target_dict)
        
        # 5. 偏爱目标专题与分组标签
        persona_tags['preferred_topic_group'] = self._calculate_topic_group(missions, target_dict)
        
        # 6. 偏爱侦察场景标签
        persona_tags['preferred_scout_scenario'] = self._calculate_scout_scenario(missions)
        
        return persona_tags
    
    def _calculate_request_frequency(self, missions: List[Any]) -> Dict[str, Any]:
        """计算提报需求频率标签"""
        total_count = len(missions)
        
        # 统计时间分布（按时间段）
        time_distribution = {}
        # 这里可以根据req_start_time进行时间分组统计
        # 简化版本：只统计总数
        
        return {
            'total_count': total_count
        }
    
    def _calculate_target_proportion(self, missions: List[Any]) -> Dict[str, Any]:
        """计算侦察目标占比标签"""
        target_counts = Counter([m.target_id for m in missions])
        total = len(missions)
        
        # 计算Top目标及占比
        top_targets = []
        for target_id, count in target_counts.most_common():
            top_targets.append({
                'target_id': target_id,
                'count': count,
                'percentage': round(count / total * 100, 2)
            })
        
        return {
            'total_targets': len(target_counts),
            'top_targets': top_targets
        }
    
    def _calculate_region_proportion(self, missions: List[Any], target_dict: Dict[str, Any]) -> Dict[str, Any]:
        """计算侦察区域占比标签"""
        region_counts = Counter()
        
        for mission in missions:
            target = target_dict.get(mission.target_id)
            if target and hasattr(target, 'target_area_type'):
                region_counts[target.target_area_type] += 1
        
        total = sum(region_counts.values())
        if total == 0:
            return {'total_regions': 0, 'top_regions': []}
        
        # 计算Top区域及占比
        top_regions = []
        for region, count in region_counts.most_common():
            top_regions.append({
                'region': region,
                'count': count,
                'percentage': round(count / total * 100, 2)
            })
        
        return {
            'total_regions': len(region_counts),
            'top_regions': top_regions
        }
    
    def _calculate_target_category(self, missions: List[Any], target_dict: Dict[str, Any]) -> Dict[str, Any]:
        """计算偏爱目标类别标签 - 统计target_type和target_category组合的Top3及占比"""
        category_counts = Counter()
        
        for mission in missions:
            target = target_dict.get(mission.target_id)
            if target:
                # 组合 target_type 和 target_category
                combo = f"{target.target_type}_{target.target_category}"
                category_counts[combo] += 1
        
        total = sum(category_counts.values())
        if total == 0:
            return {'top3_categories': []}
        
        # 获取Top3组合及占比
        top3 = []
        for combo, count in category_counts.most_common(3):
            type_category = combo.split('_', 1)
            top3.append({
                'target_type': type_category[0] if len(type_category) > 0 else '',
                'target_category': type_category[1] if len(type_category) > 1 else '',
                'count': count,
                'percentage': round(count / total * 100, 2)
            })
        
        return {
            'top3_categories': top3,
            'total_combinations': len(category_counts)
        }
    
    def _calculate_topic_group(self, missions: List[Any], target_dict: Dict[str, Any]) -> Dict[str, Any]:
        """计算偏爱目标专题与分组标签 - 统计topic_id和group_list组合的Top3及占比"""
        topic_group_counts = Counter()
        
        for mission in missions:
            topic_id = mission.topic_id
            target = target_dict.get(mission.target_id)
            
            if target and hasattr(target, 'group_list') and target.group_list:
                # 遍历目标的所有分组
                for group in target.group_list:
                    group_name = group.group_name if hasattr(group, 'group_name') else str(group)
                    combo = f"{topic_id}_{group_name}"
                    topic_group_counts[combo] += 1
            else:
                # 如果没有group_list，只统计topic_id
                combo = f"{topic_id}_无分组"
                topic_group_counts[combo] += 1
        
        total = sum(topic_group_counts.values())
        if total == 0:
            return {'top3_combinations': []}
        
        # 获取Top3组合及占比
        top3 = []
        for combo, count in topic_group_counts.most_common(3):
            parts = combo.split('_', 1)
            top3.append({
                'topic_id': parts[0] if len(parts) > 0 else '',
                'group_name': parts[1] if len(parts) > 1 else '',
                'count': count,
                'percentage': round(count / total * 100, 2)
            })
        
        return {
            'top3_combinations': top3,
            'total_combinations': len(topic_group_counts)
        }
    
    def _calculate_scout_scenario(self, missions: List[Any]) -> Dict[str, Any]:
        """计算偏爱侦察场景标签 - 统计task_type和scout_type组合的Top3及占比"""
        scenario_counts = Counter()
        
        for mission in missions:
            combo = f"{mission.task_type}_{mission.scout_type}"
            scenario_counts[combo] += 1
        
        total = len(missions)
        if total == 0:
            return {'top3_scenarios': []}
        
        # 获取Top3组合及占比
        top3 = []
        for combo, count in scenario_counts.most_common(3):
            parts = combo.split('_', 1)
            top3.append({
                'task_type': parts[0] if len(parts) > 0 else '',
                'scout_type': parts[1] if len(parts) > 1 else '',
                'count': count,
                'percentage': round(count / total * 100, 2)
            })
        
        return {
            'top3_scenarios': top3,
            'total_combinations': len(scenario_counts)
        }
