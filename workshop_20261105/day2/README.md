# 第二天｜企業 120 台商務筆電採購研究

把一份真實工作拆成四章：查資料、分工研究、中斷接續、人工審核。你主要改中文需求與規則，由 AI 協助修改，再用來源和執行紀錄驗收。每份 Colab 都可獨立執行，使用老師提供的 Key，預設 `gpt-6-luna`、CPU 即可。

|順序|工作與交付|操作步驟|Colab|
|---|---|---|---|
|L03 PDF RAG|由Colab直接下載HP／Lenovo／Dell官方PDF、Chroma向量庫、搜尋預覽與有頁碼的中文問答|[一步一步做](../labs/03_rag.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/03_rag.ipynb)|
|L04 深度研究|拆子題、實際搜尋／讀原文、Critic、重新規劃補查、主管報告|[一步一步做](../labs/04_research_loop.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/04_research_loop.ipynb)|
|L05 中斷恢復|兩個 Python 程序、恢復前後表格、結果去重與錯誤Thread|[一步一步做](../labs/05_recovery.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/05_recovery.ipynb)|
|L06 人工審核|真實PDF快照、兩週模擬比較、等待／改稿／核准／駁回|[一步一步做](../labs/06_review_monitor.md)|[開啟](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/06_review_monitor.ipynb)|

## 採購任務

教學企業要更新120台：業務／顧問60台、工程／分析40台、行政／管理20台，含稅預算600萬，預計2027-01-15前交貨。這些是情境數字，沒有假裝已取得供應商報價。

研究 HP EliteBook 8 G1a 14 Next Gen AI、Lenovo ThinkPad T14 Gen 6 AMD、Dell Pro 14 Plus PB14250 Core Ultra 200V。九項需求包括32GB、1TB、出差配置≤1.5kg、Windows 11 Pro、底座與雙螢幕、安全驗收、台灣三年到府及正式含稅報價。需求全文見 [case.json](case.json)。

## 資料與真實執行

7份官方來源、29筆人工摘述，其中27筆可用、1筆桌機服務用來練習排除、1筆HP搜尋索引線索因未讀到正文而排除。每筆有來源ID、網址、段落／頁碼、適用市場及查閱日期。參見[來源說明](SOURCES.md)、[來源清單](sources.json)、[證據片段](evidence.json)。L04以這些摘述為起點，再搜尋與實際讀取新原文；L05–L06沿用封存摘述；L03由Colab直接下載HP／Lenovo／Dell三品牌官方PDF（也可自行上傳），從原始文件抽文字、切段與建立向量。

模型、LangGraph、SQLite、跨程序恢復與interrupt都實際執行。L03使用 `day2/pdf_rag.py`，實際呼叫 `text-embedding-3-small` 建立文件與問題向量，將向量、原文、檔名與PDF頁碼存入Chroma，再以餘弦距離從每份PDF各取前幾段，先在Colab顯示片段ID、頁次、相似度與原文預覽，學員看完再播放下一格，由 `gpt-6-luna` 使用同一批片段回答並附檔名、PDF頁次與片段ID。Chroma以PersistentClient保存到`results/03_rag/chroma`，相同PDF與切段／模型設定可重用collection；JSON只留文件身分與API呼叫紀錄，不保存向量。Colab執行階段刪除後需重建，不需註冊雲端資料庫帳號。掃描圖片頁需要先OCR，教材只讀可抽取的文字。L04沿用四月的Planner→Searcher→Reader→Synthesizer→Critic→Re-plan流程；預設真正web_search搜尋官方站，再以HTTP讀HTML／PDF，保存原文片段ID、位置、日期與讀取狀態。27筆封存摘述與新原文分開標記，搜尋摘要／403不當成新證據。Colab在計畫與Critic後暫停，預設最多兩輪，補查最多兩個新子題；分開公開可補查與供應商待確認事項。相同輸入沿用完成回覆與成功原文快取，重跑顯示格不另做研究；執行階段刪除不保留記憶體checkpoint。詳見[流程設計](RESEARCH_DESIGN.md)。L06主流程實際取得官方PDF快照，保存有效基準及每次觀察。另以明確標示的兩週教學模擬報價演練重大變化／無重大變化／不同SKU／資料不足；這些價格不是真實市場或歷史證據。重大變化才建立本機待審事件，預設等待，修改後須重新核准。三條獨立分支重用同一份模型草稿，核准／改稿再審各存1筆、駁回0筆，重跑不增加，實際寄送皆0。未即時查詢時會明說使用封存資料。引用ID檢查只查存在性，還要人工核對事實支持程度。

目前沒有三品牌台灣指定SKU的完整報價、交期與到府服務購買憑證；合格產物包含缺口與供應商問題。不可因系列支援32GB就宣稱台灣交付配置符合，也不能用海外價格排名。

## 用 Antigravity 示範

開啟本儲存庫，請 AI 閱讀本頁、對應Lab；L03程式在 `pdf_rag.py`，其餘在 `procurement.py`。老師在專案根目錄 `.env` 放 Key（支援 `OPENAIAPI_KEY`、`OPENAI_API_KEY`），學員不必看 Key；Colab則在第2步輸入。不要把 `.env` 貼到AI對話或提交Git。

首次請 AI 依 [requirements.txt](requirements.txt) 在專案虛擬環境安裝套件。後續直接用白話要求它執行本章，程式入口例如：

```sh
python workshop_20261105/day2/pdf_rag.py --pdf hp_manual.pdf lenovo_t14.pdf dell_pro.pdf --out tmp/day2_rag --question '比較三品牌記憶體與SSD，先核對型號與版本，附PDF頁碼'
python workshop_20261105/day2/deep_research.py --out tmp/day2_research --rounds 2 --mode live --task '替120台更新案查三品牌規格、維修性與台灣服務，找矛盾與缺口，再補查後交報告'
python workshop_20261105/day2/procurement.py start --out tmp/day2_batch
python workshop_20261105/day2/procurement.py resume --out tmp/day2_batch
python workshop_20261105/day2/procurement.py draft --out tmp/day2_review
```

`start` 預期以23結束，代表教學暫停；不是所有錯誤都算預期中斷。恢復須使用同一輸出目錄、Thread、模型與需求。審核則先讀待審草稿及hash，再由你指示 AI 用 `approve`／`reject`／`revise` 和 `--expected-hash` 指定版本。範例只將核准草稿存進本機outbox，沒有寄信工具。

可直接複製[各章任務指令](../prompts/)。L03五步：準備並確認來源 → 輸入Key → 直接下載PDF／確認抽文 → 建立Chroma／先看搜尋片段再生成回答 → 改中文問題重查。L04五步：準備來源 → 輸入Key → 改任務並看計畫 → 第一輪原文／初稿／Critic → 新計畫補查與報告比較。L05五步：準備 → 輸入Key → 故意中斷 → 用表格核對進度與帳本 → 跨程序恢復、再次接續與錯誤Thread驗證。L06五步：準備 → 輸入Key → 真實來源觀察及兩週模擬比較 → 改中文要求、看版本差異 → 選擇等待／核准／駁回，並比較三種獨立演練分支。每一步都有目的、預期結果與驗收方式。

## 課後接續

Colab可能回收整個暫存磁碟。L05第4步會產生中斷現場ZIP，供選做的跨執行階段恢復示範使用。換新執行階段時先準備程式、輸入Key，再上傳這份備份並在選做還原格填檔名。L06可用既有完整備份讀回待審稿；反覆播放只沿用既有決定，不會新增存檔，已結束的草稿需新事件才能重審。事件識別包含比較條件／門檻及來源狀態／指紋，資料版本改變會建立不同事件；僅觀察時間改變不會重複建立。只保留notebook或Thread名稱不能恢復。

L05只有已提交結果的重用保證；若模型回覆後、結果寫入前失敗，重試可能再呼叫模型。這不是對所有外部服務的「恰好一次」保證。L06保存核准草稿不等於寄出信件。持續排程與正式寄送均未部署。

講師課前可對照[實跑報告與詢價示例](../examples/day2/README.md)；這些是示例，不能代替學員執行證據。

2026-11-06 目前L03已在Colab網頁跑通直接下載、Chroma寫入、先看搜尋片段再回答，以及改問題／TOP_K與重用向量庫；44項測試通過。詳見[Chroma驗證](../examples/chroma_rag_validation.json)與[驗證範圍](../VERIFICATION.md)。

2026-11-06 前一版L03（1592341）已完成三品牌PDF上傳、embedding、前後比較、修改中文問題與索引重用的Colab網頁實測；40項回歸測試通過，詳見[PDF驗證](../examples/pdf_rag_validation.json)。

2026-11-05 已在 Colab 網頁逐份跑通當時的 L03–L06（L03為舊詞彙版，不能代表新版PDF embedding驗證）：隱藏 Key、真實模型、27格研究矩陣、選做即時搜尋、官方 PDF 追蹤、L05 中斷 ZIP 跨全新執行階段接續，以及 L06 待審 ZIP 還原後駁回。核准只存一筆、駁回不存，兩者皆零寄送；當時的四章成果 ZIP 已下載並核對，課堂末尾的下載格現已移除。詳見[驗證範圍](../VERIFICATION.md)。
