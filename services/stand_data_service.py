"""
替身数据服务
"""

import json
import os
import datetime
from typing import Optional, Tuple
from pathlib import Path

from ..models.stand_models import StandData


class StandDataService:
    """替身数据服务"""

    STANDS_STORAGE_KEY = "jojo_stands"
    AWAKEN_RECORDS_KEY = "jojo_awaken_records"

    def __init__(self, timezone, data_dir_path: Optional[str] = None):
        """
        初始化服务

        Args:
            timezone: 时区对象
            data_dir_path: 数据目录路径（可选）
        """
        self.timezone = timezone
        self.data_dir_path = data_dir_path

        # 如果提供了数据目录路径，创建必要的目录
        if self.data_dir_path:
            self._ensure_data_dirs()

    def _ensure_data_dirs(self):
        """确保数据目录存在"""
        if not self.data_dir_path:
            return

        data_path = Path(self.data_dir_path)
        stands_dir = data_path / "stands"
        awaken_dir = data_path / "awaken_records"

        stands_dir.mkdir(parents=True, exist_ok=True)
        awaken_dir.mkdir(parents=True, exist_ok=True)

    def _get_user_stand_file(self, user_id: str) -> Optional[str]:
        """获取用户替身数据文件路径"""
        if not self.data_dir_path:
            return None
        return os.path.join(self.data_dir_path, "stands", f"{user_id}.json")

    def _get_awaken_records_file(self, user_id: Optional[str] = None) -> Optional[str]:
        """
        获取觉醒记录文件路径

        新的存储策略：每个用户的觉醒记录单独存储
        路径格式：awaken_records/user_{user_id}.json

        Args:
            user_id: 用户ID，如果为None则返回旧的按月份格式（仅用于兼容）
        """
        if not self.data_dir_path:
            return None

        if user_id:
            # 新的按用户分片存储
            return os.path.join(
                self.data_dir_path, "awaken_records", f"user_{user_id}.json"
            )
        else:
            # 旧的按月份存储（仅用于迁移兼容）
            today = datetime.datetime.now(self.timezone).strftime("%Y-%m")
            return os.path.join(self.data_dir_path, "awaken_records", f"{today}.json")

    def save_user_stand(
        self,
        user_id: str,
        abilities: str,
        name: Optional[str] = None,
        acquisition_method: str = "unknown",
    ) -> None:
        """
        保存用户的替身数据到持久化存储

        Args:
            user_id: 用户ID
            abilities: 能力值字符串，如 "5,5,4,3,2,1"
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

        # 如果有数据目录，使用文件存储；否则使用sp存储
        if self.data_dir_path:
            file_path = self._get_user_stand_file(user_id)
            if file_path:  # 确保 file_path 不是 None
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(stand_data.to_dict(), f, ensure_ascii=False, indent=2)
                except Exception:
                    # 如果文件操作失败，回退到sp存储
                    self._save_user_stand_sp(user_id, stand_data)
            else:
                self._save_user_stand_sp(user_id, stand_data)
        else:
            self._save_user_stand_sp(user_id, stand_data)

    def _save_user_stand_sp(self, user_id: str, stand_data: StandData) -> None:
        """使用sp存储用户替身数据"""
        from astrbot.api import sp

        stands_data = sp.get(self.STANDS_STORAGE_KEY, {})
        stands_data[user_id] = stand_data.to_dict()
        sp.put(self.STANDS_STORAGE_KEY, stands_data)

    def get_user_stand(self, user_id: str) -> Optional[StandData]:
        """
        获取用户的替身数据

        Args:
            user_id: 用户ID

        Returns:
            StandData: 替身数据对象，如果不存在返回None
        """
        # 如果有数据目录，先尝试从文件读取
        if self.data_dir_path:
            file_path = self._get_user_stand_file(user_id)
            if file_path and os.path.exists(file_path):  # 确保 file_path 不是 None
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        user_data = json.load(f)
                    return StandData.from_dict(user_id, user_data)
                except Exception:
                    # 如果文件读取失败，回退到sp存储
                    pass

        # 使用sp存储作为备选
        return self._get_user_stand_sp(user_id)

    def _get_user_stand_sp(self, user_id: str) -> Optional[StandData]:
        """从 sp 获取用户替身数据"""
        from astrbot.api import sp

        stands_data = sp.get(self.STANDS_STORAGE_KEY, {})
        user_data = stands_data.get(user_id)

        if user_data is None:
            return None

        return StandData.from_dict(user_id, user_data)

    def save_awaken_record(self, user_id: str) -> None:
        """
        记录用户今日觉醒记录

        优化后的存储策略：每个用户的觉醒记录单独存储
        提高读写效率，减少文件锁定冲突

        Args:
            user_id: 用户ID
        """
        today = datetime.datetime.now(self.timezone).strftime("%Y-%m-%d")

        # 如果有数据目录，使用文件存储；否则使用sp存储
        if self.data_dir_path:
            file_path = self._get_awaken_records_file(user_id)
            if file_path:  # 确保 file_path 不是 None
                try:
                    # 读取用户的觉醒记录（只包含该用户的数据）
                    user_awaken_records = {}
                    if os.path.exists(file_path):
                        with open(file_path, "r", encoding="utf-8") as f:
                            user_awaken_records = json.load(f)

                    # 更新今日记录
                    current_record = user_awaken_records.get(today, {"count": 0})
                    current_record["count"] += 1
                    current_record["last_awaken_time"] = datetime.datetime.now(
                        self.timezone
                    ).strftime("%Y-%m-%d %H:%M:%S")

                    user_awaken_records[today] = current_record

                    # 保存到用户专属文件
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(user_awaken_records, f, ensure_ascii=False, indent=2)

                except Exception:
                    # 如果文件操作失败，回退到sp存储
                    self._save_awaken_record_sp(user_id)
            else:
                self._save_awaken_record_sp(user_id)
        else:
            self._save_awaken_record_sp(user_id)

    def _save_awaken_record_sp(self, user_id: str) -> None:
        """使用sp存储觉醒记录"""
        from astrbot.api import sp

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

        优化后只需读取单个用户的觉醒记录文件，提高效率

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

        # 先尝试从用户专属文件读取
        user_awaken_records = {}
        if self.data_dir_path:
            file_path = self._get_awaken_records_file(user_id)
            if file_path and os.path.exists(file_path):  # 确保 file_path 不是 None
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        user_awaken_records = json.load(f)
                except Exception:
                    # 文件读取失败，尝试从旧数据格式或sp获取
                    return self._check_awaken_limit_fallback(
                        user_id, daily_limit, today
                    )
        else:
            # 没有数据目录，使用sp存储
            return self._check_awaken_limit_fallback(user_id, daily_limit, today)

        # 检查今日记录
        today_record = user_awaken_records.get(today, {})
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

    def _check_awaken_limit_fallback(
        self, user_id: str, daily_limit: int, today: str
    ) -> Tuple[bool, str]:
        """
        备选方案：从旧数据格式或sp获取觉醒记录
        """
        awaken_records = {}

        # 先尝试从旧的按月份文件读取
        if self.data_dir_path:
            old_file_path = self._get_awaken_records_file()  # 不传user_id，获取旧格式
            if old_file_path and os.path.exists(old_file_path):
                try:
                    with open(old_file_path, "r", encoding="utf-8") as f:
                        awaken_records = json.load(f)
                except Exception:
                    pass

        # 如果还是没有数据，使用sp
        if not awaken_records:
            awaken_records = self._get_awaken_records_sp()

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

    def _get_awaken_records_sp(self) -> dict:
        """从 sp 获取觉醒记录"""
        from astrbot.api import sp

        return sp.get(self.AWAKEN_RECORDS_KEY, {})

    def get_today_awaken_count(self, user_id: str) -> int:
        """
        获取用户今日已使用的觉醒次数

        Args:
            user_id: 用户ID

        Returns:
            int: 今日已使用的觉醒次数
        """
        today = datetime.datetime.now(self.timezone).strftime("%Y-%m-%d")

        # 先尝试从用户专属文件读取
        if self.data_dir_path:
            file_path = self._get_awaken_records_file(user_id)
            if file_path and os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        user_awaken_records = json.load(f)
                    today_record = user_awaken_records.get(today, {})
                    return today_record.get("count", 0)
                except Exception:
                    pass

        # 备选方案：从旧数据格式或sp获取
        awaken_records = {}

        # 先尝试从旧的按月份文件读取
        if self.data_dir_path:
            old_file_path = self._get_awaken_records_file()  # 不传user_id，获取旧格式
            if old_file_path and os.path.exists(old_file_path):
                try:
                    with open(old_file_path, "r", encoding="utf-8") as f:
                        awaken_records = json.load(f)
                except Exception:
                    pass

        # 如果还是没有数据，使用sp
        if not awaken_records:
            awaken_records = self._get_awaken_records_sp()

        if user_id not in awaken_records:
            return 0

        user_records = awaken_records[user_id]
        today_record = user_records.get(today, {})
        return today_record.get("count", 0)

    # ==================== 数据迁移相关方法 ====================

    def _get_migration_status_file(self) -> Optional[str]:
        """获取迁移状态文件路径"""
        if not self.data_dir_path:
            return None
        return os.path.join(self.data_dir_path, "migration_status.json")

    def _is_migration_completed(self) -> bool:
        """检查数据迁移是否已完成"""
        if not self.data_dir_path:
            return True  # 没有数据目录，不需要迁移

        status_file = self._get_migration_status_file()
        if not status_file or not os.path.exists(status_file):
            return False

        try:
            with open(status_file, "r", encoding="utf-8") as f:
                status = json.load(f)
            return status.get("migration_completed", False)
        except Exception:
            return False

    def _mark_migration_completed(self) -> None:
        """标记数据迁移已完成"""
        if not self.data_dir_path:
            return

        status_file = self._get_migration_status_file()
        if not status_file:
            return

        try:
            status = {
                "migration_completed": True,
                "migration_date": datetime.datetime.now(self.timezone).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "version": "1.0",
            }
            with open(status_file, "w", encoding="utf-8") as f:
                json.dump(status, f, ensure_ascii=False, indent=2)
        except Exception as e:
            # 记录错误但不影响主功能
            print(f"警告：无法保存迁移状态：{e}")

    def migrate_data_from_sp(self) -> dict:
        """
        从 SP 存储迁移数据到文件系统

        Returns:
            dict: 迁移结果统计
        """
        if not self.data_dir_path:
            return {
                "success": False,
                "message": "没有数据目录，跳过迁移",
                "stands_migrated": 0,
                "awaken_records_migrated": 0,
            }

        # 检查是否已经迁移过
        if self._is_migration_completed():
            return {
                "success": True,
                "message": "数据迁移已完成，跳过重复迁移",
                "stands_migrated": 0,
                "awaken_records_migrated": 0,
            }

        result = {
            "success": True,
            "message": "数据迁移成功",
            "stands_migrated": 0,
            "awaken_records_migrated": 0,
            "errors": [],
        }

        try:
            # 迁移替身数据
            stands_count = self._migrate_stands_data()
            result["stands_migrated"] = stands_count

            # 迁移觉醒记录
            awaken_count = self._migrate_awaken_records()
            result["awaken_records_migrated"] = awaken_count

            # 标记迁移完成
            self._mark_migration_completed()

            if stands_count > 0 or awaken_count > 0:
                result["message"] = (
                    f"数据迁移成功：迁移了 {stands_count} 个替身数据和 {awaken_count} 个觉醒记录"
                )
            else:
                result["message"] = "没有发现需要迁移的数据"

        except Exception as e:
            result["success"] = False
            result["message"] = f"数据迁移失败：{str(e)}"
            result["errors"].append(str(e))

        return result

    def _migrate_stands_data(self) -> int:
        """迁移替身数据从 SP 到文件系统"""
        from astrbot.api import sp

        stands_data = sp.get(self.STANDS_STORAGE_KEY, {})
        if not stands_data:
            return 0

        migrated_count = 0

        for user_id, user_data in stands_data.items():
            try:
                # 检查文件是否已存在，避免覆盖
                file_path = self._get_user_stand_file(user_id)
                if file_path and os.path.exists(file_path):
                    continue  # 文件已存在，跳过

                # 保存到文件
                if file_path:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(user_data, f, ensure_ascii=False, indent=2)
                    migrated_count += 1

            except Exception as e:
                print(f"警告：迁移用户 {user_id} 的替身数据失败：{e}")
                continue

        return migrated_count

    def _migrate_awaken_records(self) -> int:
        """
        迁移觉醒记录从 SP 到文件系统

        优化后的迁移策略：直接迁移到按用户分片的新格式
        避免创建大文件，提高性能
        """
        from astrbot.api import sp

        awaken_records = sp.get(self.AWAKEN_RECORDS_KEY, {})
        if not awaken_records:
            return 0

        migrated_count = 0

        # 直接按用户迁移到新的分片格式
        for user_id, user_records in awaken_records.items():
            try:
                # 获取用户专属觉醒记录文件路径
                file_path = self._get_awaken_records_file(user_id)
                if not file_path:
                    continue

                # 检查文件是否已存在
                existing_records = {}
                if os.path.exists(file_path):
                    with open(file_path, "r", encoding="utf-8") as f:
                        existing_records = json.load(f)

                # 合并记录（不覆盖已有数据）
                records_added = 0
                for date_str, record in user_records.items():
                    if date_str not in existing_records:
                        existing_records[date_str] = record
                        records_added += 1

                # 如果有新记录，保存到文件
                if records_added > 0:
                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(existing_records, f, ensure_ascii=False, indent=2)
                    migrated_count += records_added

            except Exception as e:
                print(f"警告：迁移用户 {user_id} 的觉醒记录失败：{e}")
                continue

        return migrated_count
