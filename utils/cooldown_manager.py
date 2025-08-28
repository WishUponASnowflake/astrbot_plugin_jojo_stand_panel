"""
冷却时间管理工具类
"""
import time
from typing import Tuple


class CooldownManager:
    """冷却时间管理器"""
    
    def __init__(self, cooldown_seconds: int = 300):
        """
        初始化冷却管理器
        
        Args:
            cooldown_seconds: 冷却时间（秒）
        """
        self.cooldown_seconds = cooldown_seconds
        self.user_cooldowns = {}  # {user_id: last_use_timestamp}
    
    def check_cooldown(self, user_id: str) -> Tuple[bool, int]:
        """
        检查用户冷却时间
        
        Args:
            user_id: 用户ID
            
        Returns:
            tuple[bool, int]: (是否可以使用, 剩余冷却时间秒数)
        """
        if self.cooldown_seconds <= 0:
            return True, 0
            
        current_time = time.time()
        last_use_time = self.user_cooldowns.get(user_id, 0)
        
        # 计算剩余冷却时间
        remaining_cooldown = self.cooldown_seconds - (current_time - last_use_time)
        
        if remaining_cooldown <= 0:
            # 更新最后使用时间
            self.user_cooldowns[user_id] = current_time
            return True, 0
        else:
            return False, int(remaining_cooldown)
    
    def format_cooldown_message(self, remaining_seconds: int) -> str:
        """
        格式化冷却时间提示消息
        
        Args:
            remaining_seconds: 剩余冷却时间（秒）
            
        Returns:
            str: 格式化的提示消息
        """
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        
        if minutes > 0:
            return f"随机替身命令冷却中，还需等待 {minutes} 分 {seconds} 秒后才能再次使用，如需频繁使用请进入官网: http://tripleying.com/jojo"
        else:
            return f"随机替身命令冷却中，还需等待 {seconds} 秒后才能再次使用，如需频繁使用请进入官网: http://tripleying.com/jojo"