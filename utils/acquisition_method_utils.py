"""
替身获得方式显示工具类
"""


class AcquisitionMethodUtils:
    """替身获得方式工具类"""

    # 获得方式映射
    METHOD_DISPLAY = {
        "manual": "🔧 手动设置",
        "awaken": "🌟 觉醒系统",
        "unknown": "❓ 未知方式",
    }

    @classmethod
    def get_method_display(cls, acquisition_method: str) -> str:
        """
        获取获得方式的显示文本

        Args:
            acquisition_method: 获得方式代码

        Returns:
            str: 获得方式的显示文本
        """
        return cls.METHOD_DISPLAY.get(acquisition_method, "❓ 未知方式")

    @classmethod
    def get_method_description(cls, acquisition_method: str) -> str:
        """
        获取获得方式的详细描述

        Args:
            acquisition_method: 获得方式代码

        Returns:
            str: 获得方式的详细描述
        """
        descriptions = {
            "manual": "通过 /设置替身 指令自定义创建",
            "awaken": "通过觉醒系统随机生成",
            "unknown": "获得方式未知（可能是旧版本数据）",
        }
        return descriptions.get(acquisition_method, "获得方式未知")
