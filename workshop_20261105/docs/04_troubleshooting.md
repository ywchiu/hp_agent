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

## L03下載／上傳PDF與embedding

找不到檔案：在Colab左側檔案區完成上傳，PDF_FILES填該區顯示的檔名，多份用半形逗號分隔，不能填自己的電腦路徑。PDF文字為空：先OCR或換能選取文字的官方手冊。加密、超過50MB／200頁或1000片段會停止，換較短文件再試。API的401／429請老師確認課堂Key與額度，不貼Key。相同檔案及設定可重用文件向量；換問題仍有問題embedding與回答用量。中文提問檢索英文手冊可能有遺漏，調整問題、TOP_K並回原PDF核對，不能把排序分數當正確率。

PDF出現`EOF marker not found`或`Stream has ended unexpectedly`：先確認左側檔案的上傳進度全部消失，再重跑第3步。檔名先出現不代表上傳完成；若仍失敗，重新下載並在電腦上打開確認PDF完整後再上傳。

官方PDF直接下載失敗：成功的文件會保留；從第1步官方連結另行下載失敗的文件，透過左側檔案面板上傳，取消勾選AUTO_DOWNLOAD後重跑第3步。網站可能封鎖Colab，不能保證每次都能自動下載。

L03的Chroma存在`results/03_rag/chroma`。同一執行階段重跑會重用；刪除或回收執行階段後，重新播放前面各格即可重建。若出現庫內資料不完整，先重跑建立Chroma那格，再重跑搜尋、回答；改問題或TOP_K後也要先重跑搜尋。不要只刪除資料夾中的單一資料庫檔案。

## L04研究迴圈

- 卡在計畫：這是預定暫停，播放下一個「第一輪」格才搜尋。卡在Critic：先看公開缺口，再播放補查計畫與完成格。
- 網址顯示403／blocked_page：已搜尋但原文沒有讀成功，不算WEB新證據；可用其他官方頁面，或在TASK指定可讀的型號文件。不要刪除失敗紀錄。
- 第二輪沒有出現：先看停止原因；只剩供應商報價、資料足夠、到輪數上限都可能提早停止。不是每次都必須重查。
- 模型503／逾時／未完成：SDK對暫時錯誤最多重試一次；仍失敗時，同一session重跑失敗格，已完成角色會重用快取；不把截斷回覆存成成功。若要全新需求，改TASK並重跑第3步起各格。
- 結構驗證未通過：沒有唯一有效JSON就會停止，不會把說明文字當研究資料。保留前面成果，重跑當格；Reader引用未知ID也不會存成成功快取。
- 重新規劃問題重複：模型產生完全相同query會排除；語意重複仍由講師與學員核對，請AI調整TASK的查證面向。
- 刪除／重啟執行階段：記憶體checkpoint與暫存快取會消失，從第1步開始。跨程序持久化恢復見L05。
- 網路不可用：SOURCE_MODE改snapshot並從第3步重跑，畫面明說未上網；模型仍有API用量，不能當成即時研究驗證。
