from datetime import datetime
from zoneinfo import ZoneInfo


def get_timezone_info(timezone_name, dt=None):
    timezone = ZoneInfo(timezone_name)

    if dt is None:
        dt = datetime.now()

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone)
    else:
        dt = dt.astimezone(timezone)

    return {
        "timezone": timezone_name,
        "datetime": dt,
        "utc_offset": dt.strftime("%z"),
        "timezone_abbr": dt.strftime("%Z"),
        "is_dst": bool(dt.dst()),
    }