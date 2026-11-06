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
        return [opening(title,diagram,flow,state),m(prepare[1].replace('下面三格','下面五格')),c(install.replace('請接著播放下兩格','請接著播放其餘準備格')),c('%%writefile day2_case.py\n# @title 寫入本章流程（按播放，不用修改）\n'+(root/'day2/procurement.py').read_text()),c(dataset),key,c(creds)]
    def afternoon_cells():
        return [c('%%writefile afternoon.py\n# @title 寫入下午的比較與觀察工具（不必修改）\n'+(root/'day2/afternoon.py').read_text()), c('# @title 載入下午的觀察工具（不必修改）\nimport afternoon as lab\n')]
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
    cells=[m('''# L03｜下載三品牌 PDF，建立競品研究 RAG

第二天｜先看狀態圖，再依五步操作。研究主題仍是三品牌競品比較。對照投影片 PDF 173–221。

![LangGraph 狀態圖]({raw}03_rag.png)

**建資料：** Colab 直接下載 HP／Lenovo／Dell 官方 PDF → 抽取每頁文字 → 切成小段 → `text-embedding-3-small` 將每段轉成向量 → 存入 Chroma 向量資料庫（包含原文、檔名與頁碼）。

**問問題：** 中文問題 → 同一個 embedding 模型轉成向量 → 查詢 Chroma，以餘弦距離從每份文件各取最接近的段落，先顯示片段 → `gpt-6-luna` 回答 → 核對片段 ID 與 PDF 頁碼。問答的三個節點實際由 LangGraph 串接。

**白話理解：** embedding 是把文字轉成能比較語意的數字；它負責找資料，回答模型負責組織答案。本章真的呼叫兩種 API。Chroma 負責保存向量與搜尋，原文、檔名及頁碼也一起存入。資料存在 Colab 的 `results/03_rag/chroma` 資料夾，不用註冊雲端帳號；執行階段刪除後，這個資料夾也會消失。

**State 工作紀錄：** question 問題、rows 取回的頁面片段與相似度、report 回答、validation 引用檢查。建索引和問答是兩個階段；換問題不用重算整本手冊的 embedding。

**案例：** 替台灣企業120台商務筆電更新案比較 HP、Lenovo、Dell 的記憶體／SSD、重量、連接埠與維修性。交付有來源頁碼的比較表、證據不足項目與供應商問題，再接到L04研究團隊。數量為教學情境，不能假裝已有報價。

**文件界線：** 官方維修手冊／規格書是競品證據庫，不是叫你實際維修。先核對封面與版本，HP AI PC手冊不可直接當成所有Next Gen AI配置；Dell同一本型錄有200V與200U，不能把兩者的記憶體混用。上傳一份可先練流程，但缺其他品牌文件時不做完整排名。
'''.replace('{raw}',raw)),m('''## 第 1 步｜開啟 Colab，確認三品牌官方來源

**怎麼做：** 存一份 Colab 副本，使用 Python 3、CPU。播放下面兩格，程式預設收起，不用修改。第3步會在Colab直接下載以下三份官方PDF，不用先存電腦再上傳。下表供你確認來源與型號：

|品牌|下載來源|自動存成|先確認什麼|
|---|---|---|---|
|HP|[EliteBook 8 G1a 14 維修手冊](https://kaas.hpcloud.hp.com/pdf-public/pdf_12237395_en-US-1.pdf)，[官方手冊清單](https://support.hp.com/us-en/product/setup-user-guides/hp-elitebook-8-g1a-14-inch-notebook-ai-pc/2102811726)|`hp_manual.pdf`|封面是14 inch Notebook AI PC；不能直接當所有Next Gen AI配置。|
|Lenovo|[ThinkPad T14 Gen 6 AMD PSREF](https://psref.lenovo.com/syspool/Sys/PDF/ThinkPad/ThinkPad_T14_Gen_6_AMD/ThinkPad_T14_Gen_6_AMD_Spec.PDF)|`lenovo_t14.pdf`|AMD、Gen 6與系列可選配置，非台灣交貨證明。|
|Dell|[Dell Pro 13／14／16 Plus官方型錄](https://www.delltechnologies.com/asset/en-gb/products/laptops-and-2-in-1s/technical-support/dell-pro-13-14-16-plus-laptop-product-brochure.pdf)|`dell_pro.pdf`|只採14吋PB14250 **Core Ultra 200V**欄位，不混用200U／其他尺寸。|

**看什麼：** 可點官方連結查看封面／標題、型號與處理器版本。本章會從實際下載的PDF抽文與embedding。下載文件不需要Key，只有後續embedding與回答才使用課堂Key。

**卡住時：** 官方站若擋取，再改用第3步的備用上傳方式；已下載成功的文件會保留。也可換成能選取文字的其他競品文件，問題要配合型號。掃描圖片需先OCR，本章不會閱讀圖片或圖表。
'''),c(install.replace('"httpx==0.28.1"]','"httpx==0.28.1","pypdf==6.21.4","chromadb==1.5.9"]')),c('%%writefile pdf_rag.py\n# @title 寫入PDF讀取與向量檢索流程（按播放，不用修改）\n'+(root/'day2/pdf_rag.py').read_text()),key,c(creds+'''EMBEDDING_MODEL = "text-embedding-3-small"
import pdf_rag as rag
from IPython.display import display, Markdown, HTML
print("找資料的模型：", EMBEDDING_MODEL, "；寫回答的模型：", MODEL)
'''),m('''## 第 3 步｜按播放，直接下載並確認PDF內容

**怎麼做：** 保持 AUTO_DOWNLOAD 勾選，直接播放下格。三份PDF會從官方站同時下載到Colab；等「下載完成」及三份文件預覽出現，再執行第4步。下載可能需要一兩分鐘，重跑會沿用已完成的PDF。PDF_FILES已填好，不必修改。

**備用：下載失敗或想換文件時**，才點左側資料夾 →「上傳至工作階段儲存空間」。等上傳進度全部消失，取消勾選 AUTO_DOWNLOAD，PDF_FILES填實際檔名，多份用半形逗號分隔，再重跑本格。已下載成功的文件不用重傳；只有一份也可練流程，其他品牌列缺文件。不要填自己電腦的路徑。

**應該看到：** 每份檔名、PDF頁數、片段數、SHA-256及第一段文字。檢查三家都有放進去，且型號符合研究目標。本格尚未呼叫embedding。PDF第1頁指閱讀器第一頁，可能與印刷章節頁碼不同。

**為什麼切段：** 問答時只把找到的幾段交給模型，不用每次送整本手冊。預設每段1200字元、重疊200字元，並保留檔名與頁碼。文字過少的頁會列出，可能是圖片頁，不能宣稱已讀懂。表格雖保留文字間距，欄位仍可能錯位，須回PDF原頁核對。掃描檔完全沒有文字時會停止並提示OCR。

**給 AI：**「這是本章PDF，請確認三品牌檔名與PDF型號；保留頁碼與未知資訊，只告訴我要修改哪個檔名欄位，不要替我編造文件內容。」
'''),c('''# @title 直接下載官方PDF（預設直接播放；備用上傳才改欄位）
AUTO_DOWNLOAD = True # @param {type:"boolean"}
PDF_FILES = "hp_manual.pdf, lenovo_t14.pdf, dell_pro.pdf" # @param {type:"string"}
if AUTO_DOWNLOAD:
    downloads = await asyncio.to_thread(rag.download_pdfs)
PDF_PATHS = [name.strip() for name in PDF_FILES.split(",") if name.strip()]
for path in PDF_PATHS:
    document = rag.extract_pdf(path)
    print("檔名：",document["file"],"；PDF頁數：",document["pages"],"；片段數：",len(document["rows"]))
    print("SHA-256：",document["sha256"])
    print("文字過少、未建立片段的頁：",document["empty_pages"])
    print("第一段：",document["rows"][0]["text"][:220])
'''),m('''## 第 4 步｜先看 embedding 搜到的片段，再生成回答

**怎麼做：** 先只播放第一格。它先建立 Chroma 向量庫、顯示庫內筆數與三筆已存資料，再把中文問題轉成向量，從每份PDF各取最接近的5段。此時只搜尋，不呼叫回答模型。先看搜尋結果，再播放下一個「用剛才的片段生成第一次回答」程式格。

**應該看到：** embedding模型、1536維向量（預設模型）、Chroma資料夾、collection名稱、庫內總筆數、已存資料範例、索引是否重用，以及搜尋表：片段ID、檔名、PDF頁碼、相似度、文字預覽。表格下可逐段展開完整原文。這就是RAG「先找資料」的結果，不是模型寫的摘要。

**先停下來看：** 三個品牌都有嗎？搜到的頁面在談記憶體／SSD嗎？型號與200V／200U對嗎？挑一段打開原PDF核對。相似度只是排序分數；內容不對，請AI幫你把問題縮小後重新搜尋，別急著生成答案。相同PDF可沿用索引；搜尋用embedding，下一格寫回答才用gpt-6-luna。
'''),c('''# @title 建立Chroma向量庫，先顯示搜尋片段（尚未生成回答）
index = await asyncio.to_thread(rag.build_index, PDF_PATHS, API_KEY, EMBEDDING_MODEL)
print("Embedding：",index["identity"]["embedding_model"],"；維度：",index["dimensions"],"；段數：",index["row_count"])
print("重用索引：",index["reused"],"；本次文件embedding呼叫：",len(index["embedding_calls_this_run"]))
store = await asyncio.to_thread(rag.inspect_index, index)
print("Chroma資料夾：",store["path"],"；collection：",store["collection"],"；庫內筆數：",store["count"])
display(Markdown("### Chroma已存資料（前三筆，尚未搜尋）"))
for row in store["sample"]:
    print(row["id"],row["file"],"PDF第",row["page"],"頁：",row["text"])
QUESTION = "先核對文件的三品牌型號與版本。比較HP、Lenovo T14 Gen 6 AMD、Dell PB14250 Core Ultra 200V的記憶體升級與SSD更換能力，做三家比較表；只用相符型號證據，附檔名、PDF頁碼和引用，缺資料列待確認。"
retrieval_before = await asyncio.to_thread(rag.retrieve_pdf, QUESTION, index, API_KEY, k=5)
display(HTML(rag.retrieval_html(retrieval_before)))
print("只完成問題embedding與搜尋；尚未呼叫回答模型。")
'''),m('''### 看完搜尋結果，再按下一格播放

先展開至少一段，核對原文是否支持比較條件。下一格會把**剛才顯示的同一批片段**交給gpt-6-luna，不重新搜尋或重算問題向量。對照回答引用的ID與上表，就能看出模型用了哪些證據。回答完成後仍須核對原文，引用ID有效不等於解讀正確。
'''),c('''# @title 用剛才的片段生成第一次回答
result_before = await asyncio.to_thread(rag.run_pdf_rag, QUESTION, index, API_KEY, MODEL, k=5, out="results/03_rag/before", retrieval=retrieval_before)
display(Markdown(result_before["report"]))
print(result_before["validation"])
'''),m('''## 第 5 步｜只改中文問題，重跑並查證

**怎麼做：** 只改下格 NEW_QUESTION、TOP_K，播放參數格，再播放「先看新問題搜回的片段」。停下來對照前後片段與頁次，最後才播放「用新的搜尋結果生成回答」。預設將研究擴成三品牌32GB／1TB、台灣120台報價和三年到府，觀察是否保留文件無法證明的缺口。也可問USB-C、重量或記憶體配置。TOP_K是每份PDF各讀幾段，可用1–12；增加段數不保證正確。

**給 AI 的指令：**「請根據本章三品牌PDF，把問題改成競品研究問題，使用相同的比較欄位，要求先核對型號、附PDF頁次與引用，不把維修手冊當台灣報價或服務憑證。只回傳NEW_QUESTION一行，不改其他程式。」

**應該看到：** 沿用同一份競品文件庫索引，重新計算問題向量與回答。對照前後取回頁次，確認中文提問可找英文手冊；若找不到內容，要分清楚『本次片段不足』與『整本手冊沒有』，不能把相似段落當成證明。

**驗收：** 用PDF閱讀器跳到引用頁，確認型號、條件和原文。手冊沒有提供你的台灣正式報價與已購服務權益，答案應列供應商待確認；不應編出價格或三年到府承諾。若換PDF，回到第3步改檔名清單，再重跑第4、5步。執行階段回收後需重新下載（或上傳）、輸入Key與建索引。
'''),c('''# @title 只改中文問題與要讀幾段
NEW_QUESTION = "替120台台灣企業採購比較HP、Lenovo、Dell：能確認32GB與1TB、台灣含稅報價、交期與已含三年到府嗎？做三品牌證據與缺口表，附PDF頁碼，不混用HP不同型號或Dell 200V與200U；沒有報價就列供應商問題。" # @param {type:"string"}
TOP_K = 6 # @param {type:"integer"}
'''),c('''# @title 先看新問題搜回的片段（尚未生成回答）
retrieval_after = await asyncio.to_thread(rag.retrieve_pdf, NEW_QUESTION, index, API_KEY, k=TOP_K)
display(HTML(rag.retrieval_html(retrieval_after)))
print("先看搜回哪些頁面；下一格才生成回答。")
'''),m('''看完上表，再播放下格。若修改了問題或TOP_K，先重跑參數格與搜尋格，不能直接拿舊片段回答新問題。
'''),c('''# @title 用新的搜尋結果生成回答
result_after = await asyncio.to_thread(rag.run_pdf_rag, NEW_QUESTION, index, API_KEY, MODEL, k=TOP_K, out="results/03_rag/after", retrieval=retrieval_after)
display(Markdown(result_after["report"]))
print(result_after["validation"])
print("本次問題embedding：",result_after["embedding_model"],"；回答：",result_after["generation_call"]["model"])
''')]
    docs['03_rag.ipynb']=cells
    cells=[m('''# L04｜深度研究：規劃、搜尋、閱讀與反思補查

第二天｜台灣企業120台商務筆電採購案｜先看狀態圖，再依五步操作。對照目前投影片PDF 222–261；流程參考四月的Deep Research完整範例。

![LangGraph狀態圖]({raw}04_team.png)

**完整流程：** Planner拆子問題 → Searcher搜尋官方來源 → Reader實際讀HTML／PDF原文 → Synthesizer整合初稿 → Critic找缺口與矛盾 → 有值得公開補查的問題就回Planner → 最終報告。

**和上一章的連結：** L03先從已下載的PDF向量庫找片段；本章先拆研究方向，再到官網找新資料。三品牌仍是HP、Lenovo、Dell，研究主題仍是台灣120台筆電更新案。

**你會看到：** 子問題、實際搜尋詞、候選網址、原文讀取成功／失敗、證據ID、各子題筆記、第一輪初稿、Critic缺口、第二輪新計畫與前後差異。每段分開播放，不必讀底層程式。

**State是研究筆記：** questions累積子問題、searches搜尋與讀取帳本、evidence原文片段、readings子題筆記、synthesis初稿、critique評審、history每輪紀錄。LangGraph暫存在記憶體，讓我們停下來觀察；執行階段刪除後不會保留，跨程序恢復留到L05。

**情境：** 台灣企業要更新120台商務筆電，教學預算含稅600萬、目標2027-01-15前交貨。比較HP EliteBook 8 G1a 14 Next Gen AI、Lenovo ThinkPad T14 Gen 6 AMD與Dell PB14250 Core Ultra 200V。數量、預算與日期是教學情境；官網資料不等於台灣指定SKU、正式報價或已購服務。
'''.replace('{raw}',raw)),m('''## 第 1 步｜準備本章，認識資料起點

**怎麼做：** 存一份Colab副本，使用Python 3、CPU。由上往下播放下面四格，程式預設收起，不必修改。會放入研究流程、120台採購需求，以及7份官方來源的29筆封存摘述，其中27筆可用。

**為什麼先給封存資料：** 它是研究起點，有來源、位置、適用市場與查閱日期；接下來仍會真的搜尋、讀取官網原文。封存摘述與本次新讀到的WEB片段分開顯示，不能假裝封存資料是剛上網取得。

**看什麼：** 先看來源表。GLOBAL系列能力、IE海外SKU、TW服務政策各能證明什麼？桌機服務與未讀到正文的搜尋線索會排除。今天要補查的是證據缺口，而不是硬選出一個贏家。

**卡住時給AI：**「請依最後一段錯誤修復Colab，保留真實搜尋、原文讀取與LangGraph迴圈，只告訴我要重跑哪格。」只貼錯誤，不貼Key。
'''),c(install.replace('"httpx==0.28.1"]','"httpx==0.28.1","pypdf==6.21.4"]').replace('請接著播放下兩格','請接著播放下面三格')),
        c('%%writefile procurement.py\n# @title 寫入採購來源與共用工具（按播放，不用修改）\n'+(root/'day2/procurement.py').read_text()),
        c('%%writefile deep_research.py\n# @title 寫入深度研究迴圈（按播放，不用修改）\n'+(root/'day2/deep_research.py').read_text()),
        c(dataset.replace('import day2_case as case','import procurement as case')),key,
        c(creds+'''import deep_research as research
from IPython.display import HTML
print("本章預設會真正搜尋並讀取官方來源。")
'''),m('''## 第 3 步｜改研究任務，先看Planner拆出的子問題

**怎麼做：** 下格主要改TASK。MAX_ROUNDS預設2，可用1–3；指的是搜尋／閱讀／評審的完整研究輪數。SOURCE_MODE預設live，會真的上網，沿用課堂Key，不必再申請搜尋服務Key。snapshot只供網路故障時演練，畫面會明說沒有即時搜尋。

**給AI：**「請將120台筆電採購寫成研究任務，加入〔IT／業務／採購最在意的條件〕。要求比較三品牌、核對型號、找反證、保留台灣SKU與報價缺口。只回TASK一段，不改程式。」

播放參數格後，再播放「先產生研究計畫」。Planner只規劃，還沒有搜尋或寫報告。它會拆成三個跨品牌子題，列出規劃的搜尋字詞與查證目的。實際工具字詞會在搜尋後另外列出。

**先停下來看：** 三題是否分別涵蓋規格／維修性、行動／底座、台灣服務／商務？query有正確型號與Dell 200V嗎？計畫若偏題，請AI幫你調整TASK，再重跑這兩格。
'''),c('''# @title 只改研究任務、輪數與來源模式
TASK = "替台灣企業120台商務筆電更新案研究HP、Lenovo與Dell：比較32GB／1TB與升級維修、1.5kg出差配置、USB-C底座及雙4K螢幕、台灣三年到府；核對HP型號與Dell 200V／200U差異。主動找證據矛盾、台灣SKU與商務缺口，交主管報告與供應商問題，不編造價格、交期或合規贏家。" # @param {type:"string"}
MAX_ROUNDS = 2 # @param {type:"integer"}
SOURCE_MODE = "live" # @param ["live", "snapshot"]
print("來源模式：",SOURCE_MODE,"；最多研究輪數：",MAX_ROUNDS)
'''),c('''# @title 先產生研究計畫（此時尚未搜尋）
# 相同任務重跑本格會保留目前session；改參數才建立新研究。
settings = (TASK, MODEL, MAX_ROUNDS, SOURCE_MODE)
if globals().get("research_settings") != settings:
    session = research.ResearchSession(TASK, API_KEY, MODEL, MAX_ROUNDS, SOURCE_MODE)
    state = await asyncio.to_thread(session.advance)
    research_settings = settings
else:
    state = session.state()
display(HTML(research.plan_html(state)))
print("下一階段：",session.app.get_state(session.config).next)
'''),m('''## 第 4 步｜執行第一輪，先讀證據再看Critic

**怎麼做：** 先播放「搜尋、讀原文並評審」。每個子題會先搜官方站，最多2個候選網址，再實際GET網頁或PDF，取出相關原文交Reader。各角色開始／完成會顯示，可能需幾分鐘，不要重複按播放。

完成後先看原文帳本：哪個網址read_ok？哪個403、擋取或沒有可讀文字？只有讀取成功的內容才新增WEB片段；搜尋摘要不能冒充原文。read_ok也只代表讀到文字，還要核對型號與市場。封存片段保留原查閱日期。

接著播放「看子題筆記、初稿與Critic」。Reader按子題交筆記，Synthesizer整合，Critic回到原始片段找未回答項目、證據矛盾及不當推論。

**討論：** 挑一筆WEB片段打開原網址核對。Critic指出哪件事能再查官網？哪件事只能問供應商？例如系列支援32GB不證明台灣交貨，三年保固也不一定包含到府。分數是模型的完整性意見，不是正確率。
'''),c('''# @title 第一輪：搜尋、讀原文並評審（等待完成）
if session.state().get("history"):
    state = session.state()
    print("第一輪已完成，保留現場；下一步看補查計畫。")
else:
    state = await asyncio.to_thread(session.advance)
display(HTML(research.evidence_html(state)))
print("本輪新增原文：",state["round_added"],"段；完成子題：",len(state["readings"]))
'''),c('''# @title 看子題筆記、第一輪初稿與Critic（這格不再呼叫模型）
for note in [n for n in state["readings"] if n["round"] == 1]:
    display(Markdown("### "+note["question_id"]+"｜"+note["question"]+"\\n\\n"+note["answer"]))
display(Markdown("## 第一輪研究初稿\\n\\n"+state["history"][0]["synthesis"]))
first_round = dict(state, round=1, critique=state["history"][0]["critique"])
display(Markdown(research.critique_markdown(first_round)))
print("下一步判斷：",research.next_action(state))
'''),m('''## 第 5 步｜看重新規劃與補查，對照報告改變

**先播放「根據Critic決定下一步」：** 若有公開可補查缺口，Planner會讀Critic意見及舊問題，提出最多兩個新子題。先比較新舊搜尋詞，確認這次真的針對缺口。這就是四月範例的Re-plan。

如果資料足以形成研究報告、只剩供應商能回答的事項，或已達輪數上限，就會直接進最終報告；不為了展示第二輪而重複搜尋。第二輪沒有新證據時也會停下，保留缺口。

**再播放「完成剩餘補查與報告」：** 新子題會重新經過Searcher、Reader、Synthesizer與Critic，累積原文與筆記，再交最終報告。最後一格只讀取已完成結果，不重啟整場研究，也不重新呼叫模型。

**怎麼驗收：** 看每輪對照表，說出「Critic提了什麼 → 第二輪改查什麼 → 新增哪個原文ID → 報告改了哪個結論」。若沒有新增證據或改善，也要如實說明。核對報告引用、資料來源、研究限制與供應商問題；達上限不等於資料已充分，更不等於已取得台灣報價。

**給AI：**「請依history與原始片段，比較第一輪初稿和最終報告，列三項改變及新增證據ID；沒有證據改善就寫沒有，不只比較文句。再說下一次最值得改哪個TASK條件。」

**重跑與成本：** 相同任務／資料／模型會沿用已完成角色與搜尋快取，並顯示原查閱時間；不是每次都刷新官網。改TASK會建立新session。預設兩輪最多17次模型回應（含最多5次搜尋請求，工具實際執行次數另列）；實際可能提早停止。SOURCE_MODE=snapshot不會上網，仍會呼叫模型；課堂Key由老師提供。
'''),c('''# @title 根據Critic決定下一步，先看補查計畫
if session.state().get("report"):
    state = session.state()
elif session.app.get_state(session.config).next == ("planner",):
    state = await asyncio.to_thread(session.advance)
elif session.app.get_state(session.config).next == ("final_report",):
    state = await asyncio.to_thread(session.advance)
else:
    state = session.state()
if state.get("report"):
    print("已進最終報告；停止原因：",state["stop_reason"])
else:
    display(HTML(research.plan_html(state)))
    print("上方是新計畫；下一格才開始補查，不會重查全部舊問題。")
'''),c('''# @title 完成剩餘補查與報告（已完成時重跑不再呼叫模型）
state = await asyncio.to_thread(session.finish)
display(HTML(research.history_html(state)))
display(HTML(research.evidence_html(state)))
for note in [n for n in state["readings"] if n["round"] > 1]:
    display(Markdown("### 補查筆記 "+note["question_id"]+"\\n\\n"+note["answer"]))
if len(state["history"]) > 1:
    display(Markdown(research.critique_markdown(state)))
print("停止原因：",state["stop_reason"],"；總子題：",len(state["questions"]))
print("模型回應紀錄：",len(session.llm.log),"；沿用快取：",sum(c["used_cache"] for c in session.llm.log))
print("本次新呼叫中API回傳的搜尋工具數：",sum(c["web_search_calls"] for c in session.llm.log if not c["used_cache"]))
'''),c('''# @title 只看最終報告與引用檢查（這格不呼叫模型）
display(Markdown(state["report"]))
print(state["validation"])
print("原文與每輪紀錄：results/04_research/trace.json；引用有效仍須人工核對內容。")
''')]
    docs['04_research_loop.ipynb']=cells
    cells=start('L05｜120 台研究案中斷後接續','05_recovery','HP → Lenovo → Dell → 彙整；每個完成節點寫 checkpoint。課堂故意在 Lenovo 結果存入操作帳本後中斷，讓你看到帳本與 checkpoint 的差別。','results 已完成品牌；next 下一節點另存在 checkpoint；operations.sqlite 是已提交結果帳本')
    cells[5:5] = afternoon_cells()
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
display(Markdown(lab.recovery_table(paused)))
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

**應該看到：** 執行紀錄 HP → Lenovo → Lenovo（reused=True）→ Dell；唯一結果共3筆；next 變空，報告有三品牌。下方再接續一次，新增操作與模型呼叫都應為0；刻意用錯Thread則應先被拒絕，不執行研究。不能只看「恢復成功」四個字，須核對 SQLite 與紀錄。

**跨全新 Colab：** 第4步已額外產生 `05_recovery_中斷現場.zip`，可從左側「檔案」下載。重新開機時先準備程式及 Key，再用選做還原格載入這份ZIP；照第3～5步播放即可沿用原進度。若沒有保存ZIP，Colab 暫存檔回收後不能憑 Thread 名找回資料。
'''),c('''# @title 第二個 Python 程序接續同一任務
await asyncio.to_thread(run_worker,"resume")
resumed = case.inspect_batch(BATCH_DIR)
display(Markdown(lab.recovery_table(resumed)))
assert resumed["next"]==[] and len(resumed["completed_brands"])==3
assert resumed["effects"]=={"HP":1,"Lenovo":1,"Dell":1}
assert [e["brand"] for e in resumed["execution"]]==["HP","Lenovo","Lenovo","Dell"]
assert resumed["execution"][2]["reused"] is True
display(Markdown(Path(BATCH_DIR,"report.md").read_text()))
# 同一份已完成工作再接續，不產生新的研究操作。
before_repeat = len(resumed["execution"])
await asyncio.to_thread(run_worker,"resume")
after_repeat = case.inspect_batch(BATCH_DIR)
assert len(after_repeat["execution"])==before_repeat
print("同一任務再次恢復：新增研究操作0筆、新增模型呼叫0次。")
try:
    await asyncio.to_thread(case.run_batch,BATCH_DIR,API_KEY,MODEL,THREAD+"-wrong",resume=True)
except ValueError as error:
    if "無法恢復" not in str(error): raise
    print("錯誤Thread：已在呼叫模型前拒絕，原進度保留。")
else:
    raise AssertionError("錯誤Thread不應被接受")

''')]
    docs['05_recovery.ipynb']=cells
    cells=start('L06｜兩週變化、來源追蹤與人工審核','06_review','先讀真實官方PDF快照，再用明確標示的兩週模擬報價演練比較規則；重大變化 → 模型草擬詢價 → interrupt 等人 → 修改再審／駁回／核准存本機outbox。','比較基準與事件；draft 含收件人、正文、證據與比較附件；decision 決定；receipt 本機回執；pending 是否等候')
    cells[5:5] = afternoon_cells()
    cells += restore('06_review')
    cells += [m('''## 第 3 步｜先看來源，再比較兩週變化

**為什麼：** 投影片的完整流程是「取得新資料 → 對照有效基準 → 判斷重要性 → 決定是否交人工」。不能看到網頁改字，就直接寫成降價通知。

**先做真實觀察：** 播放第一格，Colab會實際讀取Lenovo官方PSREF PDF，顯示網址、取得時間、檔案指紋與判定。首次建立今天的有效基準；重跑才比較。取得失敗也會保留紀錄，不能覆蓋基準。指紋改變只表示檔案有變，須回原PDF查讀，不能推論價格。這段不呼叫模型。

**再做兩週規則演練：** 播放第二格。表格會明確標示「教學模擬報價」，使用模擬SKU、第一週40,000元、第二週34,000元；這不是三家品牌的官網價格或真實歷史。真實產品資料仍使用本章官方來源，規則演練的假價格不會當成詢價正文的市場事實。

**只需要改：** SECOND_WEEK_PRICE（第二週模擬價格）、ALERT_THRESHOLD（百分比門檻）。先用預設值，看見−15%進待審；之後可改39,000，觀察不達10%門檻。表格還會比較「沒有變動」「不同SKU」「讀取失敗」三種情況，不能全部當成無變化。

**應該看到：** 兩週條件與來源標示、變動率、規則、四種處理路徑；只有重大變化才建立本次待審任務。不同SKU要先補條件，讀取失敗要補查。若你改為無重大變化，後面只顯示狀態，不會新增草稿或自動核准。
'''),c('''# @title 讀取真正的官方PDF，保存有效基準與觀察歷史
monitor_result = await asyncio.to_thread(lab.monitor_once,"results/06_review/monitor")
current = monitor_result["new"]
display(Markdown("|本次觀察|結果|\\n|---|---|\\n"+"\\n".join(
    f"|{name}|{current.get(field,'未取得')}|" for name,field in
    [("官方來源","url"),("實際取得時間","fetched_at"),("PDF指紋","sha256"),("取得狀態","status")])+f"\\n|比較判定|{monitor_result['status']}|"))
print("這是真實PDF觀察；歷史報價尚未建立，不能從指紋推定降價。")
'''),c('''# @title 比較兩週教學模擬報價（這些價格不是真實產品報價）
SECOND_WEEK_PRICE = 34000 # @param {type:"number"}
ALERT_THRESHOLD = 10 # @param {type:"number"}
weeks = lab.teaching_weeks(SECOND_WEEK_PRICE,ALERT_THRESHOLD)
case.save("results/06_review/teaching_weeks.json",weeks)
display(Markdown("### 教學模擬報價｜非真實市場或歷史證據"))
display(Markdown("|欄位|第一週|第二週|\\n|---|---|---|\\n"+"\\n".join(
    f"|{field}|{weeks['first'][field]}|{weeks['second'][field]}|" for field in
    ("sku","market","currency","tax","configuration","price","observed_at","source"))))
display(Markdown("|情況|變動率|處理路徑|原因|\\n|---|---|---|---|\\n"+"\\n".join(
    f"|{r['scenario']}|{str(r.get('change_pct','—'))+'%' if 'change_pct' in r else '—'}|{r['route']}|{r['reason']}|" for r in weeks["comparisons"])))
trigger = weeks["comparisons"][0]
event_identity = case.digest({"comparison":trigger,"source":{k:current.get(k) for k in ("status","url","sha256")}})
REVIEW_DIR = "results/06_review/events/"+event_identity[:16]
review_state = None
if trigger["route"]=="重大變化待審":
    if not Path(REVIEW_DIR,"checkpoints.sqlite").exists():
        draft = await asyncio.to_thread(case.draft_rfq,"請寫給供應商的正式詢價草稿，保留未確認項，不承諾下單。價格變動只是課堂規則模擬，不得寫成真實市價或真實降價。",API_KEY,MODEL)
        draft["comparison_attachment"] = weeks
        draft["monitor_observation"] = monitor_result
        review_state = case.approval(REVIEW_DIR,draft=draft)
    else:
        review_state = case.approval(REVIEW_DIR)
    show(review_state)
    display(Markdown("**收件人：** "+review_state["draft"]["recipient"]+"；**操作：** 只保存本機詢價草稿。"))
    display(Markdown(review_state["draft"]["body"]))
else:
    print(trigger["route"],"：本次未建立待審任務。回到預設34,000可繼續審核演練。")
'''),m('''## 第 4 步｜修改草稿，讓舊版本不能放行新版

**怎麼做：** 先讀收件人、正文與上方比較附件，再只改ADD_REQUIREMENT的中文要求並播放。它會保留原文、附加你的要求，產生新指紋，回到待審，不另外呼叫模型。同一句要求重跑只會沿用，不重複附加。

**應該看到：** 新舊版本指紋、修改理由與新版正文；新稿仍pending=True、outbox_count=0、sent_count=0。下一格會真的拿舊指紋嘗試核准，確認被拒絕。指紋會把正文、收件人、比較附件與本次來源觀察一起算進去；日後來源更新影響內容，須建立新事件重新審核。

**給AI：**「請將我的條件寫成一句供應商能回答的詢價問題，保留台灣SKU、含稅報價、交期與服務適用條件，不把模擬價格當成市價；只回傳ADD_REQUIREMENT中文，不改審核程式。」

**重跑時：** 已完成核准或駁回的任務只讀既有結果；要改已結束的內容，應建立新事件，不覆寫已決定的草稿。
'''),c('''# @title 只改中文補充要求，查看版本與理由
ADD_REQUIREMENT = "請將台灣三年次工作日到府服務、遠端診斷限制、可交付SKU、含稅TWD總價與承諾交期分別列項，並註明報價有效期。" # @param {type:"string"}
if review_state is not None:
    review_state = lab.revise_once(REVIEW_DIR,ADD_REQUIREMENT)
    revision_path = Path(REVIEW_DIR,"revision.json")
    if revision_path.exists():
        revision = json.loads(revision_path.read_text())
        display(Markdown(f"|版本|指紋|\\n|---|---|\\n|修改前|{revision['old_hash']}|\\n|修改後|{revision['new_hash']}|\\n\\n修改理由：{revision['reason']}"))
    show(review_state)
    display(Markdown(review_state["draft"]["body"]))
else:
    print("本次沒有重大變化待審；不需修改或核准。")
'''),m('''## 第 5 步｜人作決定，再看三種分支與重複執行結果

**先測版本：** 播放第一格，確認舊版本核准被拒絕、新版仍待審。未改稿或任務已結束會明說，不能把「流程已結束」冒充「舊版本不符」。

**再自己決定：** 第二格DECISION預設wait，播放只會保持待審。閱讀後可選approve（核准存本機）或reject（駁回不存），在REASON填自己的理由，再播放。會保存指定版本、收件人、理由與結果；重跑不新增存檔。等待不會自動變成同意。這是課堂審核介面，沒有登入身分、權限驗證或正式郵件寄送。

**最後比較三條分支：** 第三格在三份獨立測試任務重用同一草稿，當作自動分支演練；不會替你決定上面的主審核任務。看approve一筆、revise改稿再審後一筆、reject零筆；每條都重複執行一次，筆數維持不變，sent_count全部是0。不額外呼叫模型。

**下週如何接續：** 本章保存真實PDF基準、每次觀察與本次模擬事件；沒有捏造真實兩週價格，也沒有部署排程。正式每週追蹤需外部排程器、Asia/Taipei時間、持久磁碟與重疊處理；中斷恢復沿用同一Thread，新一週研究另建Thread。Colab關機後不會自動醒來執行，存notebook也不會保存SQLite。需要跨執行階段時，保留整份results/06_review及輸入資料，再用前面還原格讀回。
'''),c('''# @title 核對舊版本無法核准新版本（不呼叫模型）
if review_state is not None:
    review_state = case.approval(REVIEW_DIR)
    revision_path = Path(REVIEW_DIR,"revision.json")
    if review_state["pending"] and revision_path.exists():
        revision = json.loads(revision_path.read_text())
        try:
            case.approval(REVIEW_DIR,decision={"action":"approve","hash":revision["old_hash"]})
        except ValueError as error:
            if "草稿已更動" not in str(error): raise
            print("舊版本核准被拒絕；新版仍待審，零新增存檔。")
        else:
            raise AssertionError("舊版本不應被核准")
    else:
        print("尚未改稿或任務已結束；本格未做舊版本測試。")
else:
    print("沒有待審任務。")
'''),c('''# @title 選擇等待、核准或駁回，填寫自己的理由
DECISION = "wait" # @param ["wait","approve","reject"]
REASON = "已核對收件人、來源與未確認項，本次僅保存詢價草稿。" # @param {type:"string"}
if review_state is not None:
    review_state = lab.decide_once(REVIEW_DIR,DECISION,REASON)
    show(review_state)
    print("待審" if review_state["pending"] else "任務已結束，重跑沿用既有決定。")
else:
    print("沒有重大變化，不建立審核操作。")
'''),c('''# @title 自動演練三種分支與重複執行（獨立測試，不改上面的決定）
if review_state is not None:
    branches = lab.exercise_branches(Path(REVIEW_DIR)/"branch_exercises",review_state["draft"])
    display(Markdown("|測試分支|首次存檔|再次執行後存檔|實際寄送|\\n|---|---|---|---|\\n"+"\\n".join(
        f"|{r['branch']}|{r['outbox_count']}|{r['repeat_outbox_count']}|{r['sent_count']}|" for r in branches)))
    print("三種分支已驗證；主審核任務保持你的決定，模擬價格不能當真實報價。")
else:
    print("回到預設模擬價格34,000，建立待審後再演練。")
''')]
    docs['06_review_monitor.ipynb']=cells
    return docs
