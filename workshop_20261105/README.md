# AI Agent 逐步教材

以老師提供的 357 頁 PDF 為基準。這次先完成第一天下午（PDF 95–172），第二天課堂內容保持原樣，後續再同步；原始投影片未變更、未複製進公開教材。

**同學直接從 [第一天下午課堂入口](day1/README.md) 開始，不用另外做第 0 步 setup。** 每份 Colab 都有上方狀態圖及完整白話步驟，老師提供 Key，學員練習改需求、請 AI 修改、檢查結果。

## 第一天下午

|順序|學生步驟|Colab|交付|
|---|---|---|---|
|L01 第一份研究|[操作步驟](labs/01_first_research.md)|[開始研究](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/01_first_research.ipynb)|前後問題、報告、工具紀錄|
|L02A Skill|[操作步驟](labs/02_skill_mcp.md)|[修改研究規則](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/02_skill_mcp.ipynb)|白話 Skill、前後報告|
|L02B MCP|[操作步驟](labs/02_skill_mcp.md)|[查詢 SQLite](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/02b_company_database.ipynb)|MCP 紀錄、正常／查不到的回答|

資料是模擬產品；模型 API、LangGraph、MCP 與 SQLite 會實際執行。Key 在執行時輸入框貼上，不寫入教材。這三份 notebook 自帶明文程式與資料，可以下載後單獨上傳 Colab；依序播放收起的準備格即可。每章只修改指定中文問題或規則，最後下載成果 ZIP。

## 第二天：待後續改寫

以下保留 既有固定規則教學內容，**不呼叫模型 API**。本次未修改第二天 notebooks 與課堂內容。

|ID|PDF 頁碼|學生步驟|Colab|
|---|---|---|---|
|L03|173–221|[RAG 與引用](labs/03_rag.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/03_rag.ipynb)|
|L04|222–261|[有界研究與交接](labs/04_research_loop.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/04_research_loop.ipynb)|
|L05|262–306|[中斷恢復](labs/05_recovery.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/05_recovery.ipynb)|
|L06|307–350|[人工審核與追蹤](labs/06_review_monitor.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/06_review_monitor.ipynb)|

## 講師與維護

- [Antigravity 操作](docs/01_antigravity.md)／[可複製任務指令](prompts/)
- [講師手冊](docs/02_instructor.md)／[學生成果](docs/03_submission.md)／[排錯](docs/04_troubleshooting.md)
- [投影片同步](docs/05_slide_sync.md)／[GitHub 更新](docs/06_github.md)／[技術參考](docs/07_references.md)
- [版本紀錄](CHANGELOG.md)／[驗證範圍](VERIFICATION.md)

第一天的程式與 Skill 在 `day1/`；Colab 教學文字在 `scripts/day1_cells.py`。更新後執行 `python scripts/build_notebooks.py`，再跑 `python scripts/check_materials.py`，確保原始碼與教學同步。第二天程式仍在 `src/workshop/`，教學文字在 `scripts/lesson_cells.json`。

基準 SHA-256 與日期見 `course.json`，PDF 對照見 `slide_map.json`。Colab 與狀態圖連結使用本儲存庫 `main`；複製到其他儲存庫時須同步更新連結。
