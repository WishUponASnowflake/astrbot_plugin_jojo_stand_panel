"""
自定义替身指令处理器
"""
from astrbot.api.event import AstrMessageEvent
import astrbot.api.message_components as Comp

from .base_handler import BaseStandHandler
from ..utils.ability_utils import AbilityUtils


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
            help_text = """替身面板使用方法：
/替身 <六个能力值> [名字]

能力值格式：
- 使用A-E表示能力等级
- 必须输入恰好6个能力值
- 只支持直接连写格式，如：AAAAEE

示例：
/替身 AABCDE
/替身 ABCDEE 我的替身
/替身 AAAAAA 超级替身"""
            
            yield event.chain_result([Comp.Plain(help_text)])
            return
        
        abilities_input = message_parts[1]
        custom_name = " ".join(message_parts[2:]) if len(message_parts) > 2 else None
        
        # 解析能力值
        ability_str = AbilityUtils.parse_abilities(abilities_input)
        
        if ability_str is None:
            error_text = """❌ 能力值格式错误！

请输入恰好6个能力值（A-E），例如：
✅ AABCDE
✅ ABCDEE
✅ AAAAAA

当前输入无法识别为有效的6个能力值。"""
            
            yield event.chain_result([Comp.Plain(error_text)])
            return
        
        # 如果没有提供自定义名字，使用用户昵称
        if custom_name is None:
            display_name = event.get_sender_name()
        else:
            display_name = custom_name
        
        # 生成替身面板URL
        image_url = self.api_service.get_image_url(name=display_name, ability=ability_str)
        
        # 构建回复消息
        ability_display = abilities_input.upper()
        if custom_name:
            response_text = f"✨ 为 {custom_name} 创建的替身面板（能力：{ability_display}）："
        else:
            response_text = f"✨ 你创建的替身面板（能力：{ability_display}）："
        
        async for result in self.send_response(event, response_text, image_url):
            yield result