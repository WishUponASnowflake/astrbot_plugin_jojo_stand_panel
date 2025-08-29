"""
JOJO替身面板插件主入口
"""

from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, StarTools
from astrbot.api import AstrBotConfig, logger

from .utils.service_container import ServiceContainer
from .utils.config_manager import ConfigManager
from .handlers.random_stand_handler import RandomStandHandler
from .handlers.custom_stand_handler import CustomStandHandler
from .handlers.user_stand_handler import UserStandHandler
from .handlers.awaken_stand_handler import AwakenStandHandler


class MyPlugin(Star):
    """JOJO替身面板插件主类"""

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)

        # 初始化配置管理器和服务容器
        self.config_manager = ConfigManager(config)

        # 获取插件数据目录路径
        try:
            data_dir_path = StarTools.get_data_dir()  # 保持Path对象
        except (FileNotFoundError, PermissionError, OSError) as e:
            logger.error(f"❌ 无法获取数据目录，插件无法正常工作：{e}")
            raise
        except Exception as e:
            logger.error(f"❌ 获取数据目录时发生未预期错误：{e}")
            raise

        self.service_container = ServiceContainer(self.config_manager, data_dir_path)

        # 初始化处理器
        self._init_handlers()

    def _init_handlers(self):
        """初始化指令处理器"""
        self.random_handler = RandomStandHandler(self.service_container)
        self.custom_handler = CustomStandHandler(self.service_container)
        self.user_handler = UserStandHandler(self.service_container)
        self.awaken_handler = AwakenStandHandler(self.service_container)

    async def initialize(self):
        """插件初始化方法"""
        # 插件初始化完成
        logger.info("🎆 JOJO替身面板插件初始化完成")

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
