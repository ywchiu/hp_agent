# 驗證紀錄

## 移除選做備份還原｜2026-11-06

L05／L06移除備份還原說明與表單，L05不再產生中斷現場ZIP；目前分別9個／12個程式格，仍保留同一Colab內的跨程序恢復與人工審核。重新產生教材並通過同步／語法／連結／五步檢查及60項單元測試，確認其他五份notebook未變動。本次未重跑真實API或Colab網頁；下方10格／13格的網頁實測是移除前紀錄。

## 第二天下午：恢復、比較與人工審核｜2026-11-06

本次修訂L05及L06，第一天與L03／L04 notebook未變動。新增比較／觀察工具獨立於原研究程式，不擴改上午流程。

- 60項單元測試通過；新增4項驗證同SKU／市場／幣別／稅別／配置可比性、門檻與無效價格、PDF取得失敗／內容改動不覆蓋基準，以及真實SQLite待審、修改、舊版本拒絕、重複決定與三條分支。
- 本機獨立Jupyter kernel以.env課堂Key及gpt-6-luna跑通L05共10格、L06共13格。L05使用兩個Python程序實際中斷／恢復，保留HP/Lenovo/Lenovo(reused)/Dell四次節點進入、三筆唯一結果，再次恢復新增0次操作；錯誤Thread在模型呼叫前拒絕。
- Colab網頁新上傳兩份教材並使用CPU執行階段，實際安裝套件、隱藏Key及呼叫gpt-6-luna。L05全部10格通過；L06全部13格通過，含真實官方PDF快照、明確標示的兩週模擬報價、四種比較結果、修改前後版本、舊版本拒絕、預設wait與三種獨立審核分支。
- Colab表單另測DECISION由wait改approve及重跑，主任務維持outbox_count=1、sent_count=0；SECOND_WEEK_PRICE改39,000後不達10%門檻，不建立待審，後面的修改／決定格都只顯示無待審。
- 狀態圖以draw.io重建並檢視PNG，確認圖上區分流程外的真實來源觀察／模擬比較與LangGraph人工審核。教材重新產生後通過明文同步、語法、連結、五步操作、圖檔及清空輸出檢查。
- 機器可讀摘要見[下午驗證](examples/afternoon_validation.json)。發布notebook不含Key或執行輸出；兩週價格和SKU只供規則演練，不宣稱真實歷史報價。所有核准只存本機草稿，沒有正式寄送、排程或審核者身分／權限服務。Antigravity介面及部署排程未在本次測試。

## 深度研究與反思補查｜2026-11-06

本次只修訂L04與對應說明，其他六份notebook位元組未變。參考四月PDF 195–205頁及完整Deep Research notebook，補回規劃、實際搜尋、HTML／PDF原文閱讀、整理、Critic與重新規劃補查。舊版固定Writer修稿的測試紀錄保留於下方，不能代表新版研究迴圈。

- 56項單元測試通過，涵蓋真實LangGraph暫停／續跑、補查累積、無新證據、供應商事項停止、來源封鎖、重新導向範圍、HTML抽文、搜尋來源空值、成功快取與改題失效、結構回覆驗證及Reader未知ID不快取。
- 本機獨立Jupyter kernel跑通新版12個程式格，使用.env課堂Key與gpt-6-luna，完成真實搜尋、兩輪研究與最終報告；另重跑新版全流程，沿用完成回覆與成功原文快取。

- 第一次本機真實研究新增原文1／3段；另一輪從無快取開始實測新增3／0段，第二輪沒有改善也如實保留。每次完整研究17個成功角色回應、5個搜尋請求；API實際回傳10個web_search_call，和參數要求不同。引用ID檢查通過，但不代表事實支持已人工逐項核准。
- Colab網頁曾逐格完成準備、Key、計畫、第一輪搜尋／原文／初稿／Critic與第二輪新計畫；觀察到首輪1段新原文。補查期間遇到503及含額外文字的JSON回覆，修正後重啟重測，已完成新版準備、Key及計畫；原工作區隨後消失，因此新版剩餘搜尋／報告格與完成後重跑尚未完成網頁驗證，不能宣稱全部Colab格已通過。
- 機器可讀摘要見[深度研究驗證](examples/deep_research_validation.json)，包含各輪新證據、實際網址／讀取狀態、API工具數與網頁測試中斷範圍。發布notebook不含Key、模型輸出或原文快取。

新版記憶體checkpoint只供同一執行階段分段教學，並未宣稱跨程序持久化。官方網頁可能403、空白或逾時；只記成功讀取原文，不以搜尋摘要替代。引用檢查只確認ID存在，事實仍需人工核對。搜尋請求設定max_tool_calls=1，但真實API有回傳較多工具項目的情況，因此記錄實際數量，不將參數當費用硬上限。暫時性API失敗最多自動重試一次，失敗嘗試用量另計。


## 直接下載PDF、Chroma與搜尋預覽｜2026-11-06

本次只更新L03的流程與相應說明，其他六份notebook未變動。三品牌競品研究主題保留，改為Colab直接下載官方PDF → 實際embedding寫入Chroma → 先檢查搜尋片段 → 下一格生成比較表。

- Chroma 1.5.9使用PersistentClient，441筆、1536維；向量、原文、檔名與PDF頁次實際存進collection。JSON只存文件身分與呼叫紀錄。以新的Python程序重新開啟磁碟上的Chroma，確認441筆仍在。
- 三份PDF共133頁、441段，首次建立文件向量14次API呼叫。每次問題另做一次embedding；生成回答使用預覽的同一批片段，不再計算第二次問題向量。實際查詢Chroma並按檔名篩選，每份文件各取TOP_K段。
- 44項回歸測試通過，包含實際Chroma持久化與向量排序、逐文件取證、重用與文件／模型／切段失效、collection刪除後重建、下載失敗不留下假PDF、預覽與回答共用證據、HTML跳脫及引用範圍。
- 本機獨立Jupyter kernel以真實API跑通9個程式格，含兩輪搜尋與gpt-6-luna回答。Colab網頁以全新CPU執行階段實測套件安裝、隱藏Key、直接下載三份官方PDF、抽文、Chroma寫入與資料預覽、兩輪分開搜尋／回答；搜尋先顯示15段與18段，三品牌皆有頁碼與分數。
- Colab重跑直接下載格沿用三份完整PDF；重跑建立向量庫格顯示「重用索引True、本次文件embedding呼叫0」。另透過表單修改重量／USB-C問題及TOP_K=3，搜尋先顯示三品牌9段，再獨立執行回答。
- 網頁本次4次問題embedding、3次回答，與首次文件embedding分開計算。44項測試不消耗真實API；本機與Colab完整演練使用真實API。紀錄見[Chroma驗證摘要](examples/chroma_rag_validation.json)。

Colab的Chroma資料夾仍在暫存磁碟，刪除執行階段後需重新下載與建立。引用檢查只確認ID存在及頁次，仍須回原PDF核對型號與表格；本次未測Windows與Antigravity App介面。下方「三品牌PDF競品研究」為1592341的上傳／JSON索引版本驗證，不能當作Chroma驗證。

## 三品牌PDF競品研究｜2026-11-06

本次只更換L03，維持120台商務筆電競品研究主題：學員下載並上傳HP、Lenovo、Dell官方PDF，實際建立文件／問題embedding，再交gpt-6-luna產出三品牌比較、證據缺口與供應商問題。其他六份notebook未變動。

- 三份官方PDF共133頁，抽取441段；text-embedding-3-small回傳1536維向量，首次文件索引分14次API呼叫。中文問題每次另做一次embedding及一次真實gpt-6-luna回答。
- 本機獨立Jupyter kernel跑通L03七個程式格；真實PDF及API驗證，不使用固定回覆。單元測試40項通過，其中新增7項覆蓋PDF抽文、頁碼、中文語意排序、索引重用／失效、多文件唯一ID與逐文件檢索、API異常及引用限制。
- 實際Colab網頁測試包含CPU套件安裝、隱藏Key、左側檔案面板一次上傳三份PDF、抽文預覽、向量索引、預設前後問題與競品表、引用頁碼對照。另修改中文問題與TOP_K重跑；相同索引再跑顯示重用True、文件embedding呼叫0次。本次網頁共4次問題embedding及4次回答。公開摘要見[PDF RAG驗證](examples/pdf_rag_validation.json)。
- 引用檢查只確認ID存在於本輪取回片段與對應頁次，不能證明模型每個結論都受原文支持。已人工檢查HP封面及Dell第8頁表格；表格抽文雖保留間距仍可能錯位，教材要求回PDF原頁核對。掃描圖片沒有OCR；未測Windows或Antigravity App。
- HP文件為14 inch Notebook AI PC維修手冊，不自動等同所有Next Gen AI配置；Dell200V與200U分開。PDF不能證明台灣報價、交期或已含三年到府。廣泛採購問題可能找不到部分規格，保留「目前片段不足」，不把缺片段說成整本沒有。

重跑新版L03：`python scripts/run_notebooks.py --day 2 --notebook 03_rag.ipynb --live-model --pdf hp_manual.pdf lenovo_t14.pdf dell_pro.pdf`。跑第二天全部章節時也需提供`--pdf`。Key讀取專案.env，文件保留測試端；不公開轉存整份廠商PDF或原始抽文／向量。

下方2026-11-05紀錄屬當時版本；其中L03使用舊關鍵字檢索，不代表新版PDF流程。

## 移除末尾下載步驟｜2026-11-05

七份notebook已移除第6步說明與自動下載成果格，改為五步、共55個程式格。研究、MCP、中斷恢復與審核程式沿用先前已實測內容；L05中斷現場備份仍供恢復示範使用。README、Lab、講師說明與選用觀察清單同步更新。

本次確認七份產生結果與來源一致、沒有第6步或自動下載呼叫，並核對保留的55個程式格與先前網頁實測內容完全一致。本次33項回歸測試通過。下方62格與11份ZIP的網頁紀錄是移除前的實測，對應JSON中的tested_revision；不代表本次重新執行下載流程。

## Colab 網頁完整演練｜2026-11-05

七份 notebook 共62個程式格，已透過實際 Colab 網頁、已登入帳號、Python 3 CPU 雲端執行階段逐份執行；每章重新安裝套件並輸入隱藏 Key，使用專案既有 Key 與 `gpt-6-luna` 真實呼叫模型。這份結果有別於下方本機 Jupyter 與單元測試紀錄。

|章節|網頁實測與驗收|
|---|---|
|L01|前後研究、資料 ID／日期、台灣32GB保固待確認、成果下載。|
|L02A|在網頁編輯 Skill 加入三句主管摘要，確認規則寫入並改變報告，前後成果下載。|
|L02B|真實 MCP stdio 啟動與 SQLite 查詢，正常資料與 `not_found`、原始碼格收合、成果下載；沒有 `fileno()` 例外。|
|L03|前後 RAG、有效引用、排除桌機與不可用來源、成果下載；同日另測表單改問重跑與儲存 Drive 副本。|
|L04|8次角色模型呼叫、1輪修訂、27格矩陣及完整報告；選做即時搜尋取得2個官方引用，成果下載。|
|L05|預期結束碼23、中斷時 checkpoint／帳本差異、Lenovo重進沿用、三品牌唯一結果；下載中斷ZIP，刪除測試執行階段後，在全新Colab上傳還原，僅新增Dell一次模型呼叫。|
|L06|真實interrupt、修改後顯示完整新版草稿、舊hash與重複決定拒絕、核准僅存一筆；待審ZIP在全新Colab還原後駁回為零存檔；兩分支零寄送。官方PDF連讀兩次，建立基準後為unchanged。|

七章成果與四份中斷／還原／待審分支 ZIP 都已從瀏覽器實際下載，逐檔解壓CRC與既有Key外洩檢查通過；各ZIP的SHA-256及驗收結果見[第一天網頁紀錄](examples/day1_colab_validation.json)、[第二天網頁紀錄](examples/day2_colab_validation.json)。原始下載與瀏覽器截取保留於測試端，公開紀錄不含帳號、Key或本機私人路徑。

網頁演練修正：MCP來源格補Colab標題以預設收合；L06原本修改後只顯示狀態，現補上完整新版待審草稿。同步修正產生器並重建notebook；33項單元測試及七份教材同步、語法、連結、狀態圖與發布輸出檢查通過。單元測試使用模型替身，網頁演練使用真實API。

驗證範圍為目前已登入的Google帳號；未測重新登入、其他帳號、Windows或Antigravity App，未正式寄件或部署持續排程。L04快取失效與其他錯誤分支的覆蓋來自單元測試，未逐一重演所有網頁輸入組合。

## 第二天｜2026-11-05

- 四份Day 2 notebook已使用專案.env的既有Key與gpt-6-luna，在各自獨立本機Jupyter kernel逐格跑通。主線成功執行含14次新模型呼叫；調整、逾時及重試另計。
- RAG前後引用ID有效；研究團隊交付Planner、三品牌Researcher、Writer、Reviewer與一輪修訂，確認最終報告包含主管摘要、HP／Lenovo／Dell比較及供應商問題。ID檢查只驗存在性，事實支持程度另以官網人工核對。
- 即時web_search成功呼叫並取得一個官方引用；兩次實際取得Lenovo官方PDF，指紋一致為unchanged，沒有捏造歷史價格。官網7來源查閱及採用邊界見[來源說明](day2/SOURCES.md)。
- L05兩個獨立Python程序：中斷後checkpoint只有HP，帳本有HP／Lenovo；恢復後log為HP→Lenovo→Lenovo(reused)→Dell，唯一結果三筆。新增中斷現場ZIP及還原格，跨目錄還原後接續的測試通過。
- L06真實LangGraph interrupt：待審零存檔、修改仍待審、舊hash拒絕、核准存本機一筆、重複決定拒絕；駁回分支測試零存檔。所有分支都沒有寄送。
- 33項測試通過（第二天新增7項），涵蓋來源適用性、27格矩陣、角色上限、操作／checkpoint差異、資料身分、ZIP恢復、快取失效及審核／監測錯誤分支。單元測試使用模型替身；實跑notebook使用真實API。
- 四張draw.io狀態圖已匯出並目視核對。七份notebook皆為明文程式，圖放上方、六步白話說明，發布版清空執行輸出。來源manifest、357頁對照、語法及相對連結通過；第一天研究邏輯未改，後續Colab顯示修正見上方。
- 實測修正：角色輸出截斷、修訂稿誤回審查摘要，以及API讀取逾時。現在限制篇幅、要求完整報告；L04相同輸入重用已完成角色回覆，任務／證據變動會重新呼叫。
- 已在實際Colab網頁、已登入帳號與Python 3 CPU雲端執行階段跑通L03：安裝、來源表、隱藏Key輸入、前後兩份RAG報告、引用檢查、ZIP下載及複製到雲端硬碟。另透過表單修改中文問題並重跑，這次網頁測試共3次真實gpt-6-luna呼叫。ZIP解壓CRC通過，8個檔案含需求／來源／片段、前後報告與trace，逐檔確認不含Key。詳見[Colab網頁驗證](examples/day2_colab_validation.json)。
- 網頁實測發現流程原始碼格缺少Colab表單標題，導致整段程式攤開；已補上標題，並在Colab確認收合後仍可執行，同步套用第二天四份notebook。
- 後續已補齊四章Colab網頁實測與跨全新執行階段還原，詳見上方完整演練。

實際產物：[驗證摘要](examples/day2_validation.json)、[講師示例](examples/day2/README.md)。重跑：`python scripts/run_notebooks.py --day 2 --live-model`；只跑一章可加`--notebook 04_research_loop.ipynb`。Key不寫入程式、報告、ZIP或發布notebook。

Colab MCP 相容性修正：重現預設 stderr 不支援 `fileno()` 時的同一個例外，改將 MCP 子程序錯誤輸出寫入成果資料夾的 `mcp_server.log`。回歸測試使用無檔案描述元的串流，仍實際啟動 MCP、探索工具及查詢 SQLite；未以直接讀 JSON 替代 MCP。

## 第一天下午｜2026-11-05

- 三份第一天 notebook 已在獨立本機 Jupyter kernel 逐格通過，包含前後報告、Skill、真實 MCP／SQLite 與成果 ZIP。
- 自動驗證以模型替身取代付費 API、以測試輸入取代互動 Key 提示；發布 notebook 保留真正模型呼叫及隱藏輸入框，不含測試替身。
- 第一天下午新增 8 項測試通過，涵蓋實際 OpenAI SDK 的模擬 HTTP 工具往返、Skill 原文傳入、MCP 探索與查詢、市場與空值、not_found、錯誤及六次上限。
- 三張狀態圖已以 draw.io 匯出並目視核對；第一天 notebook 的圖放在第一個執行格上方。
- 相對連結、357 頁對照、原始碼同步與 notebook 語法檢查通過；三份成果 ZIP 完整且未含測試 Key。
- 已使用使用者指定 `.env` 的既有 Key，以 `gpt-6-luna` 真實執行第一天三份 notebook、六次研究，共 17 次模型呼叫。核對 TW 兩筆資料、保固缺漏、Skill 規則、MCP 查詢與 not_found 均符合預期。
- 後續三章Colab網頁演練已完成，隱藏Key輸入及MCP雲端啟動均通過，詳見上方完整演練；Antigravity App與Windows未測。
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
