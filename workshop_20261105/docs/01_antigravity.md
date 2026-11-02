# Antigravity 的逐步模型研究路徑

這條路徑讓平台模型實際讀取資料、運用方法、使用 MCP 工具及修訂報告。Colab 的規則程式作為可重現參考答案。

1. 依 [L00](00_setup.md) 開啟工作區，貼 P00。
2. 在同一工作區貼 [P01](../prompts/01_first_research.txt)，只完成起始版。模型應回報讀過哪些檔案，交付表格與待確認問題。
3. 打開 `runs/antigravity/01_report.md`，回查兩筆 JSON；親自核對市場、配置與保固。不要只讀模型的完成宣告。
4. 貼 [P02](../prompts/02_skill.txt)，讓模型先讀 Skill，再套用你新增的一條規則；保留修改前後檔案。
5. 完成本機安裝後，執行 `python -m workshop.cli mcp --out runs/mcp`，確認真正協定握手、工具探索與呼叫均成功。
6. 如要讓 Antigravity 模型直接呼叫 MCP，執行 `python scripts/make_mcp_config.py`，將產生的設定合併到 Antigravity 的 MCP 自訂設定。保留原有服務；介面位置以當日版本與 [官方文件](https://antigravity.google/docs/mcp/) 為準。
7. 重新載入服務，確認兩個工具出現。貼 [P03](../prompts/03_mcp.txt)。要求模型真的呼叫工具；檢查工具執行紀錄，不能以它閱讀 JSON 或 Python CLI 成功代替模型工具呼叫。
8. 依序貼 [P04](../prompts/04_rag.txt)、[P05](../prompts/05_research_team.txt)，讓模型從片段中找證據、補查、修訂。每一步先看交付物再進下一步。
9. 貼 [P06](../prompts/06_recovery.txt)，要求它執行現成的中斷與恢復命令，展示狀態檔與紀錄。
10. 貼 [P07](../prompts/07_review.txt)，操作三種人工決定與重跑。
11. 選做：[P08](../prompts/08_live_sources.txt) 將其中一項改成官方公開來源研究。保留 URL、查閱日期、原文位置與市場。讀取失敗就是未取得；不把教材資料冒充即時官網。

**Skill 載入**：本版直接在提示詞指定讀取 `skills/product-research/SKILL.md`，不依賴某一版 UI 的自動發現路徑。若已安裝為平台 Skill，也要用輸出和規則驗收，不只確認檔名出現。

**角色分工**：P05 先以同一模型分次扮演 Planner／Researcher／Writer／Reviewer。這是角色化流程。如果平台支援獨立子代理，可選擇分成獨立上下文，另記錄每位的輸入、工具與交接；不能只因有四個段落就宣稱已完成 Multi-Agent。

可選的比較頁：在 L02 成果完成後貼 P09，讓 Coding Agent 產出單檔 HTML 比較頁，保留來源與「待確認」；先核對資料，再看畫面。
