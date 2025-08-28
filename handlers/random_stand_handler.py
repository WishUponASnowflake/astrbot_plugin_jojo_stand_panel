"""
随机替身指令处理器
"""
import random
import datetime
from astrbot.api.event import AstrMessageEvent
import astrbot.api.message_components as Comp

from .base_handler import BaseStandHandler


class RandomStandHandler(BaseStandHandler):
    """随机替身指令处理器"""
    
    async def handle_random_stand(self, event: AstrMessageEvent):
        """处理随机替身指令"""
        if not self.check_group_permission(event):
            return

        user_id = event.get_sender_id()
        can_use, remaining_cooldown = self.cooldown_manager.check_cooldown(user_id)
        
        if can_use:
            user_name = event.get_sender_name()
            image_url = self.api_service.get_image_url(name=user_name)
            async for result in self.send_response(event, "你抽到的替身面板是：", image_url):
                yield result
        else:
            cooldown_message = self.cooldown_manager.format_cooldown_message(remaining_cooldown)
            yield event.chain_result([Comp.Plain(cooldown_message)])
    
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

        for i in range(6):
            ability_arr.append(str(person_random.randint(1, 5)))
        ability_str = ",".join(ability_arr)
        image_url = self.api_service.get_image_url(name=user_name, ability=ability_str)
        
        async for result in self.send_response(event, "你抽到的替身面板是：", image_url):
            yield result