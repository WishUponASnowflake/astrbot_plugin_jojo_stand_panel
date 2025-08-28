"""
能力值处理工具类
"""

import random
from typing import Optional


class AbilityUtils:
    """能力值处理工具类"""

    # 能力值映射
    ABILITY_TO_NUMBER = {"A": "5", "B": "4", "C": "3", "D": "2", "E": "1"}
    NUMBER_TO_ABILITY = {"5": "A", "4": "B", "3": "C", "2": "D", "1": "E"}

    @classmethod
    def parse_abilities(cls, abilities_str: str) -> Optional[str]:
        """
        将用户输入的能力值（A-E）转换为数字（5-1）
        只支持 "AAAAAA" 格式，不支持逗号分隔

        Args:
            abilities_str: 用户输入的能力字符串，如 "AABCDE"

        Returns:
            str: 转换后的数字字符串，如 "5,5,4,3,2,1"，如果格式错误返回None
        """
        # 移除所有空格，转换为大写
        abilities_clean = "".join(
            c.upper() for c in abilities_str if c.upper() in "ABCDE"
        )

        # 检查是否有效（必须恰好6个字符）
        if len(abilities_clean) != 6:
            return None

        # 转换 A-E 到 5-1
        converted = [cls.ABILITY_TO_NUMBER[c] for c in abilities_clean]

        return ",".join(converted)

    @classmethod
    def convert_abilities_to_letters(cls, abilities: str) -> str:
        """
        将数字能力值转换为字母格式

        Args:
            abilities: 数字格式能力值，如 "5,4,3,2,1,5"

        Returns:
            str: 字母格式能力值，如 "ABCDE"
        """
        ability_nums = abilities.split(",")
        return "".join([cls.NUMBER_TO_ABILITY[num] for num in ability_nums])

    @classmethod
    def generate_random_abilities(cls) -> str:
        """
        生成随机的替身能力值

        Returns:
            str: 随机能力值字符串，如 "5,4,3,2,1,5"
        """
        abilities = []
        for _ in range(6):
            abilities.append(str(random.randint(1, 5)))
        return ",".join(abilities)
