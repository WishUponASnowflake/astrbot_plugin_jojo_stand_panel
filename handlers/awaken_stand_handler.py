"""
觉醒替身指令处理器
"""

import datetime
from astrbot.api.event import AstrMessageEvent
import astrbot.api.message_components as Comp

from .base_handler import BaseStandHandler
from ..utils.ability_utils import AbilityUtils
from ..utils.ability_display_utils import AbilityDisplayUtils
from ..resources import UITexts


class AwakenStandHandler(BaseStandHandler):
    """觉醒替身指令处理器"""

    async def handle_awaken_stand(self, event: AstrMessageEvent):
        """处理觉醒替身指令"""
        if not self.check_group_permission(event):
            return

        # 检查觉醒系统是否启用
        if not self.config_manager.is_awaken_system_enabled():
            yield event.chain_result([Comp.Plain(UITexts.AWAKEN_SYSTEM_DISABLED)])
            return

        user_id = event.get_sender_id()

        # 检查用户是否已经有替身
        existing_stand = self.data_service.get_user_stand(user_id)
        if existing_stand is not None:
            # 用户已有替身，引导到重新觉醒
            yield event.chain_result([Comp.Plain(UITexts.AWAKEN_STAND_EXISTS)])
            return

        # 执行觉醒操作
        async for result in self._perform_awaken(event, user_id, is_reawaken=False):
            yield result

    async def handle_reawaken_stand(self, event: AstrMessageEvent):
        """处理重新觉醒替身指令"""
        if not self.check_group_permission(event):
            return

        # 检查觉醒系统是否启用
        if not self.config_manager.is_awaken_system_enabled():
            yield event.chain_result([Comp.Plain(UITexts.AWAKEN_SYSTEM_DISABLED)])
            return

        user_id = event.get_sender_id()

        # 检查用户是否有现有替身
        existing_stand = self.data_service.get_user_stand(user_id)
        if existing_stand is None:
            # 用户没有替身，直接引导到觉醒替身
            yield event.chain_result([Comp.Plain(UITexts.REAWAKEN_STAND_NO_EXISTING)])
            return

        # 执行觉醒操作
        async for result in self._perform_awaken(event, user_id, is_reawaken=True):
            yield result

    async def _perform_awaken(
        self, event: AstrMessageEvent, user_id: str, is_reawaken: bool = False
    ):
        """
        执行觉醒操作的公共逻辑

        Args:
            event: 消息事件
            user_id: 用户ID
            is_reawaken: 是否为重新觉醒
        """
        # 检查觉醒次数限制（使用配置的限制次数）
        daily_limit = self.config_manager.get_daily_awaken_limit()
        can_awaken, limit_message = self.data_service.check_awaken_limit(
            user_id, daily_limit
        )
        if not can_awaken:
            yield event.chain_result([Comp.Plain(limit_message)])
            return

        # 生成新的随机能力值和名字
        random_abilities = AbilityUtils.generate_random_abilities()
        random_name = self.stand_name_generator.generate_random_stand_name()

        # 保存新的替身数据（覆盖原有的）
        self.data_service.save_user_stand(
            user_id, random_abilities, random_name, "awaken"
        )

        # 记录觉醒次数
        self.data_service.save_awaken_record(user_id)

        # 生成替身面板URL
        image_url = self.api_service.get_image_url(
            name=random_name, ability=random_abilities
        )

        # 构建回复消息
        ability_letters = AbilityUtils.convert_abilities_to_letters(random_abilities)
        formatted_abilities = AbilityDisplayUtils.format_abilities_compact(
            ability_letters
        )

        # 根据配置生成觉醒次数提示
        # 获取用户今日已使用的觉醒次数（包括当前这次）
        current_awaken_count = self.data_service.get_today_awaken_count(user_id)
        limit_hint = self._get_awaken_limit_hint(daily_limit, current_awaken_count)

        if is_reawaken:
            response_text = UITexts.REAWAKEN_STAND_SUCCESS.format(
                stand_name=random_name,
                abilities=formatted_abilities,
                awaken_time=datetime.datetime.now(self.timezone).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                limit_hint=limit_hint,
            )
        else:
            stand_info = f"🌟 替身名：{random_name}\n\n能力值：\n{formatted_abilities}"
            response_text = UITexts.AWAKEN_STAND_SUCCESS.format(
                stand_info=stand_info,
                awaken_time=datetime.datetime.now(self.timezone).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                limit_hint=limit_hint,
            )

        async for result in self.send_response(event, response_text, image_url):
            yield result

    def _get_awaken_limit_hint(self, daily_limit: int, current_count: int = 0) -> str:
        """
        根据配置生成觉醒次数限制提示

        Args:
            daily_limit: 每日觉醒次数限制
            current_count: 当前已使用次数（默认为0）

        Returns:
            str: 觉醒次数提示文字
        """
        if daily_limit == -1:
            # 不限次数
            return "🔄 你可以随时再次觉醒！"
        elif daily_limit == 0:
            # 已禁用（理论上不会到达这里，因为前面已经检查过）
            return "🚫 觉醒系统已被管理员禁用。"
        elif current_count >= daily_limit:
            # 已达到上限
            if daily_limit == 1:
                return "📅 今日觉醒次数已用完，明天可以再次觉醒。"
            else:
                return f"📅 今日觉醒次数已用完（{daily_limit}次），明天可以再次觉醒。"
        else:
            # 未达到上限，显示剩余次数
            remaining = daily_limit - current_count
            return f"🎆 今天还可以再觉醒 {remaining} 次！"
