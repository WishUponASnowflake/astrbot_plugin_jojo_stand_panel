"""
替身数据模型
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class StandData:
    """替身数据模型"""

    user_id: str
    abilities: str  # 能力值字符串，如 "5,4,3,2,1,5"
    name: Optional[str] = None  # 替身名字
    created_at: Optional[str] = None  # 创建时间
    acquisition_method: Optional[str] = (
        None  # 获得方式："manual"(设置替身)、"awaken"(觉醒系统)、"unknown"(未知)
    )

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "abilities": self.abilities,
            "name": self.name,
            "created_at": self.created_at,
            "acquisition_method": self.acquisition_method,
        }

    @classmethod
    def from_dict(cls, user_id: str, data: dict) -> "StandData":
        """从字典创建实例"""
        return cls(
            user_id=user_id,
            abilities=data.get("abilities", ""),
            name=data.get("name"),
            created_at=data.get("created_at"),
            acquisition_method=data.get(
                "acquisition_method", "unknown"
            ),  # 旧数据默认为未知
        )


@dataclass
class AwakenRecord:
    """觉醒记录模型"""

    user_id: str
    date: str  # YYYY-MM-DD 格式
    count: int = 0
    last_awaken_time: Optional[str] = None

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {"count": self.count, "last_awaken_time": self.last_awaken_time}

    @classmethod
    def from_dict(cls, user_id: str, date: str, data: dict) -> "AwakenRecord":
        """从字典创建实例"""
        return cls(
            user_id=user_id,
            date=date,
            count=data.get("count", 0),
            last_awaken_time=data.get("last_awaken_time"),
        )
