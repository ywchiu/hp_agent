"""第一天下午 Colab：每個執行步驟都先用白話說明。"""
import json
from pprint import pformat


def day1_lessons(root):
    raw = 'https://raw.githubusercontent.com/ywchiu/hp_agent/main/workshop_20261105/day1/assets/'
    agent = (root/'day1/research_agent.py').read_text().split("if __name__ == '__main__':")[0]
    products = (root/'data/products.json').read_text()
    skill = (root/'day1/SKILL.md').read_text()
    install = '''# @title 啟動範例（按播放，不用改程式）
import os, sys, subprocess
if os.environ.get("HP_WORKSHOP_SKIP_INSTALL") != "1":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q",
        "openai==3.46.0", "langgraph==1.2.19", "mcp==1.30.0"])
print("範例已就緒。下一步輸入老師提供的 Key。")
'''
    core = '# @title 研究助理原始碼（不必修改；可展開閱讀）\n'+agent
    dataset = '# @title 放入教學資料（不必修改）\nproducts = '+pformat(json.loads(products), sort_dicts=False)+'''\nPath("products.json").write_text(json.dumps(products, ensure_ascii=False), encoding="utf-8")
from IPython.display import Markdown, display
def show_result(result):
    display(Markdown(result["report"]))
    print("模型呼叫次數：", result["model_calls"])
    print("實際工具紀錄：")
    for entry in result["tool_log"]:
        print(entry["transport"], entry["tool"], entry["arguments"], "→", entry["result"].get("status"))
display(Markdown("|資料 ID|市場|記憶體 GB|儲存 GB|保固年數|更新日期|\\n|---|---|---:|---:|---|---|\\n" +
    "\\n".join(f"|{p['id']}|{p['market']}|{p['memory_gb']}|{p['storage_gb']}|{p['warranty_years'] if p['warranty_years'] is not None else '缺資料'}|{p['updated']}|" for p in products)))
'''
    skill_code = '# @title 研究規則（本章請修改這段白話文字）\nresearch_skill = """\n'+skill+'"""\nPath("SKILL.md").write_text(research_skill, encoding="utf-8")\nprint(research_skill)\n'
    credentials = '''# @title 輸入老師提供的 API Key（執行時輸入，不寫在程式裡）
API_KEY = getpass("貼上老師提供的 API Key，然後按 Enter：").strip()
if not API_KEY:
    raise ValueError("還沒有輸入 Key；請重跑這一格。")
MODEL = "gpt-4.1-mini" # @param {type:"string"}
print("Key 已暫存於本次執行階段；不顯示、不存入報告。模型：", MODEL)
'''
    prepare = '''## 第 1 步｜開啟範例，按播放鍵

**為什麼做：** 讓這份 Colab 自己準備研究助理，直接從第一個範例開始。

**怎麼做：** 點「檔案 → 在雲端硬碟中儲存副本」，使用 Python 3、CPU 即可。若右上顯示「連線」，先按連線。依序按下面三格左側的 ▶，等每格完成再往下。它們預設收起，不用修改；想看原始碼才展開。

**應該看到：** 最後出現三筆模擬產品的小表格。TW 是台灣、US 是美國。台灣 32 GB 那筆保固缺資料；美國版的 3 年不能拿來補台灣版。

**如果卡住，可貼給 AI：**「我在 Colab 執行第一步，最後一段錯誤是：〔貼錯誤文字〕。請先說明原因，再告訴我只要重跑哪一格。保留目前教材，不要改產品事實。」只貼錯誤，不貼 Key。若提示重新啟動執行階段，重啟後從本步重新依序播放。
'''
    key_help = '''## 第 2 步｜輸入老師提供的 Key

**為什麼做：** 接下來會真的呼叫模型 API，讓模型判斷要用哪個工具。產品資料是模擬的，模型回答會依需求產生。

**怎麼做：** 按下格 ▶，在執行時跳出的輸入框貼上老師當堂提供的 Key，按 Enter。輸入不會顯示。每份 notebook 都要輸入一次；模型名稱依老師指定調整，預設為 `gpt-4.1-mini`。不用自己申請 Key。

**應該看到：**「Key 已暫存於本次執行階段」。執行階段重啟後需重新輸入。不要把 Key 寫進程式碼、AI 對話或分享的 notebook。

**如果卡住：** 401 先請老師確認 Key；429 請老師確認額度／課堂用量，稍後再試；找不到模型請照老師提供的名稱修改 MODEL。提供錯誤代碼與模型名稱即可，不需貼完整 Key。
'''
    export_help = '''## 第 6 步｜保存成果，確認自己真的完成

**為什麼做：** 儲存 notebook 只會保留文字和程式，不會替你保留 Colab 暫存資料夾。

**怎麼做：** 按下格 ▶ 下載本章成果 ZIP。裡面有修改前後的 `report.md`、`research_log.json` 與研究問題；Skill 章另附規則，MCP 章另附 SQLite，沒有 API Key。確認你能說出：我改了什麼、模型查過什麼、哪一項仍不能確定。

**應該看到：** 下載一份 ZIP；解壓後能讀到兩次報告。沒有自動下載時，到左側「檔案」找同名 ZIP，按右側選單下載。

**請 AI 幫忙檢查：**「請比較兩份報告與研究問題，逐項指出符合與不符合處。核對市場、資料 ID、日期和未知值；不要補沒有證據的數字。」只提供報告與問題，不提供 Key。
'''

    def m(text): return ('markdown', text, False)
    def c(text, folded=True): return ('code', text, folded)
    def opening(title, diagram, explanation):
        return m(f'# {title}\n\n第一天下午｜教材 v0.2.0｜每次只改指定欄位。\n\n'
                 f'![LangGraph 狀態圖]({raw}{diagram}.png)\n\n{explanation}\n\n'
                 '**看圖方式：** 箭頭是工作順序；State 是助理隨身帶著的工作紀錄。'
                 '模型讀問題與已有證據，要求工具就走下方，再帶資料回模型；沒有工具要求就交付回答。'
                 '第六次仍要求工具便停止並回報未完成。END 代表流程結束，仍要核對回答是否合格。\n\n'
                 '|狀態裡存什麼|白話意思|\n|---|---|\n|messages|你的問題、模型回覆、工具查到的資料|\n'
                 '|calls / tool_log|這次要用的工具／實際用過的工具與結果|\n|turns / report|模型已被問幾次／最後的回答|\n\n'
                 '**本章資料界線：** DemoBook 是教學假產品，沒有即時上網。LangGraph 與工具會實際執行；'
                 '研究時使用老師提供的 Key 呼叫模型。回答可能每次不同，以資料核對為準。')

    task = '比較 DemoBook A 台灣版 16 GB 與 32 GB 的記憶體、儲存與保固；附資料 ID 與更新日期。'
    scenarios = [
        ('01_first_research.ipynb', 'L01｜讓 AI 完成第一份產品研究', '01_research_state', '01_research', False, False),
        ('02_skill_mcp.ipynb', 'L02A｜把研究方法變成 Skill', '02_skill_state', '02_skill', True, False),
        ('02b_company_database.ipynb', 'L02B｜用 MCP 查詢企業資料庫', '02b_mcp_state', '02b_mcp', True, True),
    ]
    lessons = {}
    for filename, title, diagram, folder, use_skill, use_mcp in scenarios:
        explanation = ('這章的變化：工具改走 **MCP Client → Server → SQLite**，模型與 Skill 繼續沿用。'
                       if use_mcp else '這章的變化：每次模型呼叫都讀取白話規則。規則是方法，JSON 是事實。'
                       if use_skill else '先看圖，再做第一份研究。你交辦需求，模型決定查哪些工具。')
        cells = [opening(title, diagram, explanation), m(prepare), c(install), c(core), c(dataset)]
        if use_mcp:
            cells += [m('''### 本章多做一件事：啟動資料庫工具

按下格 ▶。它把可閱讀的 MCP 服務原始碼放進這次執行階段；研究開始時自動啟動服務、探索工具並建立教學 SQLite，不需要寫 SQL 或設定伺服器。完成會顯示 `Writing company_database.py` 或 `Overwriting company_database.py`。

本章只提供兩個查詢工具。若啟動失敗，貼最後一段錯誤給 AI：「請修復 MCP 連線，保留工具名稱與唯讀查詢，不可改成直接讀 JSON 冒充 MCP。」'''),
                      c('%%writefile company_database.py\n'+(root/'day1/company_database.py').read_text())]
        cells += [m(key_help), c(credentials)]
        cells += [m('''## 第 3 步｜先交辦一次，留下比較基準

**為什麼做：** 先看看助理會交出什麼，才能判斷修改後是否更符合需求。

**怎麼做：** 下格先不改，直接按 ▶。問題已指定 DemoBook A、台灣版、16 GB 與 32 GB。等回答出現後，對照第 1 步資料表。

**應該看到：** 中文比較表、資料 ID 與日期。台灣 16 GB 保固 1 年；台灣 32 GB 保固未知／待確認。表格下會列模型呼叫次數與實際工具名稱。起始報告存到 `before`，修改版不會蓋掉它。

**若不合格，給 AI 的指令：**「這份報告把〔指出錯誤〕寫錯了。請依教材資料修正研究問題或研究規則，保留來源 ID、日期與未知值；只回傳需要替換的那一格，不修改底層工具。」
'''+ ('\n這一回先不載入 Skill；下一步才加入，產品資料保持相同。' if use_skill and not use_mcp else '\n本章兩次都使用相同 Skill 與 MCP；比較研究問題的改變。' if use_mcp else ''))]
        if use_mcp:
            cells += [m('先載入上章的白話規則。這格不用改；執行後會顯示完整內容，請先讀一遍。'), c(skill_code)]
        cells += [c(f'''# @title 跑第一份研究（先不用改）
TASK = {task!r}
LESSON_OUT = Path("results/{folder}")
result_before = await run_research(TASK, api_key=API_KEY, model=MODEL,
    skill={'research_skill' if use_mcp else "''"}, mcp_server={"'company_database.py'" if use_mcp else 'None'}, output_dir=LESSON_OUT/"before")
show_result(result_before)
''')]
        if use_skill and not use_mcp:
            cells += [m('''## 第 4 步｜只改白話研究規則

**為什麼做：** Skill 是可以重複使用的工作方法。這裡把 `SKILL.md` 完整文字傳給模型，不依賴 Colab 自動安裝平台 Skill。

**怎麼做：** 讀下格 `research_skill` 三個引號中間的內容。在裡面加一句：「最後請用三句話，向沒有技術背景的採購主管說明差異與尚缺的證據。」其他程式不用改。按 ▶ 後存成 `SKILL.md` 並顯示規則。

**應該看到：** 原有規則仍在，新規則出現在顯示內容裡。不要把產品保固或價格寫成你希望的答案。

**複製給 AI：**「請只修改 research_skill 的白話內容，加入三句主管摘要，保留不同市場不可混用、缺資料待確認、來源 ID 與更新日期。回傳完整 research_skill 儲存格，其他程式不改。」

有 Colab AI 編輯功能時可選這格請它改；沒有時，把這格與上述指令貼給 Antigravity，再貼回 AI 回傳的那一格。不要把 Key 儲存格一起貼過去。
'''), c(skill_code, False)]
        else:
            new_task = ('請讀取資料 ID DEMO-TW-999，說明能確認的規格、缺少什麼資料，以及下一步要問誰；不得用其他 ID 代替。'
                        if use_mcp else '請向採購主管比較 DemoBook A 台灣版 16 GB 與 32 GB，保留來源 ID、更新日期與待確認，並補上採購前要問的三個問題。')
            cells += [m('''## 第 4 步｜只改研究問題，請 AI 幫你改寫

**為什麼做：** 練習把需求交代清楚，再看助理是否照做。

**怎麼做：** 下格 `NEW_TASK` 是唯一要改的地方。直接改引號裡的中文，或使用表單欄位。先用範例，再換你的要求；不要刪引號，也不用改工具。按 ▶ 記錄新問題，下一步才研究。

**複製給 AI：**「請把研究問題改寫清楚：我要〔填需求〕，範圍是 DemoBook A 台灣版，結果保留來源 ID、日期與未知值。只回傳 NEW_TASK 這一行，不改工具或資料。」

**應該看到：** 新問題印在下面。確認 AI 沒有替你改市場、換產品或添加任務。
'''+ ('\n**本章特別測試：** 範例問不存在的 ID。預期 MCP 回傳 `not_found`，助理應說查不到。查不到資料與服務斷線是兩種狀況。' if use_mcp else '')),
                      c(f'# @title 改這一個研究問題\nNEW_TASK = {json.dumps(new_task, ensure_ascii=False)} # @param {{type:"string"}}\nprint(NEW_TASK)\n', False)]
        cells += [m('''## 第 5 步｜重跑，核對修改是否生效

**為什麼做：** AI 說「改好了」還不算完成，要以新的輸出驗收。

**怎麼做：** 按下格 ▶，成果另存 `after`。對照前後報告：範圍正確嗎？來源 ID、日期保留嗎？未知值仍保留嗎？新要求採用了嗎？工具先後與呼叫次數可能不同。

**應該看到：**
'''+ ('- 同一問題加入新規則後，報告符合主管摘要和採購問題要求。\n- 若原稿本來已正確，如實說明格式／方法改了什麼，不製造假的資料改善。'
         if use_skill and not use_mcp else '- 工具紀錄標示 `mcp`，查不存在的 ID 看到 `not_found`。\n- 回答承認查不到，列出補查問題，不能冒出其他配置的規格。'
         if use_mcp else '- 回應新增的採購問題，資料仍是兩筆台灣配置。\n- 32 GB 保固仍待確認；寫成 3 年就沒有通過驗收。')+
'''

**若改了卻沒變：** 確認第 4 步已重跑，再重跑本步。將新問題／規則及兩份報告交給 AI：「請找出未採用的要求，只修改問題或規則，保留產品事實，再告訴我重跑哪兩格。」可反覆修訂直到合格。
''')]
        after = f'''# @title 用修改後的需求或規則重跑
result_after = await run_research({'TASK' if use_skill and not use_mcp else 'NEW_TASK'}, api_key=API_KEY, model=MODEL,
    skill={'research_skill' if use_skill else "''"}, mcp_server={"'company_database.py'" if use_mcp else 'None'}, output_dir=LESSON_OUT/"after")
show_result(result_after)
(LESSON_OUT/"questions.txt").write_text("修改前："+TASK+"\\n修改後："+{'TASK' if use_skill and not use_mcp else 'NEW_TASK'}, encoding="utf-8")
'''
        if use_skill:
            after += '(LESSON_OUT/"SKILL.md").write_text(research_skill, encoding="utf-8")\n'
        after += 'print("修改後成果已另存；請與上方起始報告比較。")\n'
        cells += [c(after), m(export_help), c('''# @title 下載本章成果（不含 Key）
import shutil
artifact = shutil.make_archive(str(LESSON_OUT), "zip", LESSON_OUT)
try:
    from google.colab import files
except ImportError:
    print("成果 ZIP：", artifact)
else:
    files.download(artifact)
''')]
        lessons[filename] = cells
    return lessons
