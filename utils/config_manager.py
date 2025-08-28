"""
配置管理工具类
"""
from typing import List
from astrbot.api import AstrBotConfig


class ConfigManager:
    """配置管理器"""
    
    # 默认前缀词库
    DEFAULT_PREFIXES = [
        "白金", "黄金", "钻石", "紫金", "银色", "黑暗", "光辉", "烈焰", "寒冰", "雷电",
        "疾风", "大地", "天空", "星辰", "月光", "太阳", "深渊", "圣洁", "魔法", "神秘",
        "极光", "暴风", "海洋", "森林", "山峰", "火焰", "水晶", "虹彩", "幻影", "永恒"
    ]
    
    # 默认后缀词库
    DEFAULT_SUFFIXES = [
        "之星", "使者", "战士", "守护", "刃", "翼", "之力", "王者", "骑士", "法师",
        "之心", "灵魂", "命运", "审判", "制裁", "救赎", "希望", "梦想", "传说", "神话",
        "奇迹", "光芒", "影子", "风暴", "烈火", "寒霜", "雷鸣", "波涛", "山岳", "天使"
    ]
    
    def __init__(self, config: AstrBotConfig):
        """
        初始化配置管理器
        
        Args:
            config: AstrBot配置对象
        """
        self.config = config
    
    def get_stand_name_prefixes(self) -> List[str]:
        """
        获取替身名称前缀词库
        
        Returns:
            List[str]: 前缀词库列表
        """
        prefixes = self.config.get("stand_name_prefixes", self.DEFAULT_PREFIXES)
        
        # 确保返回的是列表且不为空
        if not isinstance(prefixes, list) or len(prefixes) == 0:
            return self.DEFAULT_PREFIXES
        
        return prefixes
    
    def get_stand_name_suffixes(self) -> List[str]:
        """
        获取替身名称后缀词库
        
        Returns:
            List[str]: 后缀词库列表
        """
        suffixes = self.config.get("stand_name_suffixes", self.DEFAULT_SUFFIXES)
        
        # 确保返回的是列表且不为空
        if not isinstance(suffixes, list) or len(suffixes) == 0:
            return self.DEFAULT_SUFFIXES
        
        return suffixes
    
    def get_api_server(self) -> str:
        """
        获取API服务器地址
        
        Returns:
            str: API服务器地址
        """
        return self.config.get("api_server", "https://api.tripleying.com/api/chart")
    
    def get_white_list(self) -> List[str]:
        """
        获取群聊白名单
        
        Returns:
            List[str]: 群聊白名单
        """
        return self.config.get("white_list", [])
    
    def get_random_cooldown(self) -> int:
        """
        获取随机替身冷却时间
        
        Returns:
            int: 冷却时间（秒）
        """
        return self.config.get("random_cooldown", 300)
    
    def get_daily_awaken_limit(self) -> int:
        """
        获取每日觉醒次数限制
        
        Returns:
            int: 每日觉醒次数限制，-1为不限次数，0为禁用
        """
        return self.config.get("daily_awaken_limit", 1)
    
    def is_awaken_system_enabled(self) -> bool:
        """
        检查觉醒系统是否启用
        
        Returns:
            bool: 觉醒系统是否启用
        """
        return self.config.get("enable_awaken_system", True)
    
    def is_whitelist_enabled(self) -> bool:
        """
        检查白名单是否启用
        
        Returns:
            bool: 白名单是否启用
        """
        return self.config.get("enable_whitelist", True)
    
    def is_set_stand_enabled(self) -> bool:
        """
        检查设置替身指令是否启用
        
        Returns:
            bool: 设置替身指令是否启用
        """
        return self.config.get("enable_set_stand", True)
    
    def is_view_others_stand_enabled(self) -> bool:
        """
        检查他的替身指令是否启用
        
        Returns:
            bool: 他的替身指令是否启用
        """
        return self.config.get("enable_view_others_stand", True)