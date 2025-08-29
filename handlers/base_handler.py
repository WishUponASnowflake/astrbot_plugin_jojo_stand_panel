"""
本文档由AI生成

基础指令处理器，提供通用的指令处理逻辑
"""

from typing import Optional
from astrbot.api.event import AstrMessageEvent
from astrbot.api.platform import MessageType
from astrbot.api import logger
import astrbot.api.message_components as Comp

from ..resources import UITexts

from ..utils.service_container import ServiceContainer


class BaseStandHandler:
    """替身指令处理器基类"""

    def __init__(self, service_container: ServiceContainer):
        """
        初始化处理器

        Args:
            service_container: 服务容器
        """
        self.service_container = service_container

        # 从服务容器获取所有依赖
        self.data_service = service_container.get_data_service()
        self.api_service = service_container.get_api_service()
        self.cooldown_manager = service_container.get_cooldown_manager()
        self.group_white_list = service_container.get_group_white_list()
        self.timezone = service_container.get_timezone()
        self.stand_name_generator = service_container.get_stand_name_generator()
        self.config_manager = service_container.get_config_manager()

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
                logger.info(
                    UITexts.GROUP_NOT_IN_WHITELIST.format(group_id=event.get_group_id())
                )
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
        chain = []
        chain.append(Comp.Plain(text))
        if image_url:
            chain.append(Comp.Image.fromURL(image_url))
        yield event.chain_result(chain)
