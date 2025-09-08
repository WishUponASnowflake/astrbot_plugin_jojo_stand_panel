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
        
        # 解析可选参数：替身名字、替身描述、画布高度
        # 参数顺序：能力值 [替身名字] [替身描述] [画布高度]
        custom_name = None
        desc = None
        h = None
        
        # 解析剩余参数
        remaining_parts = message_parts[2:] if len(message_parts) > 2 else []
        
        # 按顺序解析参数
        if len(remaining_parts) >= 1:
            # 第一个参数是替身名字
            custom_name = remaining_parts[0]
        if len(remaining_parts) >= 2:
            # 第二个参数是替身描述
            desc = remaining_parts[1]
        if len(remaining_parts) >= 3:
            # 第三个参数是画布高度
            h = remaining_parts[2]

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

        # 生成替身面板URL，包含新的desc和h参数
        image_url = self.api_service.get_image_url(
            name=display_name, ability=ability_str, desc=desc, h=h
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