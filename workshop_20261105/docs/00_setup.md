# L00｜課前準備

對照 PDF 119–124。目標：先把教材打開、執行一次、知道成果存在哪裡。

## 路線 A：Antigravity（主要模型操作）

1. 取得本教材資料夾或老師提供的 ZIP，解壓縮。保留完整目錄，不只下載提示詞。
2. 開啟 Antigravity，登入可用帳號，開啟包含本 README 的 `workshop_20261105` 資料夾作為工作區。
3. 在檔案清單確認看得到 `data/`、`skills/`、`labs/`、`src/`。App／IDE 介面名稱可能不同，以「目前工作區」為準。
4. 開啟新對話，貼上 [P00 確認工作區](../prompts/00_orientation.txt)。檢查它讀的是本版資料。
5. 不執行程式也可先由模型閱讀資料完成 L01。要執行 LangGraph、MCP、恢復與審核，請完成下方本機 Python 安裝。
6. 在工作區終端機執行以下命令；如果不熟悉，交給 Antigravity 依作業系統操作，要求回報實際命令與版本。

macOS／Linux，於教材目錄：

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -e .
python -m workshop.cli basic --out runs/setup
```

Windows PowerShell，於教材目錄：

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m pip install -e .
.venv\Scripts\python.exe -m workshop.cli basic --out runs/setup
```

後續的 `python` 均指這個虛擬環境。Windows 可持續使用完整的 `.venv\Scripts\python.exe`，不用修改系統執行政策。需要 Python 3.10+，本版以 Python 3.11 驗證。

## 路線 B：Google Colab（逐格觀察流程）

1. 到 [Google Colab](https://colab.research.google.com/)，登入 Google 帳號。
2. 選「開啟筆記本／上傳」，上傳 `notebooks/00_setup.ipynb`。日後 GitHub 發布後也可從 GitHub 頁開啟。
3. 先存一份自己的副本。選一般 Python CPU 執行階段即可，不需 GPU。
4. 從最上方的說明開始，依序按每格左邊的播放按鈕。第一格安裝指定版本，第二格展開內嵌教材。
5. 每格先看文字，預測結果，再執行；不要一開始就「全部執行」跳過觀察。
6. 在最後一格下載自己的成果 ZIP。只有儲存 notebook，不會自動保存 `/content` 內的 SQLite 或報告。
7. 換章時上傳下一份 notebook；每章自帶相同資料，不必依賴上一章的執行階段。

**恢復的界線**：L05 會啟動兩個獨立 Python 程序，展示跨程序恢復；Colab 若整個執行階段被回收，暫存檔也會消失。跨執行階段必須先下載並完整還原狀態 ZIP，或使用自己的持久磁碟。不要刪除 SQLite 再聲稱恢復成功。

## 課前驗收

- [ ] 能說出教材版本 `0.1.0`。
- [ ] 看到 DEMO-TW-016／032，沒有把 US 資料補到 TW。
- [ ] 知道資料是模擬的，沒有提供或上傳 API Key。
- [ ] 找得到本輪 `runs/` 或 notebook 顯示的成果資料夾。
