from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from .exceptions import InvalidDatetimeError
from .timezones import attach_timezone, load_timezone


def convert_timezone(
    date_time: datetime,
    source_timezone: str,
    target_timezone: str,
    fold: int | None = None,
) -> datetime:
    """
    將指定日期時間從來源時區轉換至目標時區。

    date_time 必須是不含時區資訊的 datetime。source_timezone 與
    target_timezone 可以是 IANA 名稱（例如 Asia/Taipei），也可以是
    內建地區名稱（例如 台灣）。
    """
    if not isinstance(date_time, datetime):
        raise InvalidDatetimeError("輸入必須是 datetime 物件")

    source_time = attach_timezone(date_time, source_timezone, fold)
    target = load_timezone(target_timezone)
    return source_time.astimezone(target)


def compare_timezones(
    source_timezone: str,
    target_timezone: str,
    date_time: datetime | None = None,
    fold: int | None = None,
) -> dict:
    """
    比較兩個時區在同一瞬間的 UTC 時差。

    date_time 省略時，以現在這個瞬間比較。若傳入不含時區的 datetime，
    會把它視為來源時區的鐘面時間。hours 為正，代表來源時區比目標時區快。
    """
    source = load_timezone(source_timezone)
    target = load_timezone(target_timezone)

    if date_time is None:
        if fold is not None:
            raise InvalidDatetimeError("未指定日期時間時不能設定 fold")
        source_time = datetime.now(ZoneInfo("UTC")).astimezone(source)
    elif not isinstance(date_time, datetime):
        raise InvalidDatetimeError("輸入必須是 datetime 物件")
    elif date_time.tzinfo is None:
        source_time = attach_timezone(date_time, source_timezone, fold)
    else:
        if fold is not None:
            raise InvalidDatetimeError("已含時區的日期時間不能再設定 fold")
        source_time = date_time.astimezone(source)

    target_time = source_time.astimezone(target)
    source_offset = source_time.utcoffset()
    target_offset = target_time.utcoffset()
    difference = source_offset - target_offset

    return {
        "source_timezone": source.key,
        "target_timezone": target.key,
        "source_datetime": source_time,
        "target_datetime": target_time,
        "source_utc_offset": source_time.strftime("%z"),
        "target_utc_offset": target_time.strftime("%z"),
        "difference": difference,
        "hours": difference.total_seconds() / 3600,
    }
