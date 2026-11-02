# 投影片對照與同步

基準是使用者本次提供的 PDF，共 357 頁；本次沒有同名 PPTX，不推定其他本機 deck 與此版完全相同。頁碼都指 PDF 實際頁碼。來源摘要記在 `course.json`，各段對照機器可讀於 `slide_map.json`。

| PDF 頁碼 | 課堂段落 | 教材位置 | 使用方式 |
|---|---|---|---|
| 1–40 | Agent 概念、交辦與野心 | 講師手冊 D01 | 討論／五欄任務單 |
| 41–94 | 企業案例、權限、Prompt Injection | 講師手冊 D02 | 案例討論與授權表 |
| 95–124 | Prompt、Context、Harness、工具環境 | L00、講師手冊 D03 | 開啟工作區與驗收 |
| 125–142 | 第一份研究與討論 | L01 | 研究摘要與問題 |
| 143–172 | Skill、SQLite MCP 與討論 | L02 | 規則、工具呼叫 |
| 173–221 | RAG、引用與檢索 | L03 | 檢索、對照與未知 |
| 222–261 | Deep Research、分工與停止 | L04 | 研究計畫與補查 |
| 262–306 | 持續工作、中斷恢復與權限 | L05、D04 | 跨程序恢復 Demo |
| 307–350 | 審核、排程、變化追蹤 | L06、D05 | 兩週資料與審核分支 |
| 351–357 | 結語與課後上線 | 成果清單、講師手冊 D06 | 成果報告與後續責任 |

## 之後改版的固定做法

1. 保留 L00–L06 與 P00–P09 的 ID；即使頁碼移動也不改章節 ID。
2. 更新 PDF 後，先比對每個實作的目標、例子與驗收，不直接把舊頁碼全部平移。
3. 更新 `slide_map.json` 的起訖與標題；確認所有 PDF 頁至少被一段涵蓋。
4. 改資料只改 `data/`；改規則只改 `skills/`；改程式只改 `src/workshop/`；改 notebook 教學格只改 `scripts/lesson_cells.json`。
5. 執行 `python scripts/build_notebooks.py`。它重新內嵌目前的程式與資料，並更新 `PAYLOAD.json`。不要直接手改七份 notebook 的 bootstrap。
6. 執行 `python -m unittest discover -s tests -v` 與 `python scripts/check_materials.py`。檢查 notebook 內嵌雜湊、Markdown 連結及頁碼涵蓋。
7. 在自己的乾淨 Colab 執行階段與 Antigravity 工作區各演練一次；在 `VERIFICATION.md` 記下實測與未測項目。
8. 更新 `CHANGELOG.md` 及 `course.json` 的版本、來源 SHA-256、日期；上 GitHub 時只包含本教材變更。

原則：Markdown、資料與 Python 原始碼是單一維護來源；notebook 是可單獨上傳的產物。第一版先用主分支同步，老師要固定某次課程時再以 Git tag 或 commit 鎖定。
