# AI Agent 課堂逐步教材｜v0.1.0

以老師提供的 20261105 投影片 PDF（357 頁）為基準。這是一份可先放上 GitHub、之後逐章同步的教學版本。投影片未複製進公開教材。

## 同學從這裡開始

1. 讀 [課前準備](docs/00_setup.md)，選 Antigravity 或 Colab。
2. 開啟 [實作路線](#實作路線)，依課堂進度一次做一章。
3. 每章依「操作 → 觀察 → 修改 → 驗收」執行，把成果存到自己的資料夾。
4. 最後用 [成果清單](docs/03_submission.md) 檢查交付內容。

**兩種執行方式**：Antigravity 使用登入後的平台模型，讀資料、調工具、比較與修改，是本版的模型 Agent 實作路徑。Colab 執行真正的 LangGraph、MCP 與 SQLite，但研究節點採固定規則，方便逐格觀察與驗收；它不會自行呼叫 LLM，不把規則輸出稱為模型研究。兩條路的產品資料、規則與驗收問題相同。

課堂主線不用額外申請付費模型 API。Antigravity 的帳號、模型用量與方案由各自平台決定；套件安裝仍需網路。需要既有 API Agent 延伸時，由老師另行安排原專案的 `code/` notebooks，本版不自動讀取任何 `.env`。

## 實作路線

| ID | 投影片 PDF 頁碼 | 學生步驟 | Colab notebook | 線上執行 | 交付 |
|---|---|---|---|---|---|
| L00 | 119–124 | [課前準備](docs/00_setup.md) | [00 環境檢查](notebooks/00_setup.ipynb) | [開啟 Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/00_setup.ipynb) | 環境與版本紀錄 |
| L01 | 125–140 | [第一份產品研究](labs/01_first_research.md) | [01 起始版](notebooks/01_first_research.ipynb) | [開啟 Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/01_first_research.ipynb) | 比較表與一項問題 |
| L02 | 143–170 | [Skill 與 SQLite MCP](labs/02_skill_mcp.md) | [02 Skill 與 MCP](notebooks/02_skill_mcp.ipynb) | [開啟 Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/02_skill_mcp.ipynb) | 規則前後、工具結果 |
| L03 | 173–220 | [RAG 與引用查證](labs/03_rag.md) | [03 檢索](notebooks/03_rag.ipynb) | [開啟 Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/03_rag.ipynb) | 片段、適用性、缺口 |
| L04 | 222–259 | [有界研究與角色交接](labs/04_research_loop.md) | [04 補查迴圈](notebooks/04_research_loop.ipynb) | [開啟 Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/04_research_loop.ipynb) | 需求對照、修訂與停止原因 |
| L05 | 262–299 | [中斷恢復](labs/05_recovery.md) | [05 恢復](notebooks/05_recovery.ipynb) | [開啟 Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/05_recovery.ipynb) | Checkpoint 與冪等證據 |
| L06 | 307–348 | [人工審核與兩週追蹤](labs/06_review_monitor.md) | [06 審核追蹤](notebooks/06_review_monitor.ipynb) | [開啟 Colab](https://colab.research.google.com/github/ywchiu/hp_agent/blob/main/workshop_20261105/notebooks/06_review_monitor.ipynb) | 兩週資料、三條分支、回執 |

每份 notebook 都內嵌本版程式、Skill 與資料；尚未上 GitHub 也能單獨上傳 Colab。可直接使用上表「開啟 Colab」連結，或下載後到 Colab 的「上傳」開啟。

- [Antigravity 實際模型研究操作](docs/01_antigravity.md)
- [講師帶課手冊與答案](docs/02_instructor.md)
- [排錯](docs/04_troubleshooting.md)
- [投影片逐段對照與同步方式](docs/05_slide_sync.md)
- [公開 GitHub 的操作步驟](docs/06_github.md)
- [官方技術參考](docs/07_references.md)
- [版本紀錄](CHANGELOG.md)

## 本機快速檢查

在本資料夾完成課前安裝後：

```sh
python -m workshop.cli basic --out runs/basic
python -m workshop.cli mcp --out runs/mcp
python -m unittest discover -s tests -v
```

輸出使用模擬產品、企業需求與價格；Dell／Lenovo／ASUS 的恢復範例也全是教學假資料，不是品牌官方規格。通知只寫本機測試寄件器，不連接真實郵件或排程服務。

## 版本與驗證

基準來源與 SHA-256 記在 `course.json`。頁碼使用 PDF 實際頁碼。此版本未修改投影片。GitHub 教材位於本儲存庫的 `workshop_20261105/`，Colab 連結使用 `main` 分支。測試範圍請看 [驗證紀錄](VERIFICATION.md)；本機成功不等於已在同學的 Colab 帳號或 Antigravity 介面演練過。
