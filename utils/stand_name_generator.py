"""
替身名字生成器
"""
import random
from typing import List

from .config_manager import ConfigManager


class StandNameGenerator:
    """替身名字生成器"""
    
    def __init__(self, config_manager: ConfigManager):
        """
        初始化替身名字生成器
        
        Args:
            config_manager: 配置管理器
        """
        self.config_manager = config_manager
    
    def generate_random_stand_name(self) -> str:
        """
        生成随机的替身名字
        
        Returns:
            str: 随机替身名字
        """
        # 从配置中获取前后缀词库
        prefixes = self.config_manager.get_stand_name_prefixes()
        suffixes = self.config_manager.get_stand_name_suffixes()
        
        # 随机选择前缀和后缀
        prefix = random.choice(prefixes)
        suffix = random.choice(suffixes)
        
        return f"{prefix}{suffix}"