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

第二天｜台灣企業 120 台商務筆電採購案｜先看狀態圖，再依六步操作。

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
        return [m('### 選做：在全新 Colab 還原上次的成果 ZIP\n\n第一次上課跳過。若要接續上次進度，先用左側「檔案 → 上傳」放入ZIP，再只填下格檔名並播放。接下來照原步驟操作；程式會沿用已還原的任務，不重新建立。請用全新執行階段，不能覆蓋已有成果的資料夾。'),
                c(f'''# @title 選做：還原上次下載的ZIP（第一次執行留空）
RESTORE_ZIP = "" # @param {{type:"string"}}
if RESTORE_ZIP:
    print("已還原：",case.restore_archive(RESTORE_ZIP,"results/{folder}"))
else:
    print("第一次執行，使用新任務。")
''',False)]
    def export(folder):
        return [m('''## 第 6 步｜下載成果並互相驗收

**怎麼做：** 播放下格，下載本章 ZIP。裡面包含需求副本、來源及片段、這次報告和流程紀錄；不含 Key。沒有自動下載時，從 Colab 左側「檔案」下載同名 ZIP。保存 notebook 不會保留暫存資料夾，所以離開前要下載。

**交給同學檢查：** 一項有依據的發現、一項仍待確認的條件，以及你修改需求後輸出改變的證據。將報告、片段與需求交給 AI：「請逐項核對結論、適用市場、配置、引用與未知值，列出仍需人工確認的問題。」不要以文字流暢當成驗收通過。

L05／L06 的 ZIP 另含 checkpoint 與操作 SQLite。要在全新 Colab 接續，先播放第 1、2 步，再用「選做：還原上次下載的ZIP」格還原。L05按原順序往下會沿用既有進度，L06從第3步讀回待審稿；已結束的審核不能再次修改，需開新REVIEW_DIR。原Thread、模型和需求必須保持相同。程式不會自動把 Colab 暫存檔備份到雲端。
'''),c(f'''# @title 下載本章成果
EXPORT_DIR = Path("results/{folder}")
shutil.copytree("data_day2", EXPORT_DIR/"inputs", dirs_exist_ok=True)
archive = shutil.make_archive("{folder}_成果", "zip", EXPORT_DIR)
print("成果：", archive)
try:
    from google.colab import files
    files.download(archive)
except ImportError:
    print("本機執行：ZIP 已存於目前目錄。")
''')]
    docs={}
    cells=start('L03｜用真實官網片段做 RAG 查證','03_rag','問題 → 詞彙檢索 → 模型回答 → 引用 ID 檢查。這是檢索後生成；未使用向量資料庫或 embedding。','question 問題、rows 取回片段、report 回答、validation 引用檢查')
    cells += [m('''## 第 3 步｜先跑一次，觀察資料是否足夠

**怎麼做：** 先不改下格，播放後閱讀報告與 `validation`。這次只取 4 段，問題卻涵蓋三品牌；資料不足應保留待確認，不能靠模型記憶補答案。

**應該看到：** 每筆取回片段的 ID、範圍與原文位置。ID 檢查通過只代表引用存在，仍須點官網確認這段真的支持結論。若資料不足，應提出補查問題。
'''),c('''# @title 第一份 RAG 研究（先不用改）
QUESTION = "比較三品牌的記憶體升級、台灣三年到府保固與出差重量；能直接買120台嗎？"
result_before = await asyncio.to_thread(case.run_rag, QUESTION, API_KEY, MODEL, k=4, out="results/03_rag/before")
show(result_before)
display(Markdown(case.context(result_before["rows"])))
'''),m('''## 第 4 步｜改問題與閱讀範圍

**怎麼做：** 只改下格中文問題與片段數。先聚焦 Lenovo、台灣三年到府與不同配置重量；片段數改成 10。這次讓資料量配合問題範圍，其他程式不動。

**給 AI 的指令：**「請把研究問題縮小到 Lenovo ThinkPad T14 Gen 6 AMD，要求區分筆電／桌機服務及不同配置重量，保留來源 ID 與待確認；只回傳 NEW_QUESTION 與 TOP_K 兩行。」

**先預測：** 1.38 kg 與 1.59 kg 可以同時成立嗎？桌機次工作日到府能拿來證明筆電服務嗎？
'''),c('''# @title 只改這裡的中文問題與片段數
NEW_QUESTION = "Lenovo ThinkPad T14 Gen 6 AMD 黑色／灰色配置都低於1.5kg嗎？台灣筆電三年保固等於次工作日到府嗎？請保留條件、引用與供應商問題。" # @param {type:"string"}
TOP_K = 10 # @param {type:"integer"}
print(NEW_QUESTION, TOP_K)
''',False),m('''## 第 5 步｜重跑，檢查改善與排除理由

**怎麼做：** 播放下格。比較前後報告，對照 Lenovo PSREF 第 5 頁與台灣服務頁「筆記型電腦」章節。下面另列同一問題的未篩選候選與實際排除片段。

**應該看到：** Lenovo 有些灰色配置超過 1.5 kg；筆電保固頁不能支持三年次工作日到府。桌機片段及僅索引線索被排除。海外 SKU 和全球系列仍可當候選能力證據，不能轉成台灣已出貨的結論。加大 k 不保證正確，只是讓模型多讀片段。

**驗收：** 前後答案都可能謹慎；如實寫改善的是涵蓋率／條件說明，不要製造原稿一定錯的說法。
'''),c('''# @title 重跑 RAG 並檢查篩選
result_after = await asyncio.to_thread(case.run_rag, NEW_QUESTION, API_KEY, MODEL, k=TOP_K, brand="Lenovo", out="results/03_rag/after")
show(result_after)
print("未篩選候選：", [r["id"] for r in case.retrieve(NEW_QUESTION,10,filtered=False)])
print("排除：", [(r["id"],r["scope"]) for r in case.corpus() if not case.eligible(r)])
case.save("results/03_rag/questions.json", {"before":QUESTION,"after":NEW_QUESTION,"k":TOP_K})
''')]+export('03_rag')
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
''',False)]+export('04_research')
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
''')]+export('05_recovery')
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

**兩週後怎麼做：** 今天下載成果ZIP；兩週後在同目錄還原 `monitor/baseline.json` 再播放追蹤格。教材沒有捏造歷史報價或已發生的降價，也沒有在 Colab 部署持續排程。沒有官方含稅價格和相同SKU，不能算折扣。新證據若影響已核准草稿，請用新 REVIEW_DIR 重新產稿與審核。
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
''',False)]+export('06_review')
    docs['06_review_monitor.ipynb']=cells
    return docs
