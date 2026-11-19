from __future__ import annotations

import sys
from datetime import datetime

from .converter import compare_timezones, convert_timezone
from .exceptions import TimezoneError
from .timezone_info import get_timezone_info
from .timezones import list_timezones


def _format_hours(hours: float) -> str:
    amount = abs(hours)
    if amount == int(amount):
        number = str(int(amount))
    else:
        number = f"{amount:g}"
    if hours > 0:
        return f"快 {number} 小時"
    if hours < 0:
        return f"慢 {number} 小時"
    return "時間相同"


def _print_info(info: dict) -> None:
    region = info["region"] or "其他"
    current = info["datetime"]
    dst = "是" if info["is_dst"] else "否"
    print(
        f"{region}  {info['timezone']}  "
        f"{current.strftime('%Y-%m-%d %H:%M:%S')}  "
        f"{info['utc_offset']}  {info['timezone_abbr']}  "
        f"夏令時間：{dst}"
    )


def show_timezone_info() -> None:
    """列出內建時區目前的時間與時差。"""
    print("========== 內建時區現在時間 ==========")
    for item in list_timezones():
        try:
            info = get_timezone_info(item["region"])
        except TimezoneError as error:
            print(f"查詢失敗：{error}")
            continue
        _print_info(info)


def show_comparisons() -> None:
    """以固定時間比較台灣與其他內建時區。"""
    moment = datetime(2026, 11, 18, 12, 0)
    print("\n========== 時區比對：台灣 2026-11-18 12:00 ==========")
    for item in list_timezones():
        try:
            result = compare_timezones("台灣", item["region"], moment)
        except TimezoneError as error:
            print(f"比對失敗：{error}")
            continue
        target = result["target_datetime"]
        if result["hours"] == 0:
            relation = "與台灣時間相同"
        else:
            relation = f"台灣{_format_hours(result['hours'])}"
        print(
            f"{item['region']}  {result['target_timezone']}  "
            f"{target.strftime('%Y-%m-%d %H:%M:%S')}  "
            f"{result['target_utc_offset']}  "
            f"（{relation}）"
        )


def test_daylight_saving_time() -> None:
    """測試德國不同季節的夏令時間。"""
    test_dates = [
        datetime(2026, 1, 15, 12, 0),
        datetime(2026, 7, 15, 12, 0),
        datetime(2026, 11, 15, 12, 0),
    ]

    print("\n========== 夏令時間測試：德國 ==========")
    for date in test_dates:
        try:
            info = get_timezone_info("Europe/Berlin", date)
        except TimezoneError as error:
            print(f"測試失敗：{error}")
            continue
        dst = "是" if info["is_dst"] else "否"
        print(
            f"{date.strftime('%Y-%m-%d %H:%M')}  "
            f"{info['utc_offset']}  {info['timezone_abbr']}  "
            f"夏令時間：{dst}"
        )


def run_interactive() -> None:
    """從鍵盤讀取一筆時間並轉換時區。"""
    print("\n========== 互動轉換 ==========")
    print("可輸入 IANA 名稱或地區名稱，例如 Asia/Taipei 或 台灣。")
    try:
        date_input = input("請輸入日期時間 (YYYY-MM-DD HH:MM)：")
        date_time = datetime.strptime(date_input, "%Y-%m-%d %H:%M")
        source = input("來源時區：")
        target = input("目標時區：")
    except EOFError:
        print()
        return
    except ValueError:
        print("錯誤：日期格式不正確。")
        return

    try:
        result = convert_timezone(date_time, source, target)
        comparison = compare_timezones(source, target, date_time)
    except TimezoneError as error:
        print(f"轉換失敗：{error}")
        return

    print("\n========== 轉換結果 ==========")
    print(f"來源時區：{comparison['source_timezone']}")
    print(f"目標時區：{comparison['target_timezone']}")
    print(f"轉換時間：{result.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"UTC Offset：{result.strftime('%z')}")
    print(f"來源比目標：{_format_hours(comparison['hours'])}")


def main(interactive: bool | None = None) -> None:
    print("==============================")
    print("       Timezone Converter")
    print("==============================")
    show_timezone_info()
    show_comparisons()
    test_daylight_saving_time()

    if interactive is None:
        interactive = sys.stdin.isatty()
    if interactive:
        run_interactive()
