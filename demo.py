
from datetime import datetime

from timezone_converter import (
    convert_timezone,
    get_timezone_info,
    TimezoneError
)


def show_timezone_info():
    """查詢三個時區目前的資訊"""

    timezones = [
        "Asia/Taipei",
        "Europe/Berlin",
        "America/New_York"
    ]

    for timezone_name in timezones:
        try:
            info = get_timezone_info(timezone_name)
        except TimezoneError as e:
            print(f"查詢失敗：{e}")
            continue

        print("=" * 40)
        print(f"時區：{info['timezone']}")
        print(f"當地時間：{info['datetime']}")
        print(f"UTC Offset：{info['utc_offset']}")
        print(f"時區縮寫：{info['timezone_abbr']}")
        print(f"是否使用夏令時間：{info['is_dst']}")


def test_daylight_saving_time():
    """測試德國不同季節的夏令時間"""

    test_dates = [
        datetime(2026, 1, 15, 12, 0),
        datetime(2026, 7, 15, 12, 0),
        datetime(2026, 11, 15, 12, 0)
    ]

    print("\n========== 夏令時間測試 ==========")

    for date in test_dates:
        try:
            info = get_timezone_info("Europe/Berlin", date)
        except TimezoneError as e:
            print(f"測試失敗：{e}")
            continue

        print("=" * 40)
        print(f"日期：{date}")
        print(f"當地時間：{info['datetime']}")
        print(f"UTC Offset：{info['utc_offset']}")
        print(f"時區縮寫：{info['timezone_abbr']}")
        print(f"是否使用夏令時間：{info['is_dst']}")


def main():

    print("==============================")
    print("       Timezone Converter")
    print("==============================")

    try:
        date_input = input(
            "請輸入日期時間 (YYYY-MM-DD HH:MM)："
        )

        date_time = datetime.strptime(
            date_input,
            "%Y-%m-%d %H:%M"
        )

        source = input("來源時區：")
        target = input("目標時區：")

        result = convert_timezone(
            date_time,
            source,
            target
        )

        print("\n========== 轉換結果 ==========")
        print(f"來源時區：{source}")
        print(f"目標時區：{target}")
        print(f"轉換時間：{result.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"UTC Offset：{result.strftime('%z')}")

    except ValueError:
        print("錯誤：日期格式不正確！")

    except TimezoneError as e:
        print(f"轉換失敗：{e}")


if __name__ == "__main__":
    main()
