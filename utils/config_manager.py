"""
配置管理工具类
"""

from typing import List
from astrbot.api import AstrBotConfig


class ConfigManager:
    """配置管理器"""

    # 默认前缀词库
    DEFAULT_PREFIXES = [
        "白金",
        "黄金",
        "钻石",
        "紫金",
        "银色",
        "黑暗",
        "光辉",
        "烈焰",
        "寒冰",
        "雷电",
        "疾风",
        "大地",
        "天空",
        "星辰",
        "月光",
        "太阳",
        "深渊",
        "圣洁",
        "魔法",
        "神秘",
        "极光",
        "暴风",
        "海洋",
        "森林",
        "山峰",
        "火焰",
        "水晶",
        "虹彩",
        "幻影",
        "永恒",
        "血色",
        "翡翠",
        "琥珀",
        "玛瑙",
        "珊瑚",
        "蓝宝石",
        "红宝石",
        "祖母绿",
        "猫眼石",
        "紫水晶",
        "青铜",
        "赤铜",
        "纯白",
        "漆黑",
        "暗红",
        "深蓝",
        "墨绿",
        "金辉",
        "银辉",
        "炽热",
    ]

    # 默认后缀词库
    DEFAULT_SUFFIXES = [
        "之星",
        "使者",
        "战士",
        "守护",
        "刃",
        "翼",
        "之力",
        "王者",
        "骑士",
        "法师",
        "之心",
        "灵魂",
        "命运",
        "审判",
        "制裁",
        "救赎",
        "希望",
        "梦想",
        "传说",
        "神话",
        "奇迹",
        "光芒",
        "影子",
        "风暴",
        "烈火",
        "寒霜",
        "雷鸣",
        "波涛",
        "山岳",
        "天使",
        "恶魔",
        "精灵",
        "血统",
        "耳语",
        "誓言",
        "契约",
        "追缉",
        "羁绊",
        "复仇",
        "复活",
        "逆袭",
        "逆转",
        "启示",
        "预言",
        "天命",
        "审判日",
        "未来",
        "轮回",
        "残影",
        "遗迹",
    ]

    def __init__(self, config: AstrBotConfig):
        """
        初始化配置管理器

        Args:
            config: AstrBot配置对象
        """
        self.config = config

    def get_stand_name_prefixes(self) -> List[str]:
        """
        获取替身名称前缀词库
        支持从字符串配置中解析逗号分隔的前缀

        Returns:
            List[str]: 前缀词库列表
        """
        prefixes_config = self.config.get("stand_name_prefixes", None)

        # 如果是字符串配置，解析逗号分隔的值
        if isinstance(prefixes_config, str):
            if prefixes_config.strip():
                # 按逗号分隔，并去除空格
                prefixes = [
                    prefix.strip()
                    for prefix in prefixes_config.split(",")
                    if prefix.strip()
                ]
                if prefixes:
                    return prefixes
            # 如果是空字符串或解析后为空，使用默认值
            return self.DEFAULT_PREFIXES

        # 如果是列表配置（兼容旧版本）
        elif isinstance(prefixes_config, list):
            if len(prefixes_config) > 0:
                return prefixes_config
            return self.DEFAULT_PREFIXES

        # 其他情况使用默认值
        return self.DEFAULT_PREFIXES

    def get_stand_name_suffixes(self) -> List[str]:
        """
        获取替身名称后缀词库
        支持从字符串配置中解析逗号分隔的后缀

        Returns:
            List[str]: 后缀词库列表
        """
        suffixes_config = self.config.get("stand_name_suffixes", None)

        # 如果是字符串配置，解析逗号分隔的值
        if isinstance(suffixes_config, str):
            if suffixes_config.strip():
                # 按逗号分隔，并去除空格
                suffixes = [
                    suffix.strip()
                    for suffix in suffixes_config.split(",")
                    if suffix.strip()
                ]
                if suffixes:
                    return suffixes
            # 如果是空字符串或解析后为空，使用默认值
            return self.DEFAULT_SUFFIXES

        # 如果是列表配置（兼容旧版本）
        elif isinstance(suffixes_config, list):
            if len(suffixes_config) > 0:
                return suffixes_config
            return self.DEFAULT_SUFFIXES

        # 其他情况使用默认值
        return self.DEFAULT_SUFFIXES

    def get_api_server(self) -> str:
        """
        获取API服务器地址

        Returns:
            str: API服务器地址
        """
        return self.config.get("api_server", "https://api.tripleying.com/api/chart")

    def get_white_list(self) -> List[str]:
        """
        获取群聊白名单

        Returns:
            List[str]: 群聊白名单
        """
        return self.config.get("white_list", [])

    def get_random_cooldown(self) -> int:
        """
        获取随机替身冷却时间

        Returns:
            int: 冷却时间（秒）
        """
        return self.config.get("random_cooldown", 300)

    def get_daily_awaken_limit(self) -> int:
        """
        获取每日觉醒次数限制

        Returns:
            int: 每日觉醒次数限制，-1为不限次数，0为禁用
        """
        return self.config.get("daily_awaken_limit", 1)

    def is_awaken_system_enabled(self) -> bool:
        """
        检查觉醒系统是否启用

        Returns:
            bool: 觉醒系统是否启用
        """
        return self.config.get("enable_awaken_system", True)

    def is_whitelist_enabled(self) -> bool:
        """
        检查白名单是否启用

        Returns:
            bool: 白名单是否启用
        """
        return self.config.get("enable_whitelist", True)

    def is_set_stand_enabled(self) -> bool:
        """
        检查设置替身指令是否启用

        Returns:
            bool: 设置替身指令是否启用
        """
        return self.config.get("enable_set_stand", True)

    def is_view_others_stand_enabled(self) -> bool:
        """
        检查他的替身指令是否启用

        Returns:
            bool: 他的替身指令是否启用
        """
        return self.config.get("enable_view_others_stand", True)
