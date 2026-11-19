from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .exceptions import InvalidDatetimeError, InvalidTimezoneError

# README 時區名稱範例。地區名稱可直接當成時區參數使用。
_COMMON_TIMEZONES: tuple[tuple[str, str], ...] = (
    ("台灣", "Asia/Taipei"),
    ("日本", "Asia/Tokyo"),
    ("韓國", "Asia/Seoul"),
    ("德國", "Europe/Berlin"),
    ("英國", "Europe/London"),
    ("美國紐約", "America/New_York"),
    ("美國洛杉磯", "America/Los_Angeles"),
)

_REGION_TO_TIMEZONE = dict(_COMMON_TIMEZONES)
_TIMEZONE_TO_REGION = {timezone: region for region, timezone in _COMMON_TIMEZONES}


def list_timezones() -> list[dict[str, str]]:
    """回傳套件內建的時區清單。"""
    return [
        {"region": region, "timezone": timezone}
        for region, timezone in _COMMON_TIMEZONES
    ]


def region_for_timezone(iana_name: str) -> str | None:
    """若是內建時區，回傳地區名稱。"""
    return _TIMEZONE_TO_REGION.get(iana_name)


def load_timezone(timezone_name: str) -> ZoneInfo:
    """接受 IANA 名稱或內建地區名稱，回傳 ZoneInfo。"""
    if not isinstance(timezone_name, str):
        raise InvalidTimezoneError("時區名稱必須是字串")

    cleaned = timezone_name.strip()
    if not cleaned:
        raise InvalidTimezoneError("時區名稱不可為空")

    iana_name = _REGION_TO_TIMEZONE.get(cleaned, cleaned)
    try:
        return ZoneInfo(iana_name)
    except (ZoneInfoNotFoundError, ValueError) as error:
        raise InvalidTimezoneError(f"找不到指定時區：{timezone_name}") from error


def resolve_timezone(timezone_name: str) -> str:
    """把地區名稱或 IANA 名稱轉成標準 IANA 時區名稱。"""
    return load_timezone(timezone_name).key


def is_valid_timezone(timezone_name: str) -> bool:
    """檢查時區名稱是否可用。無效時回傳 False，不丟出例外。"""
    try:
        load_timezone(timezone_name)
    except InvalidTimezoneError:
        return False
    return True


def attach_timezone(
    date_time: datetime,
    timezone_name: str,
    fold: int | None = None,
) -> datetime:
    """
    把不含時區的日期時間標成指定時區。

    夏令時間結束、同一個鐘面時間出現兩次時，fold 0 是第一次，
    fold 1 是第二次。fold 為 None 時沿用 date_time.fold。
    落在夏令時間開始空檔、實際上不存在的時間會丟出 InvalidDatetimeError。
    """
    if not isinstance(date_time, datetime):
        raise InvalidDatetimeError("輸入必須是 datetime 物件")

    if date_time.tzinfo is not None:
        raise InvalidDatetimeError("請輸入不含時區資訊的日期時間")

    chosen_fold = _choose_fold(date_time, fold)
    timezone = load_timezone(timezone_name)
    aware = date_time.replace(tzinfo=timezone, fold=chosen_fold)
    normalized = aware.astimezone(ZoneInfo("UTC")).astimezone(timezone)
    if normalized.replace(tzinfo=None) != date_time.replace(tzinfo=None):
        raise InvalidDatetimeError(
            f"{date_time} 在時區 {timezone.key} 不存在，"
            "可能落在夏令時間開始的空檔"
        )
    return aware


def _choose_fold(date_time: datetime, fold: int | None) -> int:
    if fold is None:
        return date_time.fold
    if type(fold) is not int or fold not in (0, 1):
        raise InvalidDatetimeError("fold 只能是 0 或 1")
    return fold
