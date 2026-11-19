# 時區轉換工具（Timezone Converter）

一個使用 Python 開發的時區轉換工具套件，可將指定日期與時間從來源時區轉換為目標時區，並提供時區資訊與時間差查詢功能。

本專案使用 Python 內建的 `datetime` 與 `zoneinfo` 模組處理時區轉換，採用 IANA 時區資料庫中的時區名稱，例如 `Asia/Taipei`、`Europe/Berlin`。下表的地區名稱也可以直接當作參數，例如 `台灣`。

## 功能特色

- **時區轉換**：將指定日期與時間從來源時區轉換為目標時區。
- **時區資訊查詢**：取得指定時區的時間、UTC 時差、縮寫，以及是否處於夏令時間。
- **時區差異比較**：比較兩個時區在同一瞬間相差幾小時。正數代表來源時區比較快。
- **內建時區清單**：提供下方範例表的七個時區，可用地區名稱或 IANA 名稱查詢。
- **時區名稱驗證**：檢查輸入的時區名稱是否有效。
- **錯誤處理**：無效時區、不合法的日期時間，以及夏令時間切換時不存在的鐘面時間，都會得到明確錯誤。

## 系統需求

- Python 3.9 或更新版本。
- 依賴 `tzdata`。用 pip 安裝本套件時會一併安裝，Windows 也能取得 IANA 時區資料。

## 安裝方式

```bash
pip install oo2026-timezone-0811aiesha
```

在專案目錄中以可編輯模式安裝，方便改程式後直接測試：

```bash
pip install -e .
```

## 使用範例

```python
from datetime import datetime
from timezone_converter import (
    convert_timezone,
    compare_timezones,
    get_timezone_info,
    is_valid_timezone,
    list_timezones,
)

date_time = datetime(2026, 11, 18, 12, 0)

# 地區名稱與 IANA 名稱都可以
result = convert_timezone(date_time, "台灣", "Europe/Berlin")
print(result)  # 2026-11-18 05:00:00+01:00

# 台灣在這一天比德國快 7 小時；七月德國實施夏令時間，時差會變成 6 小時
difference = compare_timezones("台灣", "德國", date_time)
print(difference["hours"])  # 7.0

info = get_timezone_info("美國紐約")
print(info["datetime"], info["utc_offset"], info["is_dst"])

print(is_valid_timezone("Asia/Taipei"))  # True
print(is_valid_timezone("UTC+8"))        # False
print(list_timezones())
```

夏令時間結束時，同一個鐘面時間可能出現兩次。`fold=0` 是第一次，`fold=1` 是第二次。落在夏令時間開始空檔、實際上不存在的時間會丟出 `InvalidDatetimeError`。

## 時區名稱範例

| 地區 | IANA 時區名稱 | 說明 |
|---|---|---|
| 台灣 | Asia/Taipei | 全年 UTC+8 |
| 日本 | Asia/Tokyo | 全年 UTC+9 |
| 韓國 | Asia/Seoul | 全年 UTC+9 |
| 德國 | Europe/Berlin | 有夏令時間 |
| 英國 | Europe/London | 有夏令時間 |
| 美國紐約 | America/New_York | 有夏令時間 |
| 美國洛杉磯 | America/Los_Angeles | 有夏令時間 |

這些地區以外，也可以傳入其他 IANA 名稱，例如 `UTC` 或 `Australia/Sydney`。`UTC+8` 這類寫法不是 IANA 名稱，套件不會接受。

## 本機示範

專案根目錄的 `demo.py` 會列出七個時區的現在時間、與台灣的時差，以及德國的夏令時間。終端機有互動輸入時，接著可以自己轉一筆時間。

```bash
python demo.py
```

安裝套件之後也可以執行：

```bash
python -m timezone_converter
```

## 測試

```bash
python -m unittest discover -s tests
```

## 專案結構

```text
timezone-converter/
├── pyproject.toml
├── README.md
├── LICENSE
├── demo.py
├── tests/
│   └── test_timezone_converter.py
└── timezone_converter/
    ├── __init__.py
    ├── __main__.py
    ├── cli.py
    ├── converter.py
    ├── timezone_info.py
    ├── timezones.py
    └── exceptions.py
```

## 使用注意事項

1. 請使用 IANA 標準時區名稱，或上方表格的地區名稱。
2. 部分地區會因夏令時間而改變 UTC 時差，同一組城市在不同日期的時差不一定相同。
3. `convert_timezone` 收到的時間不要自己附上 `tzinfo`。要比較一個已經帶有時區的瞬間，請用 `compare_timezones` 或 `get_timezone_info`。
4. 若只複製原始碼、沒有用 pip 安裝，請另外執行 `pip install tzdata`。

## 發布到 PyPI

課程作業上傳到 PyPI 時，套件做到下面這樣即可：公開函式與錯誤處理、`pyproject.toml` 的名稱與版本、README、MIT 授權，以及 `tzdata` 依賴。不需要做成網站或支援全部城市的中文別名。

套件名稱是 `oo2026-timezone-0811aiesha`。PyPI 上的名稱不能跟別人重複，上傳前請維持這個名稱。

```bash
python -m pip install build twine
python -m build
python -m twine check dist/*
python -m twine upload --repository testpypi dist/*
```

先傳到 TestPyPI 確認安裝沒問題，再上傳到正式 PyPI。若這版已經傳上去，之後改程式要先把 `pyproject.toml` 與 `timezone_converter/__init__.py` 的版本號一起加一號，不能重複上傳同一個版本。

## 開發目的

本專案為 Python 模組與 PyPI 套件發布課程作業，目的是練習 Python 模組化設計、例外處理、套件建置及 PyPI 發布流程。
