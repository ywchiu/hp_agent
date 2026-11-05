# 排錯表

第一天下午依各 Colab 的逐步說明操作；只需改問題或規則。以下前四列適用第一天，其餘多為第二天的程式維護排錯。

| 現象 | 先看什麼 | 處理步驟 |
|---|---|---|
| UnsupportedOperation: fileno | 是否仍使用更新前的研究助理格 | 重新開啟 GitHub 最新 Colab，再從第 1 步依序播放；MCP 錯誤輸出已改存 mcp_server.log |
| 401／無效 Key | 是否使用老師當堂提供的 Key | 重跑第 2 步重新輸入，仍失敗請老師確認，不把 Key 貼給 AI |
| 429／額度不足 | 錯誤代碼與模型名稱 | 請老師確認用量／額度；不要用重複重跑製造更多請求 |
| 改了中文但結果沒變 | 第 4 步是否重跑 | 先重跑第 4 步，再跑第 5 步，對照 before 與 after |
| MCP 查不到資料 | 工具結果 status | not_found 是正常結果；error／斷線要修服務，不能改讀 JSON 冒充 MCP |
| ModuleNotFoundError: workshop | Python 是否來自 `.venv`、是否在教材目錄 | 重新執行 `python -m pip install -e .`；Colab 先跑 bootstrap 格 |
| 套件裝不起來 | 網路、Python 版本、第一個錯誤 | 使用 Python 3.10+；重跑安裝格，不要改成任意最新版 |
| Colab MCP 的 event loop 錯誤 | 是否在 notebook 直接呼叫同步 `run()` | notebook 使用 `await inspect_database(...)`；CLI 才用 `run()` |
| MCP 啟動後沒有文字 | stdio 服務在等待協定訊息 | 用教材 client 或 Antigravity 呼叫；不是開網頁連 localhost |
| MCP 服務找不到 workshop | 設定中的 Python 路徑、PYTHONPATH | 用本機 venv 執行 `scripts/make_mcp_config.py` 重新產生；不要手填別人的路徑 |
| 第一個恢復命令回傳非零 | 是否包含 LESSON_PAUSE_AFTER_LENOVO_EFFECT 且結束碼23 | 只有該訊息及結束碼組合才是預定中斷；先讀 state.json，以相同目錄與Thread跑 resume |
| 恢復時找不到 Thread | 同一資料夾、同一 Thread、SQLite 是否還在 | 還原完整備份 ZIP；不可換 Thread 後稱為恢復 |
| Thread 已存在 | 是否重跑 recover-start | 同輪用 resume；新一輪換全新目錄，不刪除舊證據 |
| SQLite database is locked | 是否同時操作同一資料庫 | 一次一個程序；本教材不演示多 worker 併發 |
| stale approval | hash 是否對應目前草稿與收件人 | 重新讀取待審版本，重新核准；不要刪掉檢查 |
| operation key reused | 同事件的草稿是否改了 | 不以新內容覆寫已執行操作；建立新事件並重新審核 |
| 沒有通知 | 是 no_major_change、data_error、pending_review 還是 reject？ | 先看狀態；四種都可能暫時零通知，原因不同 |
| Colab 重啟後檔案消失 | 是否下載狀態 ZIP | 重新上傳完整保存資料；僅 notebook 副本不足以恢復 |

模型操作出錯時，請描述「哪個輸入、哪個輸出、哪項驗收不符」，再讓 Antigravity 修正；不要只說「不能跑」。

第二天：模型輸出未完整時請縮小問題，保留現有成果，不把截斷結果當完成；來源HTTP失敗為data_error，不覆蓋有效基準。L05／L06使用獨立Python程序或同步SQLite graph，Colab以await asyncio.to_thread執行，不在已有事件迴圈內呼叫asyncio.run。子程序stdout／stderr寫入真實log檔，不依賴ipykernel的fileno。

L05「目錄已有進度」：不要重跑start，改執行resume；要重演用新的BATCH_DIR。L06「已結束」：查看review_state.json，已核准／駁回就不再次提交；另一分支用新的REVIEW_DIR。
