import io
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from timezone_converter import (
    __version__,
    compare_timezones,
    convert_timezone,
    get_timezone_info,
    is_valid_timezone,
    list_timezones,
    resolve_timezone,
    InvalidDatetimeError,
    InvalidTimezoneError,
)
from timezone_converter.cli import main


class TimezoneCatalogTests(unittest.TestCase):
    def test_readme_timezones_are_included(self):
        catalog = list_timezones()
        self.assertEqual(
            [item["timezone"] for item in catalog],
            [
                "Asia/Taipei",
                "Asia/Tokyo",
                "Asia/Seoul",
                "Europe/Berlin",
                "Europe/London",
                "America/New_York",
                "America/Los_Angeles",
            ],
        )
        self.assertEqual(
            [item["region"] for item in catalog],
            ["台灣", "日本", "韓國", "德國", "英國", "美國紐約", "美國洛杉磯"],
        )

    def test_region_alias_resolves_to_iana_name(self):
        self.assertEqual(resolve_timezone("  台灣  "), "Asia/Taipei")
        self.assertEqual(resolve_timezone("America/Los_Angeles"), "America/Los_Angeles")

    def test_validation(self):
        self.assertTrue(is_valid_timezone("英國"))
        self.assertTrue(is_valid_timezone("UTC"))
        self.assertFalse(is_valid_timezone("UTC+8"))
        self.assertFalse(is_valid_timezone(""))
        self.assertFalse(is_valid_timezone(123))


class ConvertTimezoneTests(unittest.TestCase):
    def test_taipei_to_berlin_standard_time(self):
        result = convert_timezone(
            datetime(2026, 11, 18, 12, 0),
            "Asia/Taipei",
            "Europe/Berlin",
        )
        self.assertEqual(result.strftime("%Y-%m-%d %H:%M:%S %z"), "2026-11-18 05:00:00 +0100")

    def test_taipei_to_berlin_daylight_time(self):
        result = convert_timezone(
            datetime(2026, 7, 15, 12, 0),
            "台灣",
            "德國",
        )
        self.assertEqual(result.strftime("%Y-%m-%d %H:%M:%S %z"), "2026-07-15 06:00:00 +0200")

    def test_rejects_invalid_input(self):
        with self.assertRaises(InvalidDatetimeError):
            convert_timezone("2026-11-18 12:00", "台灣", "日本")
        with self.assertRaises(InvalidDatetimeError):
            convert_timezone(datetime.now().astimezone(), "台灣", "日本")
        with self.assertRaises(InvalidTimezoneError):
            convert_timezone(datetime(2026, 11, 18, 12, 0), "台北", "日本")

    def test_nonexistent_dst_time_is_rejected(self):
        with self.assertRaises(InvalidDatetimeError):
            convert_timezone(datetime(2026, 3, 8, 2, 30), "美國紐約", "台灣")

    def test_ambiguous_dst_fold(self):
        first = convert_timezone(
            datetime(2026, 11, 1, 1, 30),
            "America/New_York",
            "UTC",
            fold=0,
        )
        second = convert_timezone(
            datetime(2026, 11, 1, 1, 30),
            "America/New_York",
            "UTC",
            fold=1,
        )
        self.assertEqual(first.utcoffset(), timedelta(0))
        self.assertEqual(first.hour, 5)
        self.assertEqual(second.hour, 6)
        with self.assertRaises(InvalidDatetimeError):
            convert_timezone(
                datetime(2026, 11, 1, 1, 30),
                "America/New_York",
                "UTC",
                fold=2,
            )


class TimezoneInfoTests(unittest.TestCase):
    def test_current_time_uses_the_requested_zone(self):
        info = get_timezone_info("日本")
        self.assertEqual(info["timezone"], "Asia/Tokyo")
        self.assertEqual(info["region"], "日本")
        self.assertEqual(info["datetime"].tzinfo.key, "Asia/Tokyo")
        self.assertEqual(info["utc_offset"], "+0900")
        self.assertFalse(info["is_dst"])

    def test_berlin_dst_flag(self):
        winter = get_timezone_info("德國", datetime(2026, 1, 15, 12, 0))
        summer = get_timezone_info("德國", datetime(2026, 7, 15, 12, 0))
        self.assertEqual(winter["utc_offset"], "+0100")
        self.assertFalse(winter["is_dst"])
        self.assertEqual(summer["utc_offset"], "+0200")
        self.assertTrue(summer["is_dst"])
        self.assertEqual(summer["utc_offset_hours"], 2)


class CompareTimezoneTests(unittest.TestCase):
    def test_taipei_versus_readme_zones_in_november(self):
        moment = datetime(2026, 11, 18, 12, 0)
        expected = {
            "台灣": 0,
            "日本": -1,
            "韓國": -1,
            "德國": 7,
            "英國": 8,
            "美國紐約": 13,
            "美國洛杉磯": 16,
        }
        for region, hours in expected.items():
            result = compare_timezones("Asia/Taipei", region, moment)
            self.assertEqual(result["hours"], hours)
            self.assertEqual(result["source_utc_offset"], "+0800")

    def test_dst_changes_the_difference(self):
        winter = compare_timezones("台灣", "德國", datetime(2026, 1, 15, 12, 0))
        summer = compare_timezones("台灣", "德國", datetime(2026, 7, 15, 12, 0))
        self.assertEqual(winter["hours"], 7)
        self.assertEqual(summer["hours"], 6)
        self.assertEqual(summer["difference"], timedelta(hours=6))

    def test_aware_datetime_is_the_same_instant(self):
        aware = datetime(2026, 11, 18, 12, 0, tzinfo=ZoneInfo("Asia/Taipei"))
        result = compare_timezones("德國", "英國", aware)
        self.assertEqual(result["source_datetime"].strftime("%H:%M %z"), "05:00 +0100")
        self.assertEqual(result["target_datetime"].strftime("%H:%M %z"), "04:00 +0000")


class PackageTests(unittest.TestCase):
    def test_version(self):
        self.assertEqual(__version__, "0.1.0")

    def test_demo_examples_run(self):
        with redirect_stdout(io.StringIO()) as output:
            main(interactive=False)
        self.assertIn("Asia/Taipei", output.getvalue())
        self.assertIn("夏令時間：是", output.getvalue())


if __name__ == "__main__":
    unittest.main()
