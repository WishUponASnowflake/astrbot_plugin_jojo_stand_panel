"""
替身数据服务
"""

import datetime
from typing import Optional, Tuple
from astrbot.api import sp

from ..models.stand_models import StandData


class StandDataService:
    """替身数据服务"""

    STANDS_STORAGE_KEY = "jojo_stands"
    AWAKEN_RECORDS_KEY = "jojo_awaken_records"

    def __init__(self, timezone):
        """
        初始化服务

        Args:
            timezone: 时区对象
        """
        self.timezone = timezone

    def save_user_stand(
        self, user_id: str, abilities: str, name: Optional[str] = None
    ) -> None:
        """
        保存用户的替身数据到持久化存储

        Args:
            user_id: 用户ID
            abilities: 能力值字符串，如 "5,5,4,3,2,1"
            name: 替身名字（可选）
        """
        # 获取现有的替身数据
        stands_data = sp.get(self.STANDS_STORAGE_KEY, {})

        # 创建替身数据对象
        stand_data = StandData(
            user_id=user_id,
            abilities=abilities,
            name=name,
            created_at=datetime.datetime.now(self.timezone).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        )

        # 保存用户替身数据
        stands_data[user_id] = stand_data.to_dict()

        # 持久化存储
        sp.put(self.STANDS_STORAGE_KEY, stands_data)

    def get_user_stand(self, user_id: str) -> Optional[StandData]:
        """
        获取用户的替身数据

        Args:
            user_id: 用户ID

        Returns:
            StandData: 替身数据对象，如果不存在返回None
        """
        stands_data = sp.get(self.STANDS_STORAGE_KEY, {})
        user_data = stands_data.get(user_id)

        if user_data is None:
            return None

        return StandData.from_dict(user_id, user_data)

    def save_awaken_record(self, user_id: str) -> None:
        """
        记录用户今日觉醒记录

        Args:
            user_id: 用户ID
        """
        awaken_records = sp.get(self.AWAKEN_RECORDS_KEY, {})
        today = datetime.datetime.now(self.timezone).strftime("%Y-%m-%d")

        if user_id not in awaken_records:
            awaken_records[user_id] = {}

        current_record = awaken_records[user_id].get(today, {"count": 0})
        current_record["count"] += 1
        current_record["last_awaken_time"] = datetime.datetime.now(
            self.timezone
        ).strftime("%Y-%m-%d %H:%M:%S")

        awaken_records[user_id][today] = current_record

        sp.put(self.AWAKEN_RECORDS_KEY, awaken_records)

    def check_awaken_limit(
        self, user_id: str, daily_limit: int = 1
    ) -> Tuple[bool, str]:
        """
        检查用户今日觉醒次数限制

        Args:
            user_id: 用户ID
            daily_limit: 每日限制次数，-1为不限次数，0为禁用

        Returns:
            tuple[bool, str]: (是否可以觉醒, 提示消息)
        """
        # 如果设置为0，禁用觉醒功能
        if daily_limit == 0:
            return False, "❌ 觉醒功能已被管理员禁用！"

        # 如果设置为-1，不限次数
        if daily_limit == -1:
            return True, ""

        awaken_records = sp.get(self.AWAKEN_RECORDS_KEY, {})
        today = datetime.datetime.now(self.timezone).strftime("%Y-%m-%d")

        if user_id not in awaken_records:
            return True, ""

        user_records = awaken_records[user_id]
        today_record = user_records.get(today, {})
        today_count = today_record.get("count", 0)

        if today_count >= daily_limit:
            last_awaken_time = today_record.get("last_awaken_time", "未知时间")
            tomorrow = (
                datetime.datetime.now(self.timezone) + datetime.timedelta(days=1)
            ).strftime("%Y-%m-%d")
            return (
                False,
                f"❌ 今日觉醒次数已用完！\n\n你今天已经重新觉醒过了（{last_awaken_time}）\n每天只能重新觉醒 {daily_limit} 次，请明天（{tomorrow}）再来尝试！",
            )

        return True, ""
