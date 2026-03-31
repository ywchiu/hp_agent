# LLM Application - AI Agent 實戰課程

針對 HP 筆電 / PC 產業設計的 AI Agent 開發實戰訓練，從基礎概念到企業級部署的完整兩天課程。

## 課程大綱

### 第一天：AI Agent 導入與語音整合

| 時段 | 主題 | 內容 |
|------|------|------|
| 上午 | LangGraph 核心設計思維 | Agent 概念、LangGraph 核心元件、ReAct / Plan-and-Execute / Supervisor 三種模式 |
| 下午 | 打造語音助理系統 | ASR 語音識別、TTS 語音合成、Pipeline / Orchestrator / Memory / HITL / Tool 五大模式 |

### 第二天：RAG 進階與深度研究

| 時段 | 主題 | 內容 |
|------|------|------|
| 上午 | 從 Naive RAG 到 Agentic RAG | RAG 三代演進、Corrective RAG / Self-RAG 論文解析、Router / Grader / Hallucination Checker 實作 |
| 下午 | Deep Research Agent | 研究型 Agent 流程、Planner / Searcher / Reader / Synthesizer + Critic、迭代研究與自適應終止 |

## 教材 Notebooks

| # | Notebook | 說明 |
|---|----------|------|
| 00 | [最簡單的 Agent](code/00_Simple_Agent_Demo.ipynb) | LLM + Tools + Loop，用最少的程式碼打造一個可運作的 Agent |
| 01 | [LangGraph 核心設計](code/01_LangGraph_Core_Design.ipynb) | StateGraph / Node / Edge / Conditional Edge，實作 ReAct、Plan-Execute、Supervisor |
| 02 | [語音助理系統](code/02_Voice_Assistant.ipynb) | Whisper ASR + OpenAI TTS + LangGraph Pipeline，含 IT 術語修正 |
| 03 | [進階語音助理](code/03_Advanced_Voice_Agent.ipynb) | 五大模式整合：Pipeline / Orchestrator / Memory / HITL / Tool-Augmented |
| 04 | [Agentic RAG](code/04_Agentic_RAG.ipynb) | 完整的自我修正 RAG 系統，含 Router / Grader / Hallucination Checker / Fallback |
| 05 | [Deep Research Agent](code/05_Deep_Research_Agent.ipynb) | 迭代式研究 Agent，含 Planner / Searcher / Reader / Synthesizer + Critic |

## 實作練習 Labs

每個 Lab 約 30 分鐘，提供骨架程式碼，學員只需填入關鍵邏輯（約 3-5 行）。

| Lab | 主題 | 對應課程 |
|-----|------|---------|
| [Lab 1](code/labs/Lab1_LangGraph_First_Agent.ipynb) | 我的第一個 LangGraph — HP 產品查詢 Agent | Day 1 上午 |
| [Lab 2](code/labs/Lab2_Voice_Pipeline.ipynb) | 語音進語音出 — STT → LLM → TTS Pipeline | Day 1 下午 |
| [Lab 3](code/labs/Lab3_RAG_Grader.ipynb) | 給 RAG 加一個品質關卡 — Grader 節點實作 | Day 2 上午 |
| [Lab 4](code/labs/Lab4_Deep_Research.ipynb) | 讓 Agent 研究一個真實問題 — HP vs Lenovo 分析 | Day 2 下午 |

## 環境需求

- **執行環境：** Google Colab（免費版即可）
- **API Key：** OpenAI API Key（課程提供測試用 Key）
- **Python 版本：** 3.10+
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
| Lab 1 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab1_LangGraph_First_Agent.ipynb) |
| Lab 2 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab2_Voice_Pipeline.ipynb) |
| Lab 3 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab3_RAG_Grader.ipynb) |
| Lab 4 | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/code/labs/Lab4_Deep_Research.ipynb) |

## 講師資訊

**大數軟體有限公司**
- 網站：[largitdata.com](http://www.largitdata.com/)
