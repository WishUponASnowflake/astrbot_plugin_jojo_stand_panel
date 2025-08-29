"""
服务容器类，用于管理插件中的所有依赖项
"""

from typing import Any, Optional
import pytz

from ..services.stand_data_service import StandDataService
from ..services.api_service import StandAPIService
from .cooldown_manager import CooldownManager
from .config_manager import ConfigManager
from .stand_name_generator import StandNameGenerator


class ServiceContainer:
    """服务容器类，统一管理所有依赖项"""

    def __init__(
        self, config_manager: ConfigManager, data_dir_path: Optional[str] = None
    ):
        """
        初始化服务容器

        Args:
            config_manager: 配置管理器
            data_dir_path: 数据目录路径（可选）
        """
        self.config_manager = config_manager
        self.data_dir_path = data_dir_path
        self.timezone = pytz.timezone("Asia/Shanghai")

        # 从配置中获取参数
        self.api_server = config_manager.get_api_server()
        self.group_white_list = config_manager.get_white_list()
        self.random_cooldown = config_manager.get_random_cooldown()

        # 初始化所有服务
        self._init_services()

    def _init_services(self):
        """初始化所有服务"""
        self.data_service = StandDataService(self.timezone, self.data_dir_path)
        self.api_service = StandAPIService(self.api_server)
        self.cooldown_manager = CooldownManager(self.random_cooldown)
        self.stand_name_generator = StandNameGenerator(self.config_manager)

    def get_data_service(self) -> StandDataService:
        """获取数据服务"""
        return self.data_service

    def get_api_service(self) -> StandAPIService:
        """获取API服务"""
        return self.api_service

    def get_cooldown_manager(self) -> CooldownManager:
        """获取冷却管理器"""
        return self.cooldown_manager

    def get_config_manager(self) -> ConfigManager:
        """获取配置管理器"""
        return self.config_manager

    def get_stand_name_generator(self) -> StandNameGenerator:
        """获取替身名生成器"""
        return self.stand_name_generator

    def get_group_white_list(self) -> list:
        """获取群组白名单"""
        return self.group_white_list

    def get_timezone(self) -> Any:
        """获取时区"""
        return self.timezone
