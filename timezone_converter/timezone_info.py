from __future__ import annotations

from datetime import datetime, timedelta

from .exceptions import InvalidDatetimeError
from .timezones import attach_timezone, load_timezone, region_for_timezone


def get_timezone_info(
    timezone_name: str,
    dt: datetime | None = None,
    fold: int | None = None,
) -> dict:
    """
    取得指定時區的時間、UTC 時差與是否為夏令時間。

    dt 省略時回傳該時區的現在時間。若 dt 不含時區，會把它視為該時區的
    鐘面時間；若已含時區，則換算成該時區的同一瞬間。
    """
    timezone = load_timezone(timezone_name)

    if dt is None:
        if fold is not None:
            raise InvalidDatetimeError("未指定日期時間時不能設定 fold")
        current = datetime.now(timezone)
    elif not isinstance(dt, datetime):
        raise InvalidDatetimeError("輸入必須是 datetime 物件")
    elif dt.tzinfo is None:
        current = attach_timezone(dt, timezone_name, fold)
    else:
        if fold is not None:
            raise InvalidDatetimeError("已含時區的日期時間不能再設定 fold")
        current = dt.astimezone(timezone)

    offset = current.utcoffset() or timedelta(0)
    return {
        "timezone": timezone.key,
        "region": region_for_timezone(timezone.key),
        "datetime": current,
        "utc_offset": current.strftime("%z"),
        "utc_offset_hours": offset.total_seconds() / 3600,
        "timezone_abbr": current.strftime("%Z"),
        "is_dst": bool(current.dst()),
    }
