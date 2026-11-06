# 技術參考與查閱邊界

既有流程參考於 2026-11-02；第一天模型 API 參考於 2026-11-05。課前仍應確認平台介面與套件可用性。

- [OpenAI Function calling](https://developers.openai.com/api/docs/guides/function-calling)：第一天使用 Responses API 的工具要求與 function_call_output。
- [OpenAI Quickstart](https://developers.openai.com/api/docs/quickstart)：模型 API 的基本使用。
- [GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna)：本範例預設模型；老師可依課堂帳號可用模型調整。

- [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)：區分 thread 內的 checkpoint 與跨任務資料。本教材用磁碟 SQLite 保存 graph state。
- [LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)：`interrupt` 暫停，使用原 thread 與 `Command(resume=...)` 恢復。恢復會從節點開頭重進，副作用需另行處理。
- [MCP 官方 Python SDK](https://github.com/modelcontextprotocol/python-sdk)：stdio 的 ClientSession、工具探索與 FastMCP 服務。
- [Antigravity Skills](https://antigravity.google/docs/skills/)：可重用方法。此版本使用顯式讀檔，避免依賴自動載入位置。
- [Antigravity Settings](https://www.antigravity.google/docs/settings)：設定與 MCP 自訂功能；UI 位置依版本確認。
- [Google Colab](https://colab.research.google.com/)：本課用上傳 notebook，不依賴私人 Drive 連結。

L03實際讀取Colab直接下載或自行上傳的三品牌PDF，以 `text-embedding-3-small` 建立文件與問題向量，以Chroma保存向量、原文與頁碼，實際查詢collection並先顯示片段，再由 `gpt-6-luna` 回答；參考[OpenAI embedding文件](https://developers.openai.com/api/docs/guides/embeddings)。其他研究角色也真實呼叫模型。官方資料出處與採用邊界見 [第二天來源說明](../day2/SOURCES.md)。L04預設實際web_search與HTML／PDF原文閱讀，採用四月完整研究迴圈（詳見[設計對照](../day2/RESEARCH_DESIGN.md)），L06選做真實PDF快照，沒有虛構歷史報價。

投影片中的產業新聞、效能統計與產品故事屬原簡報內容，本版不重新驗證或延伸其數字，也不將它們當成程式測試的證據。

L03使用[Chroma明確提供向量寫入](https://docs.trychroma.com/docs/collections/add-data)、[collection查詢與metadata篩選](https://docs.trychroma.com/docs/querying-collections/query-and-get)、[HNSW與cosine設定](https://docs.trychroma.com/docs/collections/configure)。Chroma負責儲存與搜尋，OpenAI負責embedding；相似度顯示為1減cosine distance，並非正確率。
