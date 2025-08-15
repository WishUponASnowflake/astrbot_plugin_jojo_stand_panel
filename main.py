from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.platform.message_type import MessageType
from astrbot.api import AstrBotConfig
import astrbot.api.message_components as Comp

import random
import datetime
import pytz
from urllib.parse import urlencode


@register(
    "astrbot_plugin_jojo_stand_panel",
    "Dogend",
    "调用TripleYing的API生成JOJO替身面板图片",
    "1.0.0",
)
class MyPlugin(Star):
    api_server = "https://api.tripleying.com/api/chart"
    time_zone = pytz.timezone("Asia/Shanghai")
    group_white_list = []

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.api_server = config.get("api_server")
        self.group_white_list = config.get("white_list")

    async def initialize(self):
        """插件初始化方法"""

    def get_image_url(self, name: str = None, ability: str = None):
        params = {}
        if name is not None:
            params["name"] = name
        if ability is not None:
            params["ability"] = ability
        if not params:
            return self.api_server
        query_string = urlencode(params)
        return f"{self.api_server}?{query_string}"

    @filter.command("随机替身")
    async def random_stand(self, event: AstrMessageEvent):
        if event.get_message_type() == MessageType.GROUP_MESSAGE:
            if event.get_group_id() not in self.group_white_list:
                logger.info("群聊不在白名单中:" + event.get_group_id())
                return
        user_name = event.get_sender_name()
        image_url = self.get_image_url(name=user_name)
        chain = [
            Comp.Plain("你抽到的替身面板是："),
            Comp.Image.fromURL(image_url),
        ]
        yield event.chain_result(chain)

    @filter.command("今日替身")
    async def today_stand(self, event: AstrMessageEvent):
        if event.get_message_type() == MessageType.GROUP_MESSAGE:
            if event.get_group_id() not in self.group_white_list:
                logger.info("群聊不在白名单中:" + event.get_group_id())
                return
        user_id = event.get_sender_id()
        user_name = event.get_sender_name()
        ability_arr = []
        current_date = datetime.datetime.now(self.time_zone).strftime("%Y%m%d")
        seed = f"{user_id}{current_date}"
        person_random = random.Random(seed)

        for i in range(6):
            ability_arr.append(str(person_random.randint(1, 5)))
        ability_str = ",".join(ability_arr)
        image_url = self.get_image_url(name=user_name, ability=ability_str)
        chain = [
            Comp.Plain("你抽到的替身面板是："),
            Comp.Image.fromURL(image_url),
        ]
        yield event.chain_result(chain)

    async def terminate(self):
        """插件销毁方法"""
