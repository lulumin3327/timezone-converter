from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .exceptions import (
    InvalidTimezoneError,
    InvalidDatetimeError
)


def convert_timezone(
    date_time: datetime,
    source_timezone: str,
    target_timezone: str
) -> datetime:
    """
    將指定日期時間從來源時區轉換至目標時區。
    """

    if not isinstance(date_time, datetime):
        raise InvalidDatetimeError("輸入必須是 datetime 物件")

    if date_time.tzinfo is not None:
        raise InvalidDatetimeError("請輸入不含時區資訊的日期時間")

    try:
        source = ZoneInfo(source_timezone)
        target = ZoneInfo(target_timezone)

    except (ZoneInfoNotFoundError, ValueError) as e:
        raise InvalidTimezoneError(
            f"找不到指定時區：{e}"
        ) from e

    # 將原始時間指定為來源時區
    source_time = date_time.replace(tzinfo=source)

    # 轉換為目標時區
    result = source_time.astimezone(target)

    return result