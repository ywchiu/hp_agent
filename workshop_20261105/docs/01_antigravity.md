# Antigravity：用需求帶著 AI 修改

第一天下午依 [課堂入口](../day1/README.md)，直接開啟專案工作區，從第一份研究開始。介面位置以實際版本為準；這份教材不要求學員手寫工具或 SQL。

1. 貼 [P01 第一份研究](../prompts/01_first_research.txt)，讓 AI 準備可執行範例與執行方式。先核對模擬資料，再跑研究。
2. 若執行本教材的 LangGraph 程式，在自己操作的互動式終端貼老師提供的 Key；不要貼進 Antigravity 對話。平台對話本身使用登入帳號的模型。
3. 用自己的話提出修改，例如「請補上採購前的三個問題，但不能改產品資料」。請 AI 只改研究問題，保留前後輸出。
4. 貼 [P02 Skill](../prompts/02_skill.txt)，改 `day1/SKILL.md` 的白話規則，以同一問題重跑，核對規則是否生效。
5. 貼 [P03 MCP](../prompts/03_mcp.txt)，先跑已接好的 MCP 範例，再視課堂進度讓 AI 配置 Antigravity 的 stdio 服務。只有實際模型工具呼叫紀錄才算直連成功。
6. 各章看 `report.md` 與 `research_log.json`：是否正確市場、兩筆台灣資料、缺資料待確認、來源與日期？MCP 要確認紀錄為 `mcp`，查不到與工具錯誤有區分。

Skill 章由程式將 `day1/SKILL.md` 文字傳給模型，不依賴某版 UI 的自動 Skill 探索。如果請 Antigravity 直接研究，也要明確要求它讀該檔並用輸出驗收。

資料只來自教材，不以模擬資料冒充即時官網。學員可以請 AI 改問題／規則；每次都需重跑與核對，不能只看「完成」宣告。

第二天從[120台企業採購入口](../day2/README.md)開始，依 [P04](../prompts/04_rag.txt) 到 [P07](../prompts/07_review.txt) 執行真實模型研究、跨程序恢復與詢價審核。老師已放入專案.env時直接讀取，學員只改中文需求，不展示Key。真實官網研究 [P08](../prompts/08_live_sources.txt) 與比較頁 [P09](../prompts/09_comparison_page.txt) 是選做，主線完成後由老師安排。
