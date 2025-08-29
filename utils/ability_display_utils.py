"""
替身能力值显示工具类
定义JOJO替身面板六个能力的名称和显示格式
"""

from typing import List


class AbilityDisplayUtils:
    """替身能力值显示工具类"""

    # 六个能力名称，按照面板上从上方开始顺时针的顺序
    ABILITY_NAMES = [
        "破坏力",  # 位置1: 上方
        "速度",  # 位置2: 右上
        "射程距离",  # 位置3: 右下
        "持续力",  # 位置4: 下方
        "精密动作性",  # 位置5: 左下
        "成长性",  # 位置6: 左上
    ]

    @classmethod
    def format_abilities_with_names(cls, abilities_letters: str) -> str:
        """
        将能力值字母格式化为带名称的显示格式

        Args:
            abilities_letters: 字母格式的能力值，如 "AABCDE"

        Returns:
            str: 格式化后的能力值显示，如 "破坏力：A，速度：A，射程距离：B..."
        """
        if len(abilities_letters) != 6:
            return "能力值格式错误"

        ability_displays = []
        for i, letter in enumerate(abilities_letters):
            ability_name = cls.ABILITY_NAMES[i]
            ability_displays.append(f"{ability_name}：{letter}")

        return "，".join(ability_displays)

    @classmethod
    def format_abilities_compact(cls, abilities_letters: str) -> str:
        """
        将能力值字母格式化为紧凑的显示格式

        Args:
            abilities_letters: 字母格式的能力值，如 "AABCDE"

        Returns:
            str: 格式化后的能力值显示，每行一个能力
        """
        if len(abilities_letters) != 6:
            return "能力值格式错误"

        ability_displays = []
        for i, letter in enumerate(abilities_letters):
            ability_name = cls.ABILITY_NAMES[i]
            ability_displays.append(f"{ability_name}：{letter}")

        return "\n".join(ability_displays)

    @classmethod
    def get_ability_names(cls) -> List[str]:
        """
        获取所有能力名称列表

        Returns:
            List[str]: 能力名称列表
        """
        return cls.ABILITY_NAMES.copy()

    @classmethod
    def get_ability_name_by_index(cls, index: int) -> str:
        """
        根据索引获取能力名称

        Args:
            index: 能力索引（0-5）

        Returns:
            str: 能力名称，如果索引无效返回"未知能力"
        """
        if 0 <= index < len(cls.ABILITY_NAMES):
            return cls.ABILITY_NAMES[index]
        return "未知能力"
