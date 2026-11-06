"""第二天四章的白話教學與明文 notebook 來源。"""
import json
from pprint import pformat


def day2_lessons(root):
    m=lambda text:('markdown',text,False)
    c=lambda text,folded=True:('code',text,folded)
    raw='https://raw.githubusercontent.com/ywchiu/hp_agent/main/workshop_20261105/day2/assets/'
    install='''# @title 準備本章（按播放，CPU 即可，不必修改）
import os, sys, subprocess, asyncio, json, shutil
from pathlib import Path
from getpass import getpass
if os.environ.get("HP_WORKSHOP_SKIP_INSTALL") != "1":
    subprocess.check_call([sys.executable,"-m","pip","install","-q",
        "openai==3.46.0","langgraph==1.2.19","langgraph-checkpoint-sqlite==3.1.3",
        "python-dotenv==1.2.4","httpx==0.28.1"])
print("準備完成，請接著播放下兩格。")
'''
    data={name:json.loads((root/'day2'/name).read_text()) for name in ('case.json','sources.json','evidence.json')}
    dataset='# @title 放入本章公開來源與採購需求（明文資料，不必修改）\nDATA_FILES = '+pformat(data,sort_dicts=False,width=110)+'''
Path("data_day2").mkdir(exist_ok=True)
for name,content in DATA_FILES.items():
    Path("data_day2",name).write_text(json.dumps(content,ensure_ascii=False),encoding="utf-8")
import importlib
importlib.invalidate_caches()
import day2_case as case
from IPython.display import display, Markdown

def show(result):
    if "report" in result: display(Markdown(result["report"]))
    print({k:result[k] for k in ("validation","stop_reason","pending","outbox_count","sent_count","hash") if k in result})
    if "review" in result: display(Markdown("### Reviewer 的意見\\n"+result["review"]))

print("120 台教學採購案；7 份官方來源、29 筆片段、27 格需求矩陣。")
display(Markdown("|來源|市場／範圍|查閱狀態|\\n|---|---|---|\\n"+"\\n".join(
    f"|[{s['id']}]({s['url']})|{s['market']} / {s['scope']}|{s['verification']}|" for s in case.load("sources.json"))))
'''
    creds='''# @title 輸入老師提供的 Key（不寫入原始碼）
API_KEY = getpass("貼上老師提供的 API Key：").strip()
if not API_KEY: raise ValueError("尚未輸入 Key；請重跑此格。")
MODEL = "gpt-6-luna" # @param {type:"string"}
print("Key 已暫存，不顯示也不存檔。模型：", MODEL)
'''
    def opening(title,diagram,flow,state):
        return m(f'''# {title}

第二天｜台灣企業 120 台商務筆電採購案｜先看狀態圖，再依五步操作。

![LangGraph 狀態圖]({raw}{diagram}.png)

{flow}

**State 是工作紀錄：** {state}。節點是分工，箭頭是下一步；只有 L05、L06 示範把狀態保存到 SQLite，L03重跑會重新呼叫模型；L04相同輸入會沿用已完成角色的回覆快取，修改需求後才產生新回覆。

**情境：** 業務／顧問 60 台、工程／分析 40 台、行政／管理 20 台，共 120 台；含稅總預算 NT$600 萬，預計 2027-01-15 前交貨。比較 HP EliteBook 8 G1a 14 Next Gen AI、Lenovo ThinkPad T14 Gen 6 AMD、Dell Pro 14 Plus PB14250 **Core Ultra 200V**。需要 32 GB、1 TB、出差配置 ≤1.5 kg、Win11 Pro、底座／雙螢幕、安全、台灣三年到府與正式報價。

**資料界線：** 企業、數量、預算及日期是教學情境；產品與服務片段來自真實官方網頁，查閱日為 2026-11-05。29 筆中有 27 筆可用、1 筆桌機服務陷阱、1 筆 HP 搜尋索引待核實線索。官網能力或海外 SKU 不等於台灣出貨／保固／報價。預算除以台數的 NT$50,000 是情境上限，不能當成市場價格。沒有台灣報價，結論可以是「待詢價」。
''')
    prepare=m('''## 第 1 步｜開啟本章，準備資料

**為什麼：** 每份 notebook 都自帶完整明文程式、採購需求及來源片段，可以獨立跑，不依賴上一章 Colab 暫存檔。

**怎麼做：** 存一份 Colab 副本，選 Python 3、CPU。由上往下播放下面三格；程式預設收起，不用展開修改。最後會看到來源表。可點來源網址核對內容，網站有時會擋機器連線，因此課堂主流程使用附帶的封存摘述，不會假裝剛完成線上搜尋。

**看什麼：** GLOBAL 是系列能力，IE 是愛爾蘭 SKU，TW 服務頁也未必是這一台已購買的服務。HP-SPEC 目前僅搜尋索引可見、直接存取 403，程式會排除它。

**卡住時給 AI：**「請依最後一段錯誤修復這個 Colab，保留 LangGraph、來源查核與未知值，只告訴我需要替換及重跑的格子。」只貼錯誤與對應格，不貼 Key。若要求重啟執行階段，重啟後從本步重跑。
''')
    key=m('''## 第 2 步｜輸入課堂 Key

**怎麼做：** 播放下格，在輸入框貼上老師提供的 Key，按 Enter。預設模型是 `gpt-6-luna`，不用自己申請 Key。每份 notebook 都需輸入，執行階段結束後會消失。

**應該看到：** Key 已暫存與模型名稱，不會顯示 Key。本章真的呼叫模型，重跑會產生用量。401 請老師確認 Key；429 請老師確認課堂額度；模型不存在時使用老師指定名稱。只回報錯誤碼，不貼 Key，不要將 Key 放進 AI 對話或 GitHub。
''')
    def start(title,diagram,flow,state):
        return [opening(title,diagram,flow,state),prepare,c(install),c('%%writefile day2_case.py\n# @title 寫入本章流程（按播放，不用修改）\n'+(root/'day2/procurement.py').read_text()),c(dataset),key,c(creds)]
    def restore(folder):
        return [m('### 選做：在全新 Colab 還原既有備份\n\n第一次上課跳過。若已有含輸入資料及SQLite的完整備份ZIP，可用左側「檔案 → 上傳」放入，再只填下格檔名並播放。L05可使用第4步產生的中斷現場備份。接下來照原步驟操作；程式會沿用已還原的任務，不重新建立。請用全新執行階段，不能覆蓋已有成果的資料夾。'),
                c(f'''# @title 選做：還原上次下載的ZIP（第一次執行留空）
RESTORE_ZIP = "" # @param {{type:"string"}}
if RESTORE_ZIP:
    print("已還原：",case.restore_archive(RESTORE_ZIP,"results/{folder}"))
else:
    print("第一次執行，使用新任務。")
''',False)]
    docs={}
    cells=[m('''# L03｜上傳三品牌 PDF，建立競品研究 RAG

第二天｜先看狀態圖，再依五步操作。研究主題仍是三品牌競品比較。對照投影片 PDF 173–221。

![LangGraph 狀態圖]({raw}03_rag.png)

**建資料：** 下載 HP／Lenovo／Dell 官方 PDF → 上傳 Colab → 抽取每頁文字 → 切成小段 → `text-embedding-3-small` 將每段轉成向量 → 保存本機索引。

**問問題：** 中文問題 → 同一個 embedding 模型轉成向量 → 用餘弦相似度從每份文件各取最接近的段落 → `gpt-6-luna` 回答 → 核對片段 ID 與 PDF 頁碼。問答的三個節點實際由 LangGraph 串接。

**白話理解：** embedding 是把文字轉成能比較語意的數字；它負責找資料，回答模型負責組織答案。本章真的呼叫兩種 API。向量保存在 Colab 的 JSON 索引，不必另外註冊向量資料庫。

**State 工作紀錄：** question 問題、rows 取回的頁面片段與相似度、report 回答、validation 引用檢查。建索引和問答是兩個階段；換問題不用重算整本手冊的 embedding。

**案例：** 替台灣企業120台商務筆電更新案比較 HP、Lenovo、Dell 的記憶體／SSD、重量、連接埠與維修性。交付有來源頁碼的比較表、證據不足項目與供應商問題，再接到L04研究團隊。數量為教學情境，不能假裝已有報價。

**文件界線：** 官方維修手冊／規格書是競品證據庫，不是叫你實際維修。先核對封面與版本，HP AI PC手冊不可直接當成所有Next Gen AI配置；Dell同一本型錄有200V與200U，不能把兩者的記憶體混用。上傳一份可先練流程，但缺其他品牌文件時不做完整排名。
'''.replace('{raw}',raw)),m('''## 第 1 步｜開啟 Colab，下載三品牌官方 PDF

**怎麼做：** 存一份 Colab 副本，使用 Python 3、CPU。播放下面兩格，程式預設收起，不用修改。先下載以下三份真正官方PDF到電腦，方便一起上傳：

|品牌|下載來源|建議改名|先確認什麼|
|---|---|---|---|
|HP|[EliteBook 8 G1a 14 維修手冊](https://kaas.hpcloud.hp.com/pdf-public/pdf_12237395_en-US-1.pdf)，[官方手冊清單](https://support.hp.com/us-en/product/setup-user-guides/hp-elitebook-8-g1a-14-inch-notebook-ai-pc/2102811726)|`hp_manual.pdf`|封面是14 inch Notebook AI PC；不能直接當所有Next Gen AI配置。|
|Lenovo|[ThinkPad T14 Gen 6 AMD PSREF](https://psref.lenovo.com/syspool/Sys/PDF/ThinkPad/ThinkPad_T14_Gen_6_AMD/ThinkPad_T14_Gen_6_AMD_Spec.PDF)|`lenovo_t14.pdf`|AMD、Gen 6與系列可選配置，非台灣交貨證明。|
|Dell|[Dell Pro 13／14／16 Plus官方型錄](https://www.delltechnologies.com/asset/en-gb/products/laptops-and-2-in-1s/technical-support/dell-pro-13-14-16-plus-laptop-product-brochure.pdf)|`dell_pro.pdf`|只採14吋PB14250 **Core Ultra 200V**欄位，不混用200U／其他尺寸。|

**看什麼：** 下載後用PDF閱讀器打開，核對封面／標題、型號與處理器版本。本章會從你上傳的檔案重新抽文與embedding，不用事先寫好的29筆摘述冒充讀取PDF。

**卡住時：** 官方站若擋取，老師可事先下載這三份官方文件給同學；仍需實際上傳PDF。也可先只用HP手冊學操作，或換成你有權使用、能選取文字的其他競品文件；問題也要配合改。掃描圖片需先OCR，本章不會閱讀圖片或圖表。
'''),c(install.replace('"httpx==0.28.1"]','"httpx==0.28.1","pypdf==6.21.4"]')),c('%%writefile pdf_rag.py\n# @title 寫入PDF讀取與向量檢索流程（按播放，不用修改）\n'+(root/'day2/pdf_rag.py').read_text()),key,c(creds+'''EMBEDDING_MODEL = "text-embedding-3-small"
import pdf_rag as rag
from IPython.display import display, Markdown
print("找資料的模型：", EMBEDDING_MODEL, "；寫回答的模型：", MODEL)
'''),m('''## 第 3 步｜上傳三份 PDF，確認文件庫內容

**怎麼做：** 點 Colab 左側資料夾圖示 →「上傳至工作階段儲存空間」，一次選三份PDF；等三個檔名下的上傳進度全部消失，再改下格PDF_FILES，填左側實際檔名，檔名之間用半形逗號分隔。若照上表改名，直接播放即可。不要填自己的電腦路徑。只有一份時可以先填一個檔名，但其他品牌須標缺文件。

**應該看到：** 每份檔名、PDF頁數、片段數、SHA-256及第一段文字。檢查三家都有放進去，且型號符合研究目標。本格尚未呼叫embedding。PDF第1頁指閱讀器第一頁，可能與印刷章節頁碼不同。

**為什麼切段：** 問答時只把找到的幾段交給模型，不用每次送整本手冊。預設每段1200字元、重疊200字元，並保留檔名與頁碼。文字過少的頁會列出，可能是圖片頁，不能宣稱已讀懂。表格雖保留文字間距，欄位仍可能錯位，須回PDF原頁核對。掃描檔完全沒有文字時會停止並提示OCR。

**給 AI：**「這是我上傳的手冊，請確認三品牌實際檔名與PDF型號；保留頁碼與未知資訊，只告訴我要修改哪個檔名欄位，不要替我編造文件內容。」
'''),c('''# @title 只改上傳後的PDF檔名（半形逗號分隔）
PDF_FILES = "hp_manual.pdf, lenovo_t14.pdf, dell_pro.pdf" # @param {type:"string"}
PDF_PATHS = [name.strip() for name in PDF_FILES.split(",") if name.strip()]
for path in PDF_PATHS:
    document = rag.extract_pdf(path)
    print("檔名：",document["file"],"；PDF頁數：",document["pages"],"；片段數：",len(document["rows"]))
    print("SHA-256：",document["sha256"])
    print("文字過少、未建立片段的頁：",document["empty_pages"])
    print("第一段：",document["rows"][0]["text"][:220])
'''),m('''## 第 4 步｜建立 embedding 索引，先問一個問題

**怎麼做：** 播放下格。第一次會把三份PDF的每個文字片段送到 `text-embedding-3-small`，產生向量並存進 `results/03_rag/indexes`。每一段都保留出自哪份文件與哪一頁。這些向量像資料的語意座標；問題也會轉成相同模型的向量，再從每份PDF各取最接近的5段，避免HP手冊比較長就擠掉其他品牌。最後才由 `gpt-6-luna` 寫答案。

**應該看到：** embedding模型、向量維度、段數、本次建立索引的API呼叫數，以及有頁碼的回答。索引相同時重用文件向量；換PDF、切段設定或embedding模型會建立新索引。每次提問仍會呼叫一次問題embedding與一次回答API；本步會產生課堂Key用量。

**看證據：** 下方列出實際取回的片段與相似度。相似度是排序分數，不是正確率。答案須附 `[PDF-0001]` 形式ID、檔名、PDF頁次。你要打開自己的PDF核對；引用存在不代表模型一定解讀正確。
'''),c('''# @title 建立真正的embedding索引，執行第一次PDF問答
index = await asyncio.to_thread(rag.build_index, PDF_PATHS, API_KEY, EMBEDDING_MODEL)
print("Embedding：",index["identity"]["embedding_model"],"；維度：",index["dimensions"],"；段數：",len(index["rows"]))
print("重用索引：",index["reused"],"；本次文件embedding呼叫：",len(index["embedding_calls_this_run"]))
QUESTION = "先核對上傳文件的三品牌型號與版本。比較HP、Lenovo T14 Gen 6 AMD、Dell PB14250 Core Ultra 200V的記憶體升級與SSD更換能力，做三家比較表；只用相符型號證據，附檔名、PDF頁碼和引用，缺資料列待確認。"
result_before = await asyncio.to_thread(rag.run_pdf_rag, QUESTION, index, API_KEY, MODEL, k=5, out="results/03_rag/before")
display(Markdown(result_before["report"]))
print(result_before["validation"])
for row in result_before["rows"]:
    print(row["id"],row["file"],"PDF第",row["page"],"頁；相似度",round(row["score"],3),"\\n",row["text"])
'''),m('''## 第 5 步｜只改中文問題，重跑並查證

**怎麼做：** 只改下格 NEW_QUESTION、TOP_K，再播放下兩格。預設將研究擴成「三品牌32GB／1TB、台灣120台報價和三年到府」，觀察模型是否保留手冊無法回答的缺口。也可比較三品牌USB-C、重量或記憶體配置，問題要配合上傳型號。TOP_K是每份PDF各讀幾段，可用1–12；增加段數不保證正確。

**給 AI 的指令：**「請根據我上傳的三品牌PDF，把問題改成競品研究問題，使用相同的比較欄位，要求先核對型號、附PDF頁次與引用，不把維修手冊當台灣報價或服務憑證。只回傳NEW_QUESTION一行，不改其他程式。」

**應該看到：** 沿用同一份競品文件庫索引，重新計算問題向量與回答。對照前後取回頁次，確認中文提問可找英文手冊；若找不到內容，要分清楚『本次片段不足』與『整本手冊沒有』，不能把相似段落當成證明。

**驗收：** 用PDF閱讀器跳到引用頁，確認型號、條件和原文。手冊沒有提供你的台灣正式報價與已購服務權益，答案應列供應商待確認；不應編出價格或三年到府承諾。若換PDF，回到第3步改檔名清單，再重跑第4、5步。執行階段回收後需重新上傳、輸入Key與建索引。
'''),c('''# @title 只改中文問題與要讀幾段
NEW_QUESTION = "替120台台灣企業採購比較HP、Lenovo、Dell：能確認32GB與1TB、台灣含稅報價、交期與已含三年到府嗎？做三品牌證據與缺口表，附PDF頁碼，不混用HP不同型號或Dell 200V與200U；沒有報價就列供應商問題。" # @param {type:"string"}
TOP_K = 6 # @param {type:"integer"}
'''),c('''# @title 用新的問題向量重查競品文件庫
result_after = await asyncio.to_thread(rag.run_pdf_rag, NEW_QUESTION, index, API_KEY, MODEL, k=TOP_K, out="results/03_rag/after")
display(Markdown(result_after["report"]))
print(result_after["validation"])
for row in result_after["rows"]:
    print(row["id"],row["file"],"PDF第",row["page"],"頁；相似度",round(row["score"],3),"\\n",row["text"])
print("本次問題embedding：",result_after["embedding_model"],"；回答：",result_after["generation_call"]["model"])
''')]
    docs['03_rag.ipynb']=cells
    cells=start('L04｜三品牌研究團隊與 27 格需求矩陣','04_team','Planner 規劃 → 三個品牌 Researcher 分別呼叫模型 → Writer 寫稿 → Reviewer 查核 → 最多修訂一輪。角色各有獨立輸入輸出；共用同一模型，沒有各自長期記憶。','task 任務、plan 計畫、notes 品牌交接、report 草稿、review 意見、revisions 修訂次數')
    cells += [m('''## 第 3 步｜先看研究規模，找最重要的缺口

**怎麼做：** 播放下格，看到三品牌 × 九項需求，共 27 格。這是可追溯的檢查清單，不是打分排行榜；有系列證據仍不能代表台灣 SKU 合規。

**討論：** 工程師在意可升級、業務在意重量、採購在意到府與交期，哪三件最需要供應商回答？所有品牌都沒有正式含稅報價，所以目前不能排名最便宜。
'''),c('''# @title 顯示需求矩陣（這格不呼叫模型）
matrix = case.coverage()
display(Markdown("|品牌|需求|證據ID|狀態|\\n|---|---|---|---|\\n"+"\\n".join(
    f"|{r['brand']}|{r['requirement']} {r['need']}|{r['evidence_ids'] or '無'}|{r['finding']}|" for r in matrix)))
'''),m('''## 第 4 步｜交辦完整研究，讓 AI 修改需求

**怎麼做：** 只改 TASK。先用預設採購題，或加入你負責部門的優先項目。修訂上限設 1；改 0 可比較沒有 Writer 修訂的報告。程式會依上限停止，不等所有缺口填滿。

**給 AI 的指令：**「請將120台企業採購任務寫清楚，加入〔你的部門優先需求〕。保留九項驗收、台灣市場、正式報價與服務待確認，不指定假贏家。只回傳 TASK 字串。」
'''),c('''# @title 只改這個研究任務
TASK = "替台灣企業120台更新案比較HP、Lenovo、Dell：IT看升級與雙螢幕、業務看1.5kg、採購看三年到府與交期；交主管摘要、品牌風險與供應商詢價清單。沒有台灣SKU與正式報價不可選出最便宜或已全數符合的贏家。" # @param {type:"string"}
MAX_REVISIONS = 1 # @param {type:"integer"}
print(TASK)
''',False),m('''## 第 5 步｜執行角色交接，必要時上網補查

**怎麼做：** 播放第一格，等報告與 Reviewer 意見出現。一次新研究最多8次模型呼叫，各角色開始與完成都會顯示。相同任務重跑沿用已完成角色回覆，避免逾時後整組重做；修改需求則使用新回覆。可能需要幾分鐘；不要因等待重複按播放。`trace.json` 保留各角色內容、證據 ID 與模型呼叫紀錄，`coverage.csv` 可開試算表。

**驗收：** Dell 200V 的記憶體不能升級；HP 愛爾蘭32GB/1TB不能當台灣SKU；Lenovo 保固不等於到府。Reviewer 的意見必須回到原始來源，不把 Writer 文字當新證據。達上限後仍交付未解問題。

**選做真實上網：** 下方第二格將 SEARCH_NOW 改 True，再播放。沿用老師的 Key，用模型的 web_search 搜尋官方站，最多兩次工具呼叫；保存網址與查閱時間。可能有額外搜尋費用。網站擋取或找不到台灣 SKU 就保留缺口，不可冒充查到。搜尋結果先作候選，須人工開啟核對後才可要求 AI 更新封存資料；不自動混進27格的證據。

**給 AI：**「根據 coverage.csv 和 Reviewer 意見，只列前三個最值得補查的問題、要找的官方頁面與驗收方式；不要把市場或系列能力換成已確認SKU。」
'''),c('''# @title 執行研究團隊（等待完成，避免重複播放）
team_result = await asyncio.to_thread(case.run_team,TASK,API_KEY,MODEL,MAX_REVISIONS,"results/04_research")
show(team_result)
print("需求矩陣：",len(team_result["coverage"]),"格；修訂：",team_result["revisions"],"輪")
'''),c('''# @title 選做：真的上網搜尋官方來源
SEARCH_NOW = False # @param {type:"boolean"}
SEARCH_QUESTION = "查HP EliteBook 8 G1a 14 Next Gen AI、ThinkPad T14 Gen 6 AMD、Dell PB14250 Core Ultra 200V的台灣32GB/1TB配置與三年到府服務；找不到就列供應商待確認，保留官方網址。" # @param {type:"string"}
if SEARCH_NOW:
    live_result = await asyncio.to_thread(case.live_search,SEARCH_QUESTION,API_KEY,MODEL)
    show(live_result)
    print("官方來源候選：",live_result["citations"])
else:
    print("本次使用封存的官方片段；未執行即時搜尋。")
''',False)]
    docs['04_research_loop.ipynb']=cells
    cells=start('L05｜120 台研究案中斷後接續','05_recovery','HP → Lenovo → Dell → 彙整；每個完成節點寫 checkpoint。課堂故意在 Lenovo 結果存入操作帳本後中斷，讓你看到帳本與 checkpoint 的差別。','results 已完成品牌；next 下一節點另存在 checkpoint；operations.sqlite 是已提交結果帳本')
    cells += restore('05_recovery')
    cells += [m('''## 第 3 步｜啟動批次，保留中斷現場

**怎麼做：** 播放下格。它會開一個獨立 Python 程序，實際研究 HP、Lenovo，然後在寫好 Lenovo 結果、尚未完成節點時故意停止。這個失敗是教學故障，不代表官網或模型故障。

**應該看到：** `LESSON_PAUSE_AFTER_LENOVO_EFFECT`、結束碼 23。這是預期結果；若是401、逾時或其他錯誤，程式會另報錯，不會將它當成成功中斷。準備重演時請改新的 BATCH_DIR，不要刪掉中斷進度。
'''),c('''# @title 啟動第一個 Python 程序，預期在 Lenovo 後暫停
BATCH_DIR = "results/05_recovery/batch_01"
THREAD = "procurement-120"
def run_worker(action):
    Path(BATCH_DIR).parent.mkdir(parents=True,exist_ok=True)
    env = dict(os.environ, DAY2_API_KEY=API_KEY)
    with Path(BATCH_DIR+"_"+action+".log").open("w",encoding="utf-8") as log:
        proc = subprocess.run([sys.executable,"day2_case.py",action,"--out",BATCH_DIR,"--thread",THREAD,"--model",MODEL],
                              env=env,stdout=log,stderr=log,timeout=300)
    text = Path(BATCH_DIR+"_"+action+".log").read_text()
    # 不把完整供應商錯誤／環境內容當教學輸出。
    if action=="start":
        if proc.returncode!=23 or "LESSON_PAUSE_AFTER_LENOVO_EFFECT" not in text:
            raise RuntimeError("未到預期中斷點；請在左側檔案查看 start.log 的最後錯誤，不要貼 Key。")
        print("LESSON_PAUSE_AFTER_LENOVO_EFFECT；結束碼23，預期的教學中斷。")
    elif proc.returncode:
        raise RuntimeError("恢復失敗；查看 resume.log 最後錯誤，不要貼 Key。")
    return proc.returncode
if Path(BATCH_DIR,"checkpoints.sqlite").exists():
    print("已有進度，保留現場，接著查看狀態或恢復。")
else:
    await asyncio.to_thread(run_worker,"start")
'''),m('''## 第 4 步｜只讀進度，說明為什麼不能全部重跑

**怎麼做：** 播放下格，對照完成品牌、下一節點、唯一結果筆數與執行紀錄。

**應該看到：** checkpoint 只有 HP 完成，next 是 Lenovo；操作帳本已有 HP、Lenovo 各一筆。兩者不矛盾：結果提交後、節點完成前中斷，checkpoint 還沒追上。

**給 AI：**「請根據這份中斷狀態說明應從哪個節點接續，以及哪一筆可能重進；只解釋，不刪SQLite、不改Thread、不重做已完成品牌。」同 Thread、同來源與模型才是接續，改 Thread 是新任務。
'''),c('''# @title 核對中斷現場（不呼叫模型）
paused = case.inspect_batch(BATCH_DIR)
print(json.dumps(paused,ensure_ascii=False,indent=2))
if paused["next"]:
    assert paused["completed_brands"]==["HP"]
    assert paused["next"]==["Lenovo"]
    assert paused["effects"]=={"HP":1,"Lenovo":1}
else:
    print("這份ZIP的研究已完成；第5步恢復會維持原結果，不新增模型呼叫。")
# 把中斷現場另外存成ZIP，想跨執行階段演示時可從左側檔案下載。
shutil.copytree("data_day2",Path("results/05_recovery/inputs"),dirs_exist_ok=True)
shutil.make_archive("05_recovery_中斷現場","zip","results/05_recovery")
'''),m('''## 第 5 步｜用第二個 Python 程序恢復

**怎麼做：** 播放下格，使用同 BATCH_DIR、THREAD、MODEL。這次真的是另一個程序讀 SQLite，沒有把第一個程序的記憶體變數帶過去。Lenovo 節點會重新進入，但讀回已存結果；然後才呼叫模型研究 Dell。

**應該看到：** 執行紀錄 HP → Lenovo → Lenovo（reused=True）→ Dell；唯一結果共3筆；next 變空，報告有三品牌。不能只看「恢復成功」四個字，須核對 SQLite 與紀錄。

**跨全新 Colab：** 第4步已額外產生 `05_recovery_中斷現場.zip`，可從左側「檔案」下載。重新開機時先準備程式及 Key，再用選做還原格載入這份ZIP；照第3～5步播放即可沿用原進度。若沒有保存ZIP，Colab 暫存檔回收後不能憑 Thread 名找回資料。
'''),c('''# @title 第二個 Python 程序接續同一任務
await asyncio.to_thread(run_worker,"resume")
resumed = case.inspect_batch(BATCH_DIR)
print(json.dumps(resumed,ensure_ascii=False,indent=2))
assert resumed["next"]==[] and len(resumed["completed_brands"])==3
assert resumed["effects"]=={"HP":1,"Lenovo":1,"Dell":1}
assert [e["brand"] for e in resumed["execution"]]==["HP","Lenovo","Lenovo","Dell"]
assert resumed["execution"][2]["reused"] is True
display(Markdown(Path(BATCH_DIR,"report.md").read_text()))
''')]
    docs['05_recovery.ipynb']=cells
    cells=start('L06｜來源追蹤、詢價草稿與人工審核','06_review','模型產詢價草稿 → interrupt 等人決定 → 修改再審／駁回結束／核准存本機 outbox。官網追蹤是另外的讀取檢查，不會自動核准任何草稿。','draft 收件對象、內容與需求hash；decision 決定；receipt 本機存檔回執；pending 是否等候')
    cells += restore('06_review')
    cells += [m('''## 第 3 步｜產生詢價草稿，停在人工審核

**怎麼做：** 播放下格。模型依九項需求及真實來源寫 RFQ 草稿，LangGraph 以 interrupt 暫停。這份草稿是要求供應商補報價、SKU及服務證明，不是訂購承諾。

**應該看到：** pending=True、outbox_count=0、sent_count=0，並顯示草稿及 hash。hash 是整份草稿的指紋，收件對象、內容或需求變動都會改變。使用 .invalid 教學地址，這套範例沒有寄信工具。
'''),c('''# @title 產生詢價草稿並暫停等人審核
REVIEW_DIR = "results/06_review/approval_01"
if not Path(REVIEW_DIR,"checkpoints.sqlite").exists():
    draft = await asyncio.to_thread(case.draft_rfq,"請寫給供應商的正式詢價草稿，保留未確認項，不承諾下單。",API_KEY,MODEL)
    review_state = case.approval(REVIEW_DIR,draft=draft)
else:
    review_state = case.approval(REVIEW_DIR)
show(review_state)
display(Markdown(review_state["draft"]["body"]))
'''),m('''## 第 4 步｜修改草稿，讓舊核准失效

**怎麼做：** 只改下格 ADD_REQUIREMENT 中文，例如要求報價逐項列出三年到府與交期。按播放，會保留原文、加入你的要求，再次等待審核。這是你手動修改草稿，不會再呼叫模型。

**應該看到：** hash 改變、仍 pending=True、零存檔、零寄送。內容改了，舊 hash 不能拿來核准新稿。

**給 AI：**「請將我的補充條件改寫成一句供應商可回答的詢價問題，保留台灣市場、交付SKU和服務條件，不編造報價，只回傳 ADD_REQUIREMENT 中文字串。」
'''),c('''# @title 只改這個補充要求，再送回待審
ADD_REQUIREMENT = "請將台灣三年次工作日到府服務、遠端診斷限制、可交付SKU、含稅TWD總價與承諾交期分別列項，並註明報價有效期。" # @param {type:"string"}
old_hash = review_state["hash"]
new_text = review_state["draft"]["body"]+"\\n\\n補充要求："+ADD_REQUIREMENT
review_state = case.approval(REVIEW_DIR,decision={"action":"revise","hash":old_hash,"text":new_text})
show(review_state)
display(Markdown("### 修改後的待審草稿"))
display(Markdown(review_state["draft"]["body"]))
assert review_state["pending"] and review_state["hash"]!=old_hash
assert review_state["outbox_count"]==0
''',False),m('''## 第 5 步｜決定是否核准，並讀取真實來源快照

**怎麼做：** 先閱讀新草稿，再在 DECISION 選 approve 或 reject。核准只會把指定版本存入本機 outbox 一次；駁回不存。下格也會測試舊 hash 被拒絕、重複決定不增加紀錄。

**應該看到：** approve 後 outbox_count=1、sent_count=0；reject 為0、0。要測另一分支，請改新的 REVIEW_DIR 從第3步重做，不要刪原證據。

**選做來源追蹤：** 第二格將 CHECK_WEB 改 True，會實際下載 Lenovo 官方 PSREF PDF 並保存本次時間與 SHA-256。首次建立基準；日後再執行同格比較。unchanged 是檔案沒變、content_changed_needs_review 是內容指紋變動待人工讀文件、data_error 是讀取失敗。檔案變化不能直接稱為價格下跌；失敗不能覆蓋有效基準。

**兩週後怎麼做：** 請老師保留 `results/06_review`，包括 `monitor/baseline.json`，兩週後在同目錄再播放追蹤格。Colab 暫存資料可能被回收，保存 notebook 不會保留這些檔案。教材沒有捏造歷史報價或已發生的降價，也沒有在 Colab 部署持續排程。沒有官方含稅價格和相同SKU，不能算折扣。新證據若影響已核准草稿，請用新 REVIEW_DIR 重新產稿與審核。
'''),c('''# @title 核准或駁回目前草稿（只存本機，不寄送）
DECISION = "approve" # @param ["approve","reject"]
try:
    case.approval(REVIEW_DIR,decision={"action":"approve","hash":old_hash})
    raise AssertionError("舊hash不應被接受")
except ValueError:
    print("舊hash已被拒絕。")
review_state = case.approval(REVIEW_DIR,decision={"action":DECISION,"hash":review_state["hash"]})
show(review_state)
try:
    case.approval(REVIEW_DIR,decision={"action":DECISION,"hash":review_state["hash"]})
except ValueError:
    print("重複決定已拒絕，沒有新增紀錄。")
assert review_state["outbox_count"]==(1 if DECISION=="approve" else 0)
assert review_state["sent_count"]==0
''',False),c('''# @title 選做：讀取真實官網，建立或比較追蹤基準
CHECK_WEB = False # @param {type:"boolean"}
if CHECK_WEB:
    monitor = Path("results/06_review/monitor")
    current = await asyncio.to_thread(case.fetch_snapshot)
    case.save(monitor/"latest.json",current)
    baseline_path = monitor/"baseline.json"
    if baseline_path.exists():
        old = json.loads(baseline_path.read_text())
        status = case.compare_snapshots(old,current)
        case.save(monitor/"comparison.json",{"old":old,"new":current,"status":status})
        print(status,"；有效基準未自動覆蓋。")
    elif current["status"]=="ok":
        case.save(baseline_path,current)
        print("已建立今天的真實PDF基準；日後重新執行此格比較。")
    else:
        print("data_error：沒有取得有效資料，未建立基準。")
else:
    print("本次未即時連官網；人工審核使用封存來源。")
''',False)]
    docs['06_review_monitor.ipynb']=cells
    return docs
