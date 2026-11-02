# L01｜第一份產品研究

對照 PDF 125–140；建議 25 分鐘。先備：L00。交付：第一份比較表與一項待改善問題。

## 操作步驟

1. 開啟 `data/products.json`。先找出 16 GB／32 GB 各是哪筆，圈出台灣／美國市場。
2. 寫下任務：「比較 DemoBook A 台灣版兩種配置的記憶體、儲存與保固，保留資料日期與來源。」
3. Antigravity：貼 [P01](../prompts/01_first_research.txt)；Colab：上傳並開啟 `01_first_research.ipynb`，先跑安裝與 bootstrap。
4. 本機用 `python -m workshop.cli basic --out runs/l01`；notebook 跑「執行起始流程」格。觀察 fetch → compare，兩個節點共用 rows／comparison。
5. 核對輸出是否只有 `DEMO-TW-016` 與 `DEMO-TW-032`，一配置一列。
6. 對照來源：016 應為 16 GB／512 GB／一年；032 為 32 GB／1 TB／保固待確認。
7. 回答：32 GB 的儲存較大，能否進一步說保固比較好？把缺少的證據寫下來。
8. 保存比較表；Antigravity 另存 `runs/antigravity/01_report.md`，不要覆蓋後續修訂版。
9. 改題為「哪台適合我們業務出差？」。Antigravity 應先詢問企業需求與具體條件；Colab 規則程式不理解任意自然語言，請在 notebook 文字格寫出你還需要問的兩件事。
10. 用 [成果清單](../docs/03_submission.md) 自我驗收。

## 應看到的結果

| ID | 記憶體 | 儲存 | 保固 | 更新日期 |
|---|---|---|---|---|
| DEMO-TW-016 | 16 GB | 512 GB | 1 年 | 2026-10-26 |
| DEMO-TW-032 | 32 GB | 1024 GB | 待確認 | 2026-10-26 |

## 修改練習與驗收

將研究對象只指定型號、不指定市場。模型應詢問市場／配置；不要自選 US。交換同學的報告，驗收正確配置、來源、日期與缺漏四項。沒有保固資料，不等於沒有保固，也不等於不符合任何需求。

下一章：[L02 Skill 與 MCP](02_skill_mcp.md)。
