# 第二天｜企業 120 台商務筆電採購研究

把一份真實工作拆成四章：查資料、分工研究、中斷接續、人工審核。你主要改中文需求與規則，由 AI 協助修改，再用來源和執行紀錄驗收。每份 Colab 都可獨立執行，使用老師提供的 Key，預設 `gpt-6-luna`、CPU 即可。

|順序|工作與交付|操作步驟|Colab|
|---|---|---|---|
|L03 RAG|比較前後查詢、取回片段與引用|[一步一步做](../labs/03_rag.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/03_rag.ipynb)|
|L04 研究團隊|三品牌獨立研究、27格矩陣、主管報告、供應商問題|[一步一步做](../labs/04_research_loop.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/04_research_loop.ipynb)|
|L05 中斷恢復|兩個 Python 程序、SQLite進度與結果去重|[一步一步做](../labs/05_recovery.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/05_recovery.ipynb)|
|L06 人工審核|詢價草稿、修改再審、核准／駁回、來源快照|[一步一步做](../labs/06_review_monitor.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/06_review_monitor.ipynb)|

## 採購任務

教學企業要更新120台：業務／顧問60台、工程／分析40台、行政／管理20台，含稅預算600萬，預計2027-01-15前交貨。這些是情境數字，沒有假裝已取得供應商報價。

研究 HP EliteBook 8 G1a 14 Next Gen AI、Lenovo ThinkPad T14 Gen 6 AMD、Dell Pro 14 Plus PB14250 Core Ultra 200V。九項需求包括32GB、1TB、出差配置≤1.5kg、Windows 11 Pro、底座與雙螢幕、安全驗收、台灣三年到府及正式含稅報價。需求全文見 [case.json](case.json)。

## 資料與真實執行

7份官方來源、29筆人工摘述，其中27筆可用、1筆桌機服務用來練習排除、1筆HP搜尋索引線索因未讀到正文而排除。每筆有來源ID、網址、段落／頁碼、適用市場及查閱日期。參見[來源說明](SOURCES.md)、[來源清單](sources.json)、[證據片段](evidence.json)。不用下載整份PDF，也不需要 Base64 解碼。

模型、LangGraph、SQLite、跨程序恢復與interrupt都實際執行。L03使用詞彙檢索，沒有使用embedding。L04各角色分開呼叫模型，相同輸入會重用已完成角色回覆，修改任務或證據後才重新呼叫；可選擇真實 web_search，只搜官方站，保留搜尋引用，需核實後才能納入證據。L06可手動取得真實官方PDF快照，沒有捏造歷史價格。未即時查詢時會明說使用封存資料。引用ID檢查只查存在性，還要人工核對事實支持程度。

目前沒有三品牌台灣指定SKU的完整報價、交期與到府服務購買憑證；合格產物包含缺口與供應商問題。不可因系列支援32GB就宣稱台灣交付配置符合，也不能用海外價格排名。

## 用 Antigravity 示範

開啟本儲存庫，請 AI 閱讀本頁、對應Lab與 `procurement.py`。老師在專案根目錄 `.env` 放 Key（支援 `OPENAIAPI_KEY`、`OPENAI_API_KEY`），學員不必看 Key；Colab則在第2步輸入。不要把 `.env` 貼到AI對話或提交Git。

首次請 AI 依 [requirements.txt](requirements.txt) 在專案虛擬環境安裝套件。後續直接用白話要求它執行本章，程式入口例如：

```sh
python workshop_20261105/day2/procurement.py rag --out tmp/day2_rag --task 'Lenovo不同顏色配置都低於1.5kg嗎？台灣三年保固等於到府嗎？'
python workshop_20261105/day2/procurement.py team --out tmp/day2_team --task '替120台更新案交主管摘要、三品牌風險與詢價問題'
python workshop_20261105/day2/procurement.py start --out tmp/day2_batch
python workshop_20261105/day2/procurement.py resume --out tmp/day2_batch
python workshop_20261105/day2/procurement.py draft --out tmp/day2_review
```

`start` 預期以23結束，代表教學暫停；不是所有錯誤都算預期中斷。恢復須使用同一輸出目錄、Thread、模型與需求。審核則先讀待審草稿及hash，再由你指示 AI 用 `approve`／`reject`／`revise` 和 `--expected-hash` 指定版本。範例只將核准草稿存進本機outbox，沒有寄信工具。

可直接複製[各章任務指令](../prompts/)。Colab五步：準備 → 輸入Key → 觀察初始結果 → 修改需求／解讀狀態 → 重跑或決定。每一步都有目的、預期結果與驗收方式。

## 課後接續

Colab可能回收整個暫存磁碟。L05第4步會產生中斷現場ZIP，供選做的跨執行階段恢復示範使用。換新執行階段時先準備程式、輸入Key，再上傳這份備份並在選做還原格填檔名。L06可用既有完整備份讀回待審稿，已結束的決定不能重做。只保留notebook或Thread名稱不能恢復。

L05只有已提交結果的重用保證；若模型回覆後、結果寫入前失敗，重試可能再呼叫模型。這不是對所有外部服務的「恰好一次」保證。L06保存核准草稿不等於寄出信件。持續排程與正式寄送均未部署。

講師課前可對照[實跑報告與詢價示例](../examples/day2/README.md)；這些是示例，不能代替學員執行證據。

2026-11-05 已在 Colab 網頁逐份跑通 L03–L06：隱藏 Key、真實模型、27格研究矩陣、選做即時搜尋、官方 PDF 追蹤、L05 中斷 ZIP 跨全新執行階段接續，以及 L06 待審 ZIP 還原後駁回。核准只存一筆、駁回不存，兩者皆零寄送；當時的四章成果 ZIP 已下載並核對，課堂末尾的下載格現已移除。詳見[驗證範圍](../VERIFICATION.md)。
