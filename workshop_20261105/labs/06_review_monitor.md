# L06｜兩週追蹤、人工審核與測試通知

對照 PDF 307–348；建議 45 分鐘。交付：兩週快照、變化事件、草稿版本、決定、測試回執。

1. Antigravity 貼 [P07](../prompts/07_review.txt)；Colab 開 `06_review_monitor.ipynb`。
2. 建立第一週有效基準：TW-A32、TW、TWD、含稅、NT$40,000、SIM-W1、2026-10-26，保存成 week1.json。
3. 建立第二週快照：同 SKU／市場／幣別／稅別，NT$34,000、SIM-W2、2026-11-02，保存成 week2.json。
4. 算 `(34000-40000)/40000=-15%`。達絕對變動幅度 10% 門檻，產生 pending_review；目前測試寄件筆數必須是零。
5. 開啟待審單，核對 old／new 來源、日期、草稿 v1、收件人、附件 hash 與操作類型。
6. 選 **修改**，輸入保留來源與限制的 v2 文案。檢查草稿版本加一，狀態仍待審，寄件仍零筆。
7. 嘗試用 v1 的 hash 核准 v2，應拒絕且保留待審；改為核准目前 v2，寫入測試寄件器一次。
8. 同一事件再呼叫、再提交核准，應辨認已處理或拒絕重複決定，寄件仍一筆；檢查 outbox.sqlite，不只看終端文字。
9. 換獨立目錄測試 **駁回**，應保留原因記錄、不寄送。再換目錄直接 **核准**，只發送指定版本。
10. 測試相同價格（no_major_change）與缺價格（data_error）；兩者都是零通知，但前者資料可用，後者不可覆蓋有效基準。
11. 將 market 或 sku 改掉，應回 not_comparable；不可計算誤導的降價幅度。
12. 測試新品：需要 SKU、市場、發布日期與發布來源；只有新名稱不算完整事件。
13. 執行 notebook 的「發送前／後中斷」兩格；恢復後核對回執與唯一通知筆數仍為一。測試寄件器提供可查回執，所以能安全重試；若真實供應商查不到結果，應保留未知並人工確認，不能照此假定未寄出。
14. 保存全部資料與測試結果，執行課程驗收測試。

## 審核 API 的最小操作

```python
from workshop.flows import snapshot, detect, approval, digest
old = snapshot(40000, source_id='SIM-W1', date='2026-10-26')
new = snapshot()
event = detect(old, new)
state = approval('runs/review_01', event)
state = approval('runs/review_01', event, {
    'action': 'revise', 'hash': digest(state['draft']),
    'text': 'v2：同 SKU 降價 15%，請核對兩週來源；服務方案仍待確認。'
})
state = approval('runs/review_01', event, {
    'action': 'approve', 'hash': digest(state['draft'])
})
```

## 排程的課堂邊界

這裡用手動觸發模擬兩週，不建立真實自動排程。投影片的週一 09:00、Asia/Taipei 是部署需求：排程器觸發工作，持久儲存保留基準，LangGraph 執行流程，Inbox 等人決定。要持續上線需另行處理執行環境、備份、告警、結果未知、重試與費用。

驗收：未核准零通知、修改重新審、駁回零通知、核准一筆、重跑仍一筆；資料沒變與取得失敗狀態不同。
