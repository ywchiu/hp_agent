# 從第一個範例直接開始

已移除獨立的第 0 步與環境檢查 notebook。同學直接開 [第一天下午課堂入口](../day1/README.md)，範例會自行準備所需套件；老師提供 Key，不用自行申請。

這個舊連結保留給先前書籤使用，不是額外作業。

## 講師／維護者本機驗證

在 `workshop_20261105` 目錄使用獨立 Python 3.11+ 虛擬環境：

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -m pip install -e .
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_notebooks.py
.venv/bin/python scripts/check_materials.py
```

第一天下午本機示範命令在 [課堂入口](../day1/README.md)。第二天舊版 CLI 安裝後可用 `python -m workshop.cli --help` 查看，不需 API Key。
