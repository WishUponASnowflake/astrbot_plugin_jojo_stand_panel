"""
JOJO替身面板插件主入口
"""
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import AstrBotConfig
import pytz

from .services.stand_data_service import StandDataService
from .services.api_service import StandAPIService
from .utils.cooldown_manager import CooldownManager
from .utils.config_manager import ConfigManager
from .utils.stand_name_generator import StandNameGenerator
from .handlers.random_stand_handler import RandomStandHandler
from .handlers.custom_stand_handler import CustomStandHandler
from .handlers.user_stand_handler import UserStandHandler
from .handlers.awaken_stand_handler import AwakenStandHandler


@register(
    "astrbot_plugin_jojo_stand_panel",
    "Dogend",
    "调用TripleYing的API生成JOJO替身面板图片",
    "2.0.0",
)
class MyPlugin(Star):
    """JOJO替身面板插件主类"""
    
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        
        # 初始化配置管理器
        self.config_manager = ConfigManager(config)
        
        # 从配置中获取参数
        self.api_server = self.config_manager.get_api_server()
        self.group_white_list = self.config_manager.get_white_list()
        self.random_cooldown = self.config_manager.get_random_cooldown()
        self.timezone = pytz.timezone("Asia/Shanghai")
        
        # 初始化服务
        self.data_service = StandDataService(self.timezone)
        self.api_service = StandAPIService(self.api_server)
        self.cooldown_manager = CooldownManager(self.random_cooldown)
        self.stand_name_generator = StandNameGenerator(self.config_manager)
        
        # 初始化处理器
        self._init_handlers()
    
    def _init_handlers(self):
        """初始化指令处理器"""
        handler_args = (
            self.data_service,
            self.api_service, 
            self.cooldown_manager,
            self.group_white_list,
            self.timezone,
            self.stand_name_generator,
            self.config_manager
        )
        
        self.random_handler = RandomStandHandler(*handler_args)
        self.custom_handler = CustomStandHandler(*handler_args)
        self.user_handler = UserStandHandler(*handler_args)
        self.awaken_handler = AwakenStandHandler(*handler_args)

    async def initialize(self):
        """插件初始化方法"""
        pass
    
    # ==================== 指令注册 ====================
    
    @filter.command("随机替身")
    async def random_stand(self, event: AstrMessageEvent):
        """随机替身指令"""
        async for result in self.random_handler.handle_random_stand(event):
            yield result
    
    @filter.command("今日替身")
    async def today_stand(self, event: AstrMessageEvent):
        """今日替身指令"""
        async for result in self.random_handler.handle_today_stand(event):
            yield result
    
    @filter.command("替身面板")
    async def create_stand(self, event: AstrMessageEvent):
        """创建自定义替身指令"""
        async for result in self.custom_handler.handle_create_stand(event):
            yield result
    
    @filter.command("设置替身")
    async def set_stand(self, event: AstrMessageEvent):
        """设置替身指令"""
        async for result in self.user_handler.handle_set_stand(event):
            yield result
    
    @filter.command("我的替身")
    async def my_stand(self, event: AstrMessageEvent):
        """我的替身指令"""
        async for result in self.user_handler.handle_my_stand(event):
            yield result
    
    @filter.command("他的替身")
    async def view_stand(self, event: AstrMessageEvent):
        """查看他人替身指令"""
        async for result in self.user_handler.handle_view_stand(event):
            yield result
    
    @filter.command("觉醒替身")
    async def awaken_stand(self, event: AstrMessageEvent):
        """觉醒替身指令"""
        async for result in self.awaken_handler.handle_awaken_stand(event):
            yield result
    
    @filter.command("重新觉醒")
    async def confirm_awaken_stand(self, event: AstrMessageEvent):
        """重新觉醒替身指令"""
        async for result in self.awaken_handler.handle_reawaken_stand(event):
            yield result

    async def terminate(self):
        """插件销毁方法"""
        pass