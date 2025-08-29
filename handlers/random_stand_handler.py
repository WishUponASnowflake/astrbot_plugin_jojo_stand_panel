"""
本文档由AI生成

随机替身指令处理器
"""

import datetime
import random
from astrbot.api.event import AstrMessageEvent
import astrbot.api.message_components as Comp

from .base_handler import BaseStandHandler
from ..utils.ability_utils import AbilityUtils
from ..utils.ability_display_utils import AbilityDisplayUtils
from ..resources import UITexts


class RandomStandHandler(BaseStandHandler):
    """随机替身指令处理器"""

    async def handle_random_stand(self, event: AstrMessageEvent):
        """处理随机替身指令"""
        if not self.check_group_permission(event):
            return

        user_id = event.get_sender_id()
        user_name = event.get_sender_name()

        # 检查冷却时间
        can_proceed, remaining_cooldown = self.cooldown_manager.check_cooldown(user_id)
        if not can_proceed:
            cooldown_message = UITexts.RANDOM_STAND_COOLDOWN.format(
                cooldown_info=self.cooldown_manager.format_cooldown_message(
                    remaining_cooldown
                )
            )
            yield event.chain_result([Comp.Plain(cooldown_message)])
            return

        # 生成随机能力值
        ability_arr = []
        for _ in range(6):
            ability_arr.append(str(random.randint(1, 5)))
        ability_str = ",".join(ability_arr)

        # 生成图片
        image_url = self.api_service.get_image_url(name=user_name, ability=ability_str)

        # 格式化能力值显示
        ability_letters = AbilityUtils.convert_abilities_to_letters(ability_str)
        formatted_abilities = AbilityDisplayUtils.format_abilities_compact(
            ability_letters
        )

        response_text = UITexts.RANDOM_STAND_RESULT.format(
            abilities=formatted_abilities
        )

        async for result in self.send_response(event, response_text, image_url):
            yield result

    async def handle_today_stand(self, event: AstrMessageEvent):
        """处理今日替身指令"""
        if not self.check_group_permission(event):
            return

        user_id = event.get_sender_id()
        user_name = event.get_sender_name()
        ability_arr = []
        current_date = datetime.datetime.now(self.timezone).strftime("%Y%m%d")
        seed = f"{user_id}{current_date}"
        person_random = random.Random(seed)

        for _ in range(6):
            ability_arr.append(str(person_random.randint(1, 5)))
        ability_str = ",".join(ability_arr)

        # 格式化能力值显示
        ability_letters = AbilityUtils.convert_abilities_to_letters(ability_str)
        formatted_abilities = AbilityDisplayUtils.format_abilities_compact(
            ability_letters
        )

        image_url = self.api_service.get_image_url(name=user_name, ability=ability_str)
        response_text = UITexts.TODAY_STAND_RESULT.format(abilities=formatted_abilities)

        async for result in self.send_response(event, response_text, image_url):
            yield result
