"""
替身指令处理器基类
"""

from typing import Optional
from astrbot.api.event import AstrMessageEvent
from astrbot.core.platform.message_type import MessageType
from astrbot.api import logger
import astrbot.api.message_components as Comp

from ..services.stand_data_service import StandDataService
from ..services.api_service import StandAPIService
from ..utils.config_manager import ConfigManager
from ..utils.cooldown_manager import CooldownManager


class BaseStandHandler:
    """替身指令处理器基类"""

    def __init__(
        self,
        data_service: StandDataService,
        api_service: StandAPIService,
        cooldown_manager: CooldownManager,
        group_white_list: list,
        timezone,
        stand_name_generator,
        config_manager: ConfigManager,
    ):
        """
        初始化处理器

        Args:
            data_service: 数据服务
            api_service: API服务
            cooldown_manager: 冷却管理器
            group_white_list: 群组白名单
            timezone: 时区
            stand_name_generator: 替身名字生成器
            config_manager: 配置管理器
        """
        self.data_service = data_service
        self.api_service = api_service
        self.cooldown_manager = cooldown_manager
        self.group_white_list = group_white_list
        self.timezone = timezone
        self.stand_name_generator = stand_name_generator
        self.config_manager = config_manager

    def check_group_permission(self, event: AstrMessageEvent) -> bool:
        """
        检查群组权限

        Args:
            event: 消息事件

        Returns:
            bool: 是否有权限
        """
        # 如果白名单功能被禁用，则允许所有群聊使用
        if not self.config_manager.is_whitelist_enabled():
            return True

        if event.get_message_type() == MessageType.GROUP_MESSAGE:
            if event.get_group_id() not in self.group_white_list:
                logger.info("群聊不在白名单中:" + event.get_group_id())
                return False
        return True

    async def send_response(
        self, event: AstrMessageEvent, text: str, image_url: Optional[str] = None
    ):
        """
        发送响应消息

        Args:
            event: 消息事件
            text: 文本消息
            image_url: 图片URL（可选）
        """
        chain = [Comp.Plain(text)]
        if image_url:
            chain.append(Comp.Image.fromURL(image_url))
        yield event.chain_result(chain)
