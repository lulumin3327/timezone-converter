# 時區轉換工具（Timezone Converter）

一個使用 Python 開發的時區轉換工具套件，可將指定日期與時間從來源時區轉換為目標時區，並提供時區資訊與時間差查詢功能。

本專案使用 Python 內建的 `datetime` 與 `zoneinfo` 模組處理時區轉換，採用 IANA 時區資料庫中的時區名稱，例如 `Asia/Taipei`、`Europe/Berlin`。

## 功能特色

- **時區轉換**：將指定日期與時間從來源時區轉換為目標時區。
- **時區資訊查詢**：取得指定時區的目前時間與 UTC 時差。
- **時區差異比較**：比較兩個時區之間的時間差。
- **時區名稱驗證**：檢查輸入的時區名稱是否有效。
- **錯誤處理**：針對無效時區及不合法的日期時間提供明確錯誤訊息。

## 系統需求

- Python 3.9 或更新版本。
- Windows 使用者可能需要額外安裝 `tzdata`，以確保系統能取得時區資料。

## 安裝方式

使用 pip 安裝：

```bash
pip install oo2026-timezone-yourid
```

請將 `yourid` 替換成發布套件時使用的識別名稱。

## 使用範例

```python
from datetime import datetime
from timezone_converter import convert_timezone

# 設定日期與時間
date_time = datetime(2026, 11, 18, 12, 0)

# 將台灣時間轉換為德國時間
result = convert_timezone(
    date_time,
    "Asia/Taipei",
    "Europe/Berlin"
)

print(result)
```

## 時區名稱範例

| 地區 | IANA 時區名稱 |
|---|---|
| 台灣 | Asia/Taipei |
| 日本 | Asia/Tokyo |
| 韓國 | Asia/Seoul |
| 德國 | Europe/Berlin |
| 英國 | Europe/London |
| 美國紐約 | America/New_York |
| 美國洛杉磯 | America/Los_Angeles |

## 專案結構

```text
timezone-converter/
├── pyproject.toml
├── README.md
├── LICENSE
├── demo.py
└── timezone_converter/
    ├── __init__.py
    ├── converter.py
    └── exceptions.py
```

## 使用注意事項

1. 請使用 IANA 標準時區名稱，例如 `Asia/Taipei`，而非單純輸入 `UTC+8`。
2. 部分地區會因夏令時間（DST）而產生時差變化。
3. Windows 使用者若遇到找不到時區資料的錯誤，可以安裝 `tzdata`。

## 開發目的

本專案為 Python 模組與 PyPI 套件發布課程作業，目的是練習 Python 模組化設計、例外處理、套件建置及 PyPI 發布流程。