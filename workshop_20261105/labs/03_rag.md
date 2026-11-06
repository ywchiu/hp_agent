# L03｜上傳三品牌 PDF，建立競品研究 RAG

第二天｜先看狀態圖，再依五步操作。研究主題仍是三品牌競品比較。對照投影片 PDF 173–221。

![LangGraph 狀態圖](https://raw.githubusercontent.com/ywchiu/hp_agent/main/workshop_20261105/day2/assets/03_rag.png)

**建資料：** 下載 HP／Lenovo／Dell 官方 PDF → 上傳 Colab → 抽取每頁文字 → 切成小段 → `text-embedding-3-small` 將每段轉成向量 → 保存本機索引。

**問問題：** 中文問題 → 同一個 embedding 模型轉成向量 → 用餘弦相似度從每份文件各取最接近的段落 → `gpt-6-luna` 回答 → 核對片段 ID 與 PDF 頁碼。問答的三個節點實際由 LangGraph 串接。

**白話理解：** embedding 是把文字轉成能比較語意的數字；它負責找資料，回答模型負責組織答案。本章真的呼叫兩種 API。向量保存在 Colab 的 JSON 索引，不必另外註冊向量資料庫。

**State 工作紀錄：** question 問題、rows 取回的頁面片段與相似度、report 回答、validation 引用檢查。建索引和問答是兩個階段；換問題不用重算整本手冊的 embedding。

**案例：** 替台灣企業120台商務筆電更新案比較 HP、Lenovo、Dell 的記憶體／SSD、重量、連接埠與維修性。交付有來源頁碼的比較表、證據不足項目與供應商問題，再接到L04研究團隊。數量為教學情境，不能假裝已有報價。

**文件界線：** 官方維修手冊／規格書是競品證據庫，不是叫你實際維修。先核對封面與版本，HP AI PC手冊不可直接當成所有Next Gen AI配置；Dell同一本型錄有200V與200U，不能把兩者的記憶體混用。上傳一份可先練流程，但缺其他品牌文件時不做完整排名。


程式格請在[本章Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/03_rag.ipynb)播放；Antigravity貼[本章指令](../prompts/04_rag.txt)。建議50分鐘。

## 第 1 步｜開啟 Colab，下載三品牌官方 PDF

**怎麼做：** 存一份 Colab 副本，使用 Python 3、CPU。播放下面兩格，程式預設收起，不用修改。先下載以下三份真正官方PDF到電腦，方便一起上傳：

|品牌|下載來源|建議改名|先確認什麼|
|---|---|---|---|
|HP|[EliteBook 8 G1a 14 維修手冊](https://kaas.hpcloud.hp.com/pdf-public/pdf_12237395_en-US-1.pdf)，[官方手冊清單](https://support.hp.com/us-en/product/setup-user-guides/hp-elitebook-8-g1a-14-inch-notebook-ai-pc/2102811726)|`hp_manual.pdf`|封面是14 inch Notebook AI PC；不能直接當所有Next Gen AI配置。|
|Lenovo|[ThinkPad T14 Gen 6 AMD PSREF](https://psref.lenovo.com/syspool/Sys/PDF/ThinkPad/ThinkPad_T14_Gen_6_AMD/ThinkPad_T14_Gen_6_AMD_Spec.PDF)|`lenovo_t14.pdf`|AMD、Gen 6與系列可選配置，非台灣交貨證明。|
|Dell|[Dell Pro 13／14／16 Plus官方型錄](https://www.delltechnologies.com/asset/en-gb/products/laptops-and-2-in-1s/technical-support/dell-pro-13-14-16-plus-laptop-product-brochure.pdf)|`dell_pro.pdf`|只採14吋PB14250 **Core Ultra 200V**欄位，不混用200U／其他尺寸。|

**看什麼：** 下載後用PDF閱讀器打開，核對封面／標題、型號與處理器版本。本章會從你上傳的檔案重新抽文與embedding，不用事先寫好的29筆摘述冒充讀取PDF。

**卡住時：** 官方站若擋取，老師可事先下載這三份官方文件給同學；仍需實際上傳PDF。也可先只用HP手冊學操作，或換成你有權使用、能選取文字的其他競品文件；問題也要配合改。掃描圖片需先OCR，本章不會閱讀圖片或圖表。


## 第 2 步｜輸入課堂 Key

**怎麼做：** 播放下格，在輸入框貼上老師提供的 Key，按 Enter。預設模型是 `gpt-6-luna`，不用自己申請 Key。每份 notebook 都需輸入，執行階段結束後會消失。

**應該看到：** Key 已暫存與模型名稱，不會顯示 Key。本章真的呼叫模型，重跑會產生用量。401 請老師確認 Key；429 請老師確認課堂額度；模型不存在時使用老師指定名稱。只回報錯誤碼，不貼 Key，不要將 Key 放進 AI 對話或 GitHub。


## 第 3 步｜上傳三份 PDF，確認文件庫內容

**怎麼做：** 點 Colab 左側資料夾圖示 →「上傳至工作階段儲存空間」，一次選三份PDF；等三個檔名下的上傳進度全部消失，再改下格PDF_FILES，填左側實際檔名，檔名之間用半形逗號分隔。若照上表改名，直接播放即可。不要填自己的電腦路徑。只有一份時可以先填一個檔名，但其他品牌須標缺文件。

**應該看到：** 每份檔名、PDF頁數、片段數、SHA-256及第一段文字。檢查三家都有放進去，且型號符合研究目標。本格尚未呼叫embedding。PDF第1頁指閱讀器第一頁，可能與印刷章節頁碼不同。

**為什麼切段：** 問答時只把找到的幾段交給模型，不用每次送整本手冊。預設每段1200字元、重疊200字元，並保留檔名與頁碼。文字過少的頁會列出，可能是圖片頁，不能宣稱已讀懂。表格雖保留文字間距，欄位仍可能錯位，須回PDF原頁核對。掃描檔完全沒有文字時會停止並提示OCR。

**給 AI：**「這是我上傳的手冊，請確認三品牌實際檔名與PDF型號；保留頁碼與未知資訊，只告訴我要修改哪個檔名欄位，不要替我編造文件內容。」


## 第 4 步｜建立 embedding 索引，先問一個問題

**怎麼做：** 播放下格。第一次會把三份PDF的每個文字片段送到 `text-embedding-3-small`，產生向量並存進 `results/03_rag/indexes`。每一段都保留出自哪份文件與哪一頁。這些向量像資料的語意座標；問題也會轉成相同模型的向量，再從每份PDF各取最接近的5段，避免HP手冊比較長就擠掉其他品牌。最後才由 `gpt-6-luna` 寫答案。

**應該看到：** embedding模型、向量維度、段數、本次建立索引的API呼叫數，以及有頁碼的回答。索引相同時重用文件向量；換PDF、切段設定或embedding模型會建立新索引。每次提問仍會呼叫一次問題embedding與一次回答API；本步會產生課堂Key用量。

**看證據：** 下方列出實際取回的片段與相似度。相似度是排序分數，不是正確率。答案須附 `[PDF-0001]` 形式ID、檔名、PDF頁次。你要打開自己的PDF核對；引用存在不代表模型一定解讀正確。


## 第 5 步｜只改中文問題，重跑並查證

**怎麼做：** 只改下格 NEW_QUESTION、TOP_K，再播放下兩格。預設將研究擴成「三品牌32GB／1TB、台灣120台報價和三年到府」，觀察模型是否保留手冊無法回答的缺口。也可比較三品牌USB-C、重量或記憶體配置，問題要配合上傳型號。TOP_K是每份PDF各讀幾段，可用1–12；增加段數不保證正確。

**給 AI 的指令：**「請根據我上傳的三品牌PDF，把問題改成競品研究問題，使用相同的比較欄位，要求先核對型號、附PDF頁次與引用，不把維修手冊當台灣報價或服務憑證。只回傳NEW_QUESTION一行，不改其他程式。」

**應該看到：** 沿用同一份競品文件庫索引，重新計算問題向量與回答。對照前後取回頁次，確認中文提問可找英文手冊；若找不到內容，要分清楚『本次片段不足』與『整本手冊沒有』，不能把相似段落當成證明。

**驗收：** 用PDF閱讀器跳到引用頁，確認型號、條件和原文。手冊沒有提供你的台灣正式報價與已購服務權益，答案應列供應商待確認；不應編出價格或三年到府承諾。若換PDF，回到第3步改檔名清單，再重跑第4、5步。執行階段回收後需重新上傳、輸入Key與建索引。
