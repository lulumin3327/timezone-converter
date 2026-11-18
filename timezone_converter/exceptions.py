class TimezoneError(Exception):
    """時區轉換相關錯誤"""
    pass


class InvalidTimezoneError(TimezoneError):
    """無效的時區名稱"""
    pass


class InvalidDatetimeError(TimezoneError):
    """無效的日期時間"""
    pass