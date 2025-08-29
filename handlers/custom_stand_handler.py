"""
本文档由AI生成

自定义替身指令处理器
"""

from astrbot.api.event import AstrMessageEvent
import astrbot.api.message_components as Comp

from .base_handler import BaseStandHandler
from ..utils.ability_utils import AbilityUtils
from ..utils.ability_display_utils import AbilityDisplayUtils
from ..resources import UITexts


class CustomStandHandler(BaseStandHandler):
    """自定义替身指令处理器"""

    async def handle_create_stand(self, event: AstrMessageEvent):
        """处理创建替身指令"""
        if not self.check_group_permission(event):
            return

        # 解析命令参数
        message_parts = event.message_str.strip().split()

        if len(message_parts) < 2:
            # 显示帮助信息
            yield event.chain_result([Comp.Plain(UITexts.CREATE_STAND_HELP)])
            return

        abilities_input = message_parts[1]
        custom_name = " ".join(message_parts[2:]) if len(message_parts) > 2 else None

        # 解析能力值
        ability_str = AbilityUtils.parse_abilities(abilities_input)

        if ability_str is None:
            yield event.chain_result(
                [Comp.Plain(UITexts.CREATE_STAND_INVALID_ABILITIES)]
            )
            return

        # 如果没有提供自定义名字，使用用户昵称
        if custom_name is None:
            display_name = event.get_sender_name()
        else:
            display_name = custom_name

        # 生成替身面板URL
        image_url = self.api_service.get_image_url(
            name=display_name, ability=ability_str
        )

        # 格式化能力值显示
        ability_letters = AbilityUtils.convert_abilities_to_letters(ability_str)
        formatted_abilities = AbilityDisplayUtils.format_abilities_compact(
            ability_letters
        )

        # 构建回复消息
        if custom_name:
            response_text = UITexts.CREATE_STAND_SUCCESS_WITH_NAME.format(
                stand_name=custom_name, abilities=formatted_abilities
            )
        else:
            response_text = UITexts.CREATE_STAND_SUCCESS_WITHOUT_NAME.format(
                abilities=formatted_abilities
            )

        async for result in self.send_response(event, response_text, image_url):
            yield result
