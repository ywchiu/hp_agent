# 放上 GitHub 與之後同步

此版本已準備為現有 `ywchiu/hp_agent` 儲存庫中的 `workshop_20261105/` 子目錄，以 `main` 分支作為同學的教材入口。ZIP 也可解壓後單獨閱讀或使用。

## 第一次發布到原儲存庫

1. 在原儲存庫根目錄執行 `git status --short`，先辨識既有變更。
2. 執行 `git add workshop_20261105 README.md`，只加入新教材與入口連結。
3. 執行 `git diff --cached --stat` 和 `git diff --cached`，確認未包含 `.env`、個資、`runs/`、SQLite、虛擬環境、原始投影片及舊教材暫存檔。
4. 執行 `git commit -m "Simplify day-one afternoon workshop v0.2.0"`。
5. 確認要發布的分支後執行 `git push origin <你的分支>`。Colab 連結預設使用 `main`；若使用其他分支，請同步調整連結。
6. 在 GitHub 打開 `workshop_20261105/README.md`，檢查章節連結及 notebook 顯示。
7. Colab 網址格式為 `https://colab.research.google.com/github/ywchiu/hp_agent/blob/<分支或commit>/workshop_20261105/notebooks/01_first_research.ipynb`，其餘 notebook 換檔名即可。
8. 老師先在乾淨 Colab 按順序跑完；確認遠端版本存在後，才把此網址給同學。網路或權限不可用時，可改用本機上傳版。

## 如果另開一個儲存庫

只複製本目錄教材；更新 `course.json` 的 repository、Colab 連結、狀態圖網址，再重新產生 notebooks。第一天程式與資料直接附在 notebook，圖片仍需網路載入。

## 每次更新

遵循 [同步步驟](05_slide_sync.md)，用小範圍 commit 記錄「哪一章、哪個行為、哪個驗收」改變。需要學生修改紀錄時，先在自己的副本練習，老師的 main 保留可上課版本。
