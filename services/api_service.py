"""
API服务类
"""

from urllib.parse import urlencode
from typing import Optional


class StandAPIService:
    """替身API服务"""

    def __init__(self, api_server: str):
        """
        初始化API服务

        Args:
            api_server: API服务器地址
        """
        self.api_server = api_server

    def get_image_url(
        self, name: Optional[str] = None, ability: Optional[str] = None
    ) -> str:
        """
        生成替身面板图片URL

        Args:
            name: 替身名字
            ability: 能力值字符串

        Returns:
            str: 图片URL
        """
        params = {}
        if name is not None:
            params["name"] = name
        if ability is not None:
            params["ability"] = ability
        if not params:
            return self.api_server
        query_string = urlencode(params)
        return f"{self.api_server}?{query_string}"
