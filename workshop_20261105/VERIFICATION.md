# 驗證紀錄

## 第二天｜2026-11-05

- 四份Day 2 notebook已使用專案.env的既有Key與gpt-6-luna，在各自獨立本機Jupyter kernel逐格跑通。主線成功執行含14次新模型呼叫；調整、逾時及重試另計。
- RAG前後引用ID有效；研究團隊交付Planner、三品牌Researcher、Writer、Reviewer與一輪修訂，確認最終報告包含主管摘要、HP／Lenovo／Dell比較及供應商問題。ID檢查只驗存在性，事實支持程度另以官網人工核對。
- 即時web_search成功呼叫並取得一個官方引用；兩次實際取得Lenovo官方PDF，指紋一致為unchanged，沒有捏造歷史價格。官網7來源查閱及採用邊界見[來源說明](day2/SOURCES.md)。
- L05兩個獨立Python程序：中斷後checkpoint只有HP，帳本有HP／Lenovo；恢復後log為HP→Lenovo→Lenovo(reused)→Dell，唯一結果三筆。新增中斷現場ZIP及還原格，跨目錄還原後接續的測試通過。
- L06真實LangGraph interrupt：待審零存檔、修改仍待審、舊hash拒絕、核准存本機一筆、重複決定拒絕；駁回分支測試零存檔。所有分支都沒有寄送。
- 33項測試通過（第二天新增7項），涵蓋來源適用性、27格矩陣、角色上限、操作／checkpoint差異、資料身分、ZIP恢復、快取失效及審核／監測錯誤分支。單元測試使用模型替身；實跑notebook使用真實API。
- 四張draw.io狀態圖已匯出並目視核對。七份notebook皆為明文程式，圖放上方、六步白話說明，發布版清空執行輸出。來源manifest、357頁對照、語法及相對連結通過；第一天檔案SHA-256完全相同。
- 實測修正：角色輸出截斷、修訂稿誤回審查摘要，以及API讀取逾時。現在限制篇幅、要求完整報告；L04相同輸入重用已完成角色回覆，任務／證據變動會重新呼叫。
- 已在實際Colab網頁、已登入帳號與Python 3 CPU雲端執行階段跑通L03：安裝、來源表、隱藏Key輸入、前後兩份RAG報告、引用檢查、ZIP下載及複製到雲端硬碟。另透過表單修改中文問題並重跑，這次網頁測試共3次真實gpt-6-luna呼叫。ZIP解壓CRC通過，8個檔案含需求／來源／片段、前後報告與trace，逐檔確認不含Key。詳見[Colab網頁驗證](examples/day2_colab_validation.json)。
- 網頁實測發現流程原始碼格缺少Colab表單標題，導致整段程式攤開；已補上標題，並在Colab確認收合後仍可執行，同步套用第二天四份notebook。
- L04–L06仍只有本機Jupyter實跑；本次未驗證重新登入、其他Google帳號、Antigravity App或Windows，未部署持續排程或正式寄件。

實際產物：[驗證摘要](examples/day2_validation.json)、[講師示例](examples/day2/README.md)。重跑：`python scripts/run_notebooks.py --day 2 --live-model`；只跑一章可加`--notebook 04_research_loop.ipynb`。Key不寫入程式、報告、ZIP或發布notebook。

Colab MCP 相容性修正：重現預設 stderr 不支援 `fileno()` 時的同一個例外，改將 MCP 子程序錯誤輸出寫入成果資料夾的 `mcp_server.log`。回歸測試使用無檔案描述元的串流，仍實際啟動 MCP、探索工具及查詢 SQLite；未以直接讀 JSON 替代 MCP。

## 第一天下午｜2026-11-05

- 三份第一天 notebook 已在獨立本機 Jupyter kernel 逐格通過，包含前後報告、Skill、真實 MCP／SQLite 與成果 ZIP。
- 自動驗證以模型替身取代付費 API、以測試輸入取代互動 Key 提示；發布 notebook 保留真正模型呼叫及隱藏輸入框，不含測試替身。
- 第一天下午新增 8 項測試通過，涵蓋實際 OpenAI SDK 的模擬 HTTP 工具往返、Skill 原文傳入、MCP 探索與查詢、市場與空值、not_found、錯誤及六次上限。
- 三張狀態圖已以 draw.io 匯出並目視核對；第一天 notebook 的圖放在第一個執行格上方。
- 相對連結、357 頁對照、原始碼同步與 notebook 語法檢查通過；三份成果 ZIP 完整且未含測試 Key。
- 已使用使用者指定 `.env` 的既有 Key，以 `gpt-6-luna` 真實執行第一天三份 notebook、六次研究，共 17 次模型呼叫。核對 TW 兩筆資料、保固缺漏、Skill 規則、MCP 查詢與 not_found 均符合預期。
- 尚未在 Colab 網頁端、Antigravity App 或 Windows 演練；Colab 隱藏輸入框仍需在網頁端確認。
- 此段記錄第一天下午驗證；第二天更新與驗證見上方。

實際模型紀錄：[GPT-6 Luna 驗證](examples/day1_gpt6_luna_validation.json)；離線紀錄：[第一天下午驗證](examples/day1_validation.json)。維護者執行 `python scripts/run_notebooks.py`，預設只驗證第一天下午。加上 `--live-model` 可讀取專案根目錄 `.env`，實際呼叫 `gpt-6-luna`。

## 早期固定規則範例歷史紀錄

日期：2026-11-02。

- 學生本機安裝指令 `pip install -e .` 已測，並從教材目錄以外執行成功。
- 本機 Python 3.11，指定版本 LangGraph 1.2.19、langgraph-checkpoint-sqlite 3.1.3、MCP 1.30.0。
- 17 項核心驗收通過：配置與缺漏、SQLite 參數查詢、metadata 篩選、有界補查、真正 MCP stdio、跨程序恢復、冪等內容核對、比較條件、變動門檻、新品證據、審核三分支、草稿失效核准、發送前後中斷。
- 七份 notebook 已在各自獨立 Jupyter kernel 逐格執行通過，包含內嵌教材展開、MCP、跨程序中斷恢復、三種審核分支與成果 ZIP 產生。
- Markdown 相對連結、357 頁涵蓋、Python 語法及七份 notebook 內嵌雜湊同步檢查通過。

此早期版本當時未在 Google Colab 網頁端、Windows 或 Antigravity App 中實際演練；未執行平台模型研究、真實官網選做、正式寄件或真實排程。Antigravity 操作指引提供可執行步驟，平台 UI 與模型行為須課前確認。

套件安裝在獨立環境完成；notebook 自動驗證使用同一已安裝環境略過重複安裝，仍逐格執行 bootstrap、流程、MCP 與驗收。本機 notebook 成功不代表 Colab 帳號、網路或方案均已驗證。

重新驗證：安裝 requirements-dev.txt，執行 `python -m unittest discover -s tests -v`、`python scripts/check_materials.py`、`python scripts/run_notebooks.py`。最後一項需要允許 Jupyter kernel 使用本機連線。
