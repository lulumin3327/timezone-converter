from datetime import datetime

from timezone_converter import (
    convert_timezone,
    TimezoneError
)


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