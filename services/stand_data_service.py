"""
替身数据服务
"""

import json
import datetime
from typing import Optional, Tuple, Union
from pathlib import Path
from astrbot.api import logger

from ..models.stand_models import StandData


class StandDataService:
    """替身数据服务"""

    def __init__(self, timezone, data_dir_path: Union[str, Path]):
        """
        初始化服务

        Args:
            timezone: 时区对象
            data_dir_path: 数据目录路径（必需）
        """
        self.timezone = timezone
        # 转换为Path对象
        self.data_dir_path = Path(data_dir_path)

        # 创建必要的目录
        self._ensure_data_dirs()

    def _ensure_data_dirs(self):
        """确保数据目录存在"""
        try:
            stands_dir = self.data_dir_path / "stands"
            awaken_dir = self.data_dir_path / "awaken_records"

            stands_dir.mkdir(parents=True, exist_ok=True)
            awaken_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            logger.error(f"❌ 无法创建数据目录: {e}")
            raise

    def _get_user_stand_file(self, user_id: str) -> Path:
        """获取用户替身数据文件路径"""
        return self.data_dir_path / "stands" / f"{user_id}.json"

    def _get_awaken_records_file(self, user_id: str) -> Path:
        """
        获取觉醒记录文件路径

        Args:
            user_id: 用户ID
        """
        return self.data_dir_path / "awaken_records" / f"user_{user_id}.json"

    def save_user_stand(
        self,
        user_id: str,
        abilities: str,
        name: Optional[str] = None,
        acquisition_method: str = "unknown",
    ) -> None:
        """
        保存用户的替身数据到文件存储

        Args:
            user_id: 用户ID
            abilities: 能力值字符串，如 "AAAAAA"
            name: 替身名字（可选）
            acquisition_method: 获得方式："manual"(手动设置)、"awaken"(觉醒系统)、"unknown"(未知)
        """
        # 创建替身数据对象
        stand_data = StandData(
            user_id=user_id,
            abilities=abilities,
            name=name,
            created_at=datetime.datetime.now(self.timezone).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            acquisition_method=acquisition_method,
        )

        # 保存到文件
        file_path = self._get_user_stand_file(user_id)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(stand_data.to_dict(), f, ensure_ascii=False, indent=2)
        except (IOError, PermissionError, OSError) as e:
            logger.error(f"❌ 文件保存失败: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON序列化失败: {e}")
            raise

    def get_user_stand(self, user_id: str) -> Optional[StandData]:
        """
        获取用户的替身数据

        Args:
            user_id: 用户ID

        Returns:
            StandData: 替身数据对象，如果不存在返回None
        """
        file_path = self._get_user_stand_file(user_id)

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                user_data = json.load(f)
            return StandData.from_dict(user_id, user_data)
        except (IOError, PermissionError, OSError) as e:
            logger.error(f"❌ 读取替身数据失败: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON解析失败: {e}")
            return None

    def save_awaken_record(self, user_id: str) -> None:
        """
        记录用户今日觉醒记录

        Args:
            user_id: 用户ID
        """
        today = datetime.datetime.now(self.timezone).strftime("%Y-%m-%d")

        file_path = self._get_awaken_records_file(user_id)

        try:
            # 读取用户的觉醒记录
            user_awaken_records = {}
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    user_awaken_records = json.load(f)

            # 更新今日记录
            current_record = user_awaken_records.get(today, {"count": 0})
            current_record["count"] += 1
            current_record["last_awaken_time"] = datetime.datetime.now(
                self.timezone
            ).strftime("%Y-%m-%d %H:%M:%S")

            user_awaken_records[today] = current_record

            # 保存到文件
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(user_awaken_records, f, ensure_ascii=False, indent=2)

        except (IOError, PermissionError, OSError) as e:
            logger.error(f"❌ 保存觉醒记录失败: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"❌ JSON序列化失败: {e}")
            raise

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

        today = datetime.datetime.now(self.timezone).strftime("%Y-%m-%d")
        file_path = self._get_awaken_records_file(user_id)

        # 读取用户觉醒记录
        user_awaken_records = {}
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    user_awaken_records = json.load(f)
            except (IOError, PermissionError, OSError, json.JSONDecodeError) as e:
                logger.error(f"❌ 读取觉醒记录失败: {e}")
                # 读取失败时拒绝觉醒，保证限制功能的健壮性
                return False, "❌ 系统错误，暂时无法觉醒，请稍后再试"

        # 检查今日记录
        today_record = user_awaken_records.get(today, {})
        today_count = today_record.get("count", 0)

        if today_count >= daily_limit:
            last_awaken_time = today_record.get("last_awaken_time", "未知时间")
            tomorrow = (
                datetime.datetime.now(self.timezone) + datetime.timedelta(days=1)
            ).strftime("%Y-%m-%d")
            # 使用资源文件中的文本
            from ..resources import UITexts

            error_message = UITexts.AWAKEN_LIMIT_EXCEEDED.format(
                last_awaken_time=last_awaken_time,
                daily_limit=daily_limit,
                tomorrow=tomorrow,
            )
            return (False, error_message)

        return True, ""

    def get_today_awaken_count(self, user_id: str) -> int:
        """
        获取用户今日已使用的觉醒次数

        Args:
            user_id: 用户ID

        Returns:
            int: 今日已使用的觉醒次数
        """
        today = datetime.datetime.now(self.timezone).strftime("%Y-%m-%d")
        file_path = self._get_awaken_records_file(user_id)

        if not file_path.exists():
            return 0

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                user_awaken_records = json.load(f)
            today_record = user_awaken_records.get(today, {})
            return today_record.get("count", 0)
        except (IOError, PermissionError, OSError, json.JSONDecodeError) as e:
            logger.error(f"❌ 读取觉醒记录失败: {e}")
            return 0
