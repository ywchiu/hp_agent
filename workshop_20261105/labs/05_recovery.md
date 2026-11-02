# L05｜研究到一半中斷，從原進度接續

對照 PDF 262–299，重點 Demo 為 283–299；建議 30 分鐘。交付：同 Thread 的狀態、執行紀錄、唯一取證筆數與報告。

## 逐步操作

1. Antigravity 貼 [P06](../prompts/06_recovery.txt)；Colab 開 `05_recovery.ipynb`。使用獨立輸出目錄，例如 `runs/l05_01`。
2. 固定 Thread `research-demo-01`。讀 `data/recovery.json`，知道三家都是模擬資料。
3. 本機執行：

```sh
python -m workshop.cli recover-start --out runs/l05_01 --thread research-demo-01
```

4. 應收到 `DEMO_CRASH_AFTER_ASUS_WRITE` 且程序以非零結束。這是在 ASUS 取證資料寫入後、節點完成前故意拋出的例外；不會破壞作業系統。
5. 打開 `state.json`。results 只有 Dell／Lenovo，next 是 ASUS。打開 `execution.jsonl`，應為 Dell、Lenovo、ASUS 各一次。
6. 查看 `operations.sqlite`：三筆工具效果已存在，其中 ASUS 的效果早於 checkpoint 完成。記錄兩邊狀態差異。
7. **開啟另一個 Python 程序**，保留相同目錄與 Thread：

```sh
python -m workshop.cli recover-resume --out runs/l05_01 --thread research-demo-01
```

8. 查看完整 log：Dell、Lenovo、ASUS、ASUS。前兩家沒有重取，ASUS 重新進入節點。
9. 再查 operations，仍為三筆；ASUS 的結果含 `reused=true`。相同操作 key 重試沿用舊結果；若內容不同會拒絕。
10. 打開 `report.md`，確認三家與來源都有，ASUS 保固待確認。最後 state 的 next 應為空。
11. Colab 使用兩個 subprocess 格完成以上步驟。最後下載整個成果 ZIP，包含兩份 SQLite 與執行紀錄。
12. 換全新輸出目錄重新演示，保留第一份成果供比較。不要刪除原狀態來「修好」Demo。

## 驗收數字

| 項目 | 中斷後 | 恢復後 |
|---|---|---|
| checkpoint 完成品牌 | 2 | 3 |
| ASUS 節點進入次數 | 1 | 2 |
| ASUS 唯一取證紀錄 | 1 | 1 |
| 報告 | 尚未完成 | 三家完整 |

本版操作 key 使用 `<run_id>:ASUS:source`，對應投影片中 R-C-001 的同一操作識別概念。示範保證來自本機 SQLite 的唯一鍵與內容核對；不推論所有外部服務都能保證恰好一次。

想一想：改 Thread 後為什麼不是恢復？Colab 整個執行階段回收後，哪幾個檔案必須先還原？
