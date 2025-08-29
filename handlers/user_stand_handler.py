"""
本文档由AI生成

用户替身管理指令处理器
"""

from typing import Optional, Tuple
from astrbot.api.event import AstrMessageEvent
import astrbot.api.message_components as Comp

from .base_handler import BaseStandHandler
from ..utils.ability_utils import AbilityUtils
from ..utils.ability_display_utils import AbilityDisplayUtils
from ..utils.acquisition_method_utils import AcquisitionMethodUtils
from ..resources import UITexts


class UserStandHandler(BaseStandHandler):
    """用户替身管理指令处理器"""

    async def handle_set_stand(self, event: AstrMessageEvent):
        """处理设置替身指令"""
        if not self.check_group_permission(event):
            return

        # 检查设置替身指令是否启用
        if not self.config_manager.is_set_stand_enabled():
            yield event.chain_result([Comp.Plain(UITexts.SET_STAND_DISABLED)])
            return

        # 解析命令参数
        message_parts = event.message_str.strip().split()

        if len(message_parts) < 2:
            # 显示帮助信息
            yield event.chain_result([Comp.Plain(UITexts.SET_STAND_HELP)])
            return

        abilities_input = message_parts[1]
        custom_name = " ".join(message_parts[2:]) if len(message_parts) > 2 else None

        # 解析能力值
        ability_str = AbilityUtils.parse_abilities(abilities_input)

        if ability_str is None:
            yield event.chain_result([Comp.Plain(UITexts.SET_STAND_INVALID_ABILITIES)])
            return

        # 保存用户替身数据
        user_id = event.get_sender_id()
        self.data_service.save_user_stand(user_id, ability_str, custom_name, "manual")

        # 构建确认消息
        ability_display = abilities_input.upper()
        if custom_name:
            success_text = UITexts.SET_STAND_SUCCESS_WITH_NAME.format(
                stand_name=custom_name, abilities=ability_display
            )
        else:
            success_text = UITexts.SET_STAND_SUCCESS_WITHOUT_NAME.format(
                abilities=ability_display
            )

        yield event.chain_result([Comp.Plain(success_text)])

    async def handle_my_stand(self, event: AstrMessageEvent):
        """处理我的替身指令"""
        if not self.check_group_permission(event):
            return

        user_id = event.get_sender_id()
        user_name = event.get_sender_name()

        # 获取用户替身数据
        stand_data = self.data_service.get_user_stand(user_id)

        if stand_data is None:
            # 用户还没有设置替身
            yield event.chain_result([Comp.Plain(UITexts.MY_STAND_NO_STAND)])
            return

        # 确定显示名字
        if stand_data.name:
            display_name = stand_data.name
        else:
            display_name = user_name

        # 生成替身面板URL
        image_url = self.api_service.get_image_url(
            name=display_name, ability=stand_data.abilities
        )

        # 将数字能力值转换回字母显示
        ability_letters = AbilityUtils.convert_abilities_to_letters(
            stand_data.abilities
        )

        # 格式化能力值显示（带能力名称）
        formatted_abilities = AbilityDisplayUtils.format_abilities_compact(
            ability_letters
        )

        # 获取获得方式显示
        acquisition_display = AcquisitionMethodUtils.get_method_display(
            stand_data.acquisition_method or "unknown"
        )

        # 构建回复消息
        if stand_data.name:
            response_text = UITexts.MY_STAND_WITH_NAME.format(
                stand_name=stand_data.name,
                abilities=formatted_abilities,
                acquisition_method=acquisition_display,
                created_at=stand_data.created_at,
            )
        else:
            response_text = UITexts.MY_STAND_WITHOUT_NAME.format(
                abilities=formatted_abilities,
                acquisition_method=acquisition_display,
                created_at=stand_data.created_at,
            )

        async for result in self.send_response(event, response_text, image_url):
            yield result

    def _parse_target_user(
        self, event: AstrMessageEvent
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        解析目标用户的逻辑

        Args:
            event: 消息事件

        Returns:
            tuple[Optional[str], Optional[str]]: (用户ID, 用户名称)
        """
        target_user_id = None
        target_user_name = None

        # 获取消息中的所有组件
        messages = event.get_messages()

        # 查找At组件
        for msg_component in messages:
            if isinstance(msg_component, Comp.At):
                # 找到了@某人
                target_user_id = str(msg_component.qq)
                target_user_name = (
                    getattr(msg_component, "name", None) or f"用户{target_user_id}"
                )
                break

        # 如果没有找到At组件，检查是否有文本参数
        if target_user_id is None:
            message_parts = event.message_str.strip().split()
            if len(message_parts) >= 2:
                # 尝试将第二个参数作为用户ID
                potential_user_id = message_parts[1]
                if potential_user_id.isdigit():
                    target_user_id = potential_user_id
                    target_user_name = f"用户{target_user_id}"

        return target_user_id, target_user_name

    async def handle_view_stand(self, event: AstrMessageEvent):
        """处理查看他人替身指令"""
        if not self.check_group_permission(event):
            return

        # 检查他的替身指令是否启用
        if not self.config_manager.is_view_others_stand_enabled():
            yield event.chain_result([Comp.Plain(UITexts.VIEW_STAND_DISABLED)])
            return

        # 解析目标用户
        target_user_id, target_user_name = self._parse_target_user(event)

        # 如果没有找到目标用户，显示帮助信息
        if target_user_id is None:
            yield event.chain_result([Comp.Plain(UITexts.VIEW_STAND_HELP)])
            return

        # 获取目标用户的替身数据
        stand_data = self.data_service.get_user_stand(target_user_id)

        if stand_data is None:
            # 目标用户还没有设置替身
            no_stand_text = UITexts.VIEW_STAND_NO_STAND.format(
                user_name=target_user_name
            )
            yield event.chain_result([Comp.Plain(no_stand_text)])
            return

        # 确定显示名字
        if stand_data.name:
            display_name = stand_data.name
        else:
            display_name = target_user_name

        # 生成替身面板URL
        image_url = self.api_service.get_image_url(
            name=display_name, ability=stand_data.abilities
        )

        # 将数字能力值转换回字母显示
        ability_letters = AbilityUtils.convert_abilities_to_letters(
            stand_data.abilities
        )

        # 格式化能力值显示（带能力名称）
        formatted_abilities = AbilityDisplayUtils.format_abilities_compact(
            ability_letters
        )

        # 获取获得方式显示
        acquisition_display = AcquisitionMethodUtils.get_method_display(
            stand_data.acquisition_method or "unknown"
        )

        # 构建回复消息
        if stand_data.name:
            response_text = UITexts.VIEW_STAND_WITH_NAME.format(
                user_name=target_user_name,
                stand_name=stand_data.name,
                abilities=formatted_abilities,
                acquisition_method=acquisition_display,
                created_at=stand_data.created_at,
            )
        else:
            response_text = UITexts.VIEW_STAND_WITHOUT_NAME.format(
                user_name=target_user_name,
                abilities=formatted_abilities,
                acquisition_method=acquisition_display,
                created_at=stand_data.created_at,
            )

        async for result in self.send_response(event, response_text, image_url):
            yield result
