# 投影片對照與同步

基準是使用者本次提供的 PDF，共 357 頁；本次沒有同名 PPTX，不推定其他本機 deck 與此版完全相同。頁碼都指 PDF 實際頁碼。來源摘要記在 `course.json`，各段對照機器可讀於 `slide_map.json`。

| PDF 頁碼 | 課堂段落 | 教材位置 | 使用方式 |
|---|---|---|---|
| 1–40 | Agent 概念、交辦與野心 | 講師手冊 D01 | 討論／五欄任務單 |
| 41–94 | 企業案例、權限、Prompt Injection | 講師手冊 D02 | 案例討論與授權表 |
| 95–124 | Prompt、Context、Harness、工具環境 | 講師手冊 D03 | 概念講解後直接進第一份研究 |
| 125–142 | 第一份研究與討論 | L01 | 研究摘要與問題 |
| 143–172 | Skill、SQLite MCP 與討論 | L02A、L02B | 白話規則、模型工具呼叫 |
| 173–221 | RAG、引用與檢索 | L03 | 檢索、對照與未知 |
| 222–261 | Deep Research、分工與停止 | L04 | 研究計畫與補查 |
| 262–306 | 持續工作、中斷恢復與權限 | L05、D04 | 跨程序恢復 Demo |
| 307–350 | 審核、排程、變化追蹤 | L06、D05 | 真實來源快照、詢價草稿與審核分支 |
| 351–357 | 結語與課後上線 | 成果清單、講師手冊 D06 | 成果報告與後續責任 |

## 之後改版的固定做法

1. 主線保留 L01–L06、P01–P09；L02 拆為 A／B。依學員需求取消獨立 L00 setup，不因頁碼移動再重新編號。
2. 更新 PDF 後，先比對每個實作的目標、例子與驗收，不直接把舊頁碼全部平移。
3. 更新 `slide_map.json` 的起訖與標題；確認所有 PDF 頁至少被一段涵蓋。
4. 第一天程式／規則改 `day1/`，教學文字改 `scripts/day1_cells.py`；第二天程式與來源改 `day2/`、教學文字改 `scripts/day2_cells.py`。第一天模擬產品在 `data/`，第二天採購需求與公開片段在 `day2/*.json`。
5. 執行 `python scripts/build_notebooks.py`，產生第一天三份及第二天四份notebooks與 `NOTEBOOK_SOURCES.json`，全部使用明文。
6. 在已安裝套件的環境執行 `python -m unittest discover -s tests -v` 與 `python scripts/check_materials.py`，檢查程式、教學格同步、連結與頁碼。`python scripts/run_notebooks.py`預設用模型替身驗證第一天；第二天執行 `python scripts/run_notebooks.py --day 2 --live-model` 讀取既有.env並實際呼叫模型。
7. 在自己的乾淨 Colab 執行階段與 Antigravity 工作區各演練一次；在 `VERIFICATION.md` 記下實測與未測項目。
8. 更新 `CHANGELOG.md` 及 `course.json` 的版本、來源 SHA-256、日期；上 GitHub 時只包含本教材變更。

狀態圖原始來源是 `scripts/build_day1_diagrams.py` 與 `scripts/build_day2_diagrams.py`，先產生 draw.io 原檔，再以桌面 CLI 匯出 PNG，核對圖與實作一致。七份notebook皆可單獨上傳；圖片需網路。老師要固定版本時，請同時鎖定 Colab 與圖片網址的 commit。
