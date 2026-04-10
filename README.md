# LLM Application - AI Agent 實戰課程

AI Agent 開發實戰訓練，從基礎概念到企業級部署課程。


## Demo20260409
- https://colab.research.google.com/drive/1ROpSynJCc3JDcFTiKz1x1oAEm-tvl_bt?usp=sharing

## Demo20260410
- https://colab.research.google.com/drive/1dOXM3K_nXB5K5NL6r1CuveQVSTJNffGt?usp=sharing

## 教材 Notebooks

| # | Notebook | 說明 |
|---|----------|------|
| 00 | [最簡單的 Agent](code/00_Simple_Agent_Demo.ipynb) | LLM + Tools + Loop，用最少的程式碼打造一個可運作的 Agent |
| 01 | [LangGraph 核心設計](code/01_LangGraph_Core_Design.ipynb) | StateGraph / Node / Edge / Conditional Edge，實作 ReAct、Plan-Execute、Supervisor |
| 02 | [語音助理系統](code/02_Voice_Assistant.ipynb) | Whisper ASR + OpenAI TTS + LangGraph Pipeline，含 IT 術語修正 |
| 03 | [進階語音助理](code/03_Advanced_Voice_Agent.ipynb) | 五大模式整合：Pipeline / Orchestrator / Memory / HITL / Tool-Augmented |
| 04 | [Agentic RAG](code/04_Agentic_RAG.ipynb) | 完整的自我修正 RAG 系統，含 Router / Grader / Hallucination Checker / Fallback；附 MCP 整合實作 |
| 05 | [Deep Research Agent](code/05_Deep_Research_Agent.ipynb) | 迭代式研究 Agent，含 Planner / Searcher / Reader / Synthesizer + Critic；附 MCP 串接搜尋工具 |
| 06 | [MCP 實作](code/06_MCP.ipynb) | FastMCP 建立 HP 工具 Server，LangGraph Agent 透過 MCP Client 自動發現並呼叫工具 |
| 07 | [Skill 實作](code/07_Skill.ipynb) | 用 SKILL.md 封裝 Agent 行為規範，打造可複用的 HP 客服技能包 |

## 實作練習 Labs

每個 Lab 約 30 分鐘，提供骨架程式碼，學員只需填入關鍵邏輯（約 3-5 行）。

| Lab | 主題 | 對應課程 |
|-----|------|---------|
| [Lab 1](code/labs/Lab1_LangGraph_First_Agent.ipynb) | 我的第一個 LangGraph — HP 產品查詢 Agent | Day 1 上午 |
| [Lab 2](code/labs/Lab2_Voice_Pipeline.ipynb) | 語音進語音出 — STT → LLM → TTS Pipeline | Day 1 下午 |
| [Lab 3](code/labs/Lab3_RAG_Grader.ipynb) | 給 RAG 加一個品質關卡 — Grader 節點實作 | Day 2 上午 |
| [Lab 4](code/labs/Lab4_Deep_Research.ipynb) | 讓 Agent 研究一個真實問題 — HP vs Lenovo 分析 | Day 2 下午 |

## 本機啟動 MCP Server

MCP Server 讓 LangGraph Agent 或 Claude Desktop 透過標準協定呼叫 HP 工具。

### 步驟一：安裝相依套件

```bash
pip install fastmcp langchain-mcp-adapters
```

### 步驟二：啟動 Server

```bash
bash scripts/start_mcp_server.sh
```

或直接用 Python 啟動：

```bash
python scripts/hp_mcp_server.py
```

啟動後終端機會顯示：

```
✅ 啟動 HP MCP Server ...
   傳輸模式：stdio
   （等待 MCP Client 連線，按 Ctrl+C 停止）
```

### 步驟三：串接 Claude Desktop（選用）

將以下設定寫入 `~/Library/Application Support/Claude/claude_desktop_config.json`，重啟 Claude Desktop 即可在對話中直接使用 HP 工具：

```json
{
  "mcpServers": {
    "hp-tools": {
      "command": "python",
      "args": ["scripts/hp_mcp_server.py"]
    }
  }
}
```

> **提供的工具**：`check_inventory`（庫存查詢）、`check_warranty`（保固確認）、`get_repair_sop`（維修 SOP）

---

## 環境需求

- **執行環境：** Google Colab（免費版即可）
- **API Key：** OpenAI API Key（課程提供測試用 Key）
- **主要套件：** langchain, langgraph, openai, chromadb

## 如何使用

在 Google Colab 中開啟任一 Notebook：

```
https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/<NOTEBOOK 檔名>.ipynb
```

或直接點擊下方快速連結：

| Notebook | Colab 連結 |
|----------|-----------|
| 00 最簡單的 Agent | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/00_Simple_Agent_Demo.ipynb) |
| 01 LangGraph 核心 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/01_LangGraph_Core_Design.ipynb) |
| 02 語音助理 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/02_Voice_Assistant.ipynb) |
| 03 進階語音助理 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/03_Advanced_Voice_Agent.ipynb) |
| 04 Agentic RAG | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/04_Agentic_RAG.ipynb) |
| 05 Deep Research | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/05_Deep_Research_Agent.ipynb) |
| 06 MCP 實作 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/06_MCP.ipynb) |
| 07 Skill 實作 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/07_Skill.ipynb) |
| Lab 1 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab1_LangGraph_First_Agent.ipynb) |
| Lab 2 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab2_Voice_Pipeline.ipynb) |
| Lab 3 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab3_RAG_Grader.ipynb) |
| Lab 4 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab4_Deep_Research.ipynb) |

