# 驗證紀錄

## v0.2.0｜2026-11-05｜僅第一天下午

- 三份第一天 notebook 已在獨立本機 Jupyter kernel 逐格通過，包含前後報告、Skill、真實 MCP／SQLite 與成果 ZIP。
- 自動驗證以模型替身取代付費 API、以測試輸入取代互動 Key 提示；發布 notebook 保留真正模型呼叫及隱藏輸入框，不含測試替身。
- 第一天下午新增 8 項測試通過，涵蓋實際 OpenAI SDK 的模擬 HTTP 工具往返、Skill 原文傳入、MCP 探索與查詢、市場與空值、not_found、錯誤及六次上限。
- 三張狀態圖已以 draw.io 匯出並目視核對；第一天 notebook 的圖放在第一個執行格上方。
- 相對連結、357 頁對照、原始碼同步與 notebook 語法檢查通過；三份成果 ZIP 完整且未含測試 Key。
- 未使用老師的真實 Key 扣款，未在 Colab 網頁端、Antigravity App 或 Windows 演練。模型回答品質及互動輸入仍需老師使用課堂帳號演練。
- 第二天 notebooks、原始流程與課堂內容保持原樣。

逐格紀錄：[第一天下午驗證](examples/day1_validation.json)。維護者執行 `python scripts/run_notebooks.py`，預設只驗證第一天下午。

## v0.1.0 歷史紀錄

教材版本：0.1.0；日期：2026-11-02。

- 學生本機安裝指令 `pip install -e .` 已測，並從教材目錄以外執行成功。
- 本機 Python 3.11，指定版本 LangGraph 1.2.19、langgraph-checkpoint-sqlite 3.1.3、MCP 1.30.0。
- 17 項核心驗收通過：配置與缺漏、SQLite 參數查詢、metadata 篩選、有界補查、真正 MCP stdio、跨程序恢復、冪等內容核對、比較條件、變動門檻、新品證據、審核三分支、草稿失效核准、發送前後中斷。
- 七份 notebook 已在各自獨立 Jupyter kernel 逐格執行通過，包含內嵌教材展開、MCP、跨程序中斷恢復、三種審核分支與成果 ZIP 產生。
- Markdown 相對連結、357 頁涵蓋、Python 語法及七份 notebook 內嵌雜湊同步檢查通過。

本次未在 Google Colab 網頁端、Windows 或 Antigravity App 中實際演練；未執行平台模型研究、真實官網選做、正式寄件或真實排程。Antigravity 操作指引提供可執行步驟，平台 UI 與模型行為須課前確認。

套件安裝在獨立環境完成；notebook 自動驗證使用同一已安裝環境略過重複安裝，仍逐格執行 bootstrap、流程、MCP 與驗收。本機 notebook 成功不代表 Colab 帳號、網路或方案均已驗證。

重新驗證：安裝 requirements-dev.txt，執行 `python -m unittest discover -s tests -v`、`python scripts/check_materials.py`、`python scripts/run_notebooks.py`。最後一項需要允許 Jupyter kernel 使用本機連線。
