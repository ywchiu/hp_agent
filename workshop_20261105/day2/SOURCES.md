# 公開來源與採用方式

查閱日期：2026-11-05。`source_updated` 是原文標示的更新日；未標示就保留空值，不以查閱日期冒充。來源是公開規格與服務說明，非採購報價。課程只保存必要的中文摘述與定位，未公開轉存整份廠商文件。

|ID|官方來源|如何使用|
|---|---|---|
|LEN-PSREF|[ThinkPad T14 Gen 6 AMD PSREF](https://psref.lenovo.com/syspool/Sys/PDF/ThinkPad/ThinkPad_T14_Gen_6_AMD/ThinkPad_T14_Gen_6_AMD_Spec.PDF)|已讀正文；2026-08-28版。頁2作業系統／顯示、頁3記憶體／儲存、頁4電池、頁5重量、頁6連接埠、頁7安全。系列能力，非台灣SKU。|
|LEN-TW|[台灣保固服務說明](https://www.lenovo.com/tw/zh/support/think/section1/personalcomputing/)|已讀正文。筆電與桌機章節分開；三年有限保固不直接等於三年到府。部分專案一年，仍須查實際SKU／序號權益。|
|HP-IE|[C4JF4ET產品頁](https://www.hp.com/ie-en/products/laptops/product-details/2103300234)|已讀正文。愛爾蘭配置32GB、1TB、Win11 Pro，證明海外配置存在，不能證明台灣交貨。|
|HP-SPEC|[14吋Next Gen AI系列規格](https://support.hp.com/us-en/document/ish_12300115-12300036-16)|僅官方搜尋索引可見，直接頁面403。保留一筆待核實線索，程式排除，不當作已讀正文。|
|DELL-MEM|[PB14250 Core Ultra 200V記憶體](https://www.dell.com/support/manuals/en-au/dell-pro-pb14250-2-in-1-laptop/dell_pro_plus14_pb-14250_om/Memory?guid=guid-05867936-5f4f-49a0-aba0-bdb592fd6959&lang=en-us)|已讀正文。封裝記憶體、16／32GB、不能升級；不能套用到同名200U版。|
|DELL-PORT|[200V連接埠](https://www.dell.com/support/manuals/en-au/dell-pro-pb14250-2-in-1-laptop/dell_pro_plus14_pb-14250_om/external-ports-and-slots?guid=guid-1fc91ef3-b5a3-4c62-9229-cbe8084bfd5f&lang=en-us)|已讀正文；網站可能重新導向其他語系。連接埠能力不等於底座與雙4K螢幕已驗收。|
|DELL-TW|[Taiwan ProSupport Suite](https://www.dell.com/support/contents/en-tw/article/warranty/prosupport-suite-for-pcs)|已讀正文。次工作日到府有遠端診斷前提；服務介紹不能當作指定SKU已含三年。|

片段皆標 `public_fact`，表示摘述來自公開資料；不代表都適用於此案。`desktop_only` 與 `unverified_lead` 被排除；`regional_sku` 留給模型說明海外配置的邊界。可用片段27筆，不是27筆台灣合規證明。

L04–L06主流程使用封存摘述，確保官網暫時擋取時仍可演示。L04選做用OpenAI web_search查官方站並保存連結／時間；搜尋結果仍需人工核實。L06抓官方PDF的SHA-256，只能偵測內容指紋變動，不能單靠指紋推定規格、價格或服務變動。

想新增資料時，請AI同時補來源網址、原文位置、查閱日期、原文更新日、適用市場與配置，再檢查它是否把「選配」「最高」「起始」「需加購」改成了既定出貨事實。新來源要回到官網，不以另一位代理的摘要互相背書。

## L03：Colab直接下載的原始PDF（可改用上傳）

L03不使用上表29筆摘述；Colab直接下載[HP EliteBook 8 G1a 14 inch Notebook AI PC維修手冊](https://kaas.hpcloud.hp.com/pdf-public/pdf_12237395_en-US-1.pdf)，來源為[HP官方手冊清單](https://support.hp.com/us-en/product/setup-user-guides/hp-elitebook-8-g1a-14-inch-notebook-ai-pc/2102811726)，2026-11-06於官方清單核對。先核對封面，不能自行視為Next Gen AI或其他尺寸的手冊。教材不公開轉存整份廠商PDF。

以實際下載或上傳檔案的SHA-256識別版本；片段保留檔名與PDF閱讀器頁次。僅擷取文字，圖片／掃描頁不代表已讀。整份文件切段後實際送embedding API，再以問題向量從每份PDF各取前幾段；避免長手冊擠掉其他品牌。手冊型號、選配、維修資格仍須核對原文，不能拿來證明台灣指定SKU、庫存、價格或已購買服務。

同時下載[Lenovo T14 Gen 6 AMD PSREF](https://psref.lenovo.com/syspool/Sys/PDF/ThinkPad/ThinkPad_T14_Gen_6_AMD/ThinkPad_T14_Gen_6_AMD_Spec.PDF)與[Dell Pro 13／14／16 Plus官方型錄](https://www.delltechnologies.com/asset/en-gb/products/laptops-and-2-in-1s/technical-support/dell-pro-13-14-16-plus-laptop-product-brochure.pdf)，建立三品牌競品文件庫。Dell型錄同時含不同尺寸與200V／200U，研究只採PB14250 Core Ultra 200V適用欄位。只有HP文件時可練操作，其他品牌標缺文件，不可補齊假比較。L03產物是三品牌有頁碼的比較表、證據缺口與供應商問題，接續L04的研究任務；不自動將模型答案寫回其他章節的封存證據。
