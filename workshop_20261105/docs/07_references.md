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

第二天 RAG 仍用字元二元組關鍵字排序，不包含付費 embedding、向量庫或 reranker；第二天 Python 研究角色仍為固定流程。第一天下午已使用真實模型選工具，不能再以「全部 Colab 都是固定規則」描述。

投影片中的產業新聞、效能統計與產品故事屬原簡報內容，本版不重新驗證或延伸其數字，也不將它們當成程式測試的證據。
