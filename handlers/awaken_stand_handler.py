"""
觉醒替身指令处理器
"""

import datetime
from astrbot.api.event import AstrMessageEvent
import astrbot.api.message_components as Comp

from .base_handler import BaseStandHandler
from ..utils.ability_utils import AbilityUtils
from ..utils.ability_display_utils import AbilityDisplayUtils


class AwakenStandHandler(BaseStandHandler):
    """觉醒替身指令处理器"""

    async def handle_awaken_stand(self, event: AstrMessageEvent):
        """处理觉醒替身指令"""
        if not self.check_group_permission(event):
            return

        # 检查觉醒系统是否启用
        if not self.config_manager.is_awaken_system_enabled():
            yield event.chain_result([Comp.Plain("❌ 觉醒系统已被管理员禁用！")])
            return

        user_id = event.get_sender_id()

        # 检查用户是否已经有替身
        existing_stand = self.data_service.get_user_stand(user_id)
        if existing_stand is not None:
            # 用户已经有替身，询问是否要重新觉醒
            confirm_text = f"""⚠️ 你已经拥有替身了！

📊 当前替身信息：
🏷️ 替身名：{existing_stand.name or "未命名"}

💪 能力值：
{AbilityDisplayUtils.format_abilities_compact(AbilityUtils.convert_abilities_to_letters(existing_stand.abilities))}

⏰ 设置时间：{existing_stand.created_at or "未知"}

🚨 如果重新觉醒将会覆盖当前替身，确定要继续吗？
👁️ 发送 /我的替身 来查看当前替身
🔄 发送 /重新觉醒 来确认重新觉醒
🔧 发送 /设置替身 可以自定义替身能力值"""

            yield event.chain_result([Comp.Plain(confirm_text)])
            return

        # 生成随机能力值和名字
        random_abilities = AbilityUtils.generate_random_abilities()
        random_name = self.stand_name_generator.generate_random_stand_name()

        # 保存用户替身数据
        self.data_service.save_user_stand(
            user_id, random_abilities, random_name, "awaken"
        )

        # 生成替身面板URL
        image_url = self.api_service.get_image_url(
            name=random_name, ability=random_abilities
        )

        # 构建回复消息
        ability_letters = AbilityUtils.convert_abilities_to_letters(random_abilities)
        formatted_abilities = AbilityDisplayUtils.format_abilities_compact(
            ability_letters
        )
        response_text = f"""🌟 恭喜！你觉醒了替身！

🏷️ 替身名：{random_name}

💪 能力值：
{formatted_abilities}

⏰ 觉醒时间：{datetime.datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")}

👁️ 发送 /我的替身 查看你的替身面板
🔄 发送 /重新觉醒 来重新觉醒你的替身
🔧 发送 /设置替身 可以自定义替身能力值"""

        async for result in self.send_response(event, response_text, image_url):
            yield result

    async def handle_reawaken_stand(self, event: AstrMessageEvent):
        """处理重新觉醒替身指令"""
        if not self.check_group_permission(event):
            return

        # 检查觉醒系统是否启用
        if not self.config_manager.is_awaken_system_enabled():
            yield event.chain_result([Comp.Plain("❌ 觉醒系统已被管理员禁用！")])
            return

        user_id = event.get_sender_id()

        # 检查用户是否有现有替身
        existing_stand = self.data_service.get_user_stand(user_id)
        if existing_stand is None:
            # 用户没有替身，直接引导到觉醒替身
            yield event.chain_result(
                [Comp.Plain("🌱 你还没有替身，请使用 /觉醒替身 来获得你的第一个替身！")]
            )
            return

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
        current_awaken_count = self.data_service.get_today_awaken_count(user_id) + 1
        limit_hint = self._get_awaken_limit_hint(daily_limit, current_awaken_count)

        response_text = f"""🔥 替身重新觉醒成功！

🆕 新替身名：{random_name}

🔋 新能力值：
{formatted_abilities}

⏰ 觉醒时间：{datetime.datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")}

🎆 你的替身已经进化，获得了全新的力量！
{limit_hint}"""

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
