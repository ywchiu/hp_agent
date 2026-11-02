# L02｜Skill 與 SQLite MCP

對照 PDF 143–170；建議 40 分鐘。先備：L01。交付：規則修改、前後摘要、MCP 工具結果與最終比較表。

## A. 修改一條研究規則

1. 讀 `skills/product-research/SKILL.md`，將「方法」與 `products.json` 裡的「產品事實」分開。
2. Colab 開 `02_skill_mcp.ipynb`；Antigravity 貼 [P02](../prompts/02_skill.txt)。
3. notebook 會在成果資料夾複製一份拿掉 `[unknown_warranty]` 規則的起始 Skill，先跑出「未填」的初稿。它刻意表現不完整，但不製造錯誤保固值。
4. 在那份起始 Skill 加回「保固缺漏標示待確認，不能推論較佳」。保留標記 `[unknown_warranty]`，讓規則程式辨識這個練習開關。
5. 以完全相同資料重跑，保存 before／after。Antigravity 則讓模型讀完整 Skill 套用規則，並指出實際改變的結論。
6. 檢查產品檔沒有被改動。更新方法不應改寫產品保固資料。

## B. 查詢真正的 MCP 服務

7. 本機執行 `python -m workshop.cli mcp --out runs/l02_mcp`；Colab 跑 MCP 格。client 將啟動 stdio server、initialize、list_tools，再呼叫兩個工具。
8. 應看到 `find_products_by_model` 與 `read_product_by_id`。第一個傳 `DemoBook A`／`TW` 得到兩筆配置；第二個讀 `DEMO-TW-032`，保固為 null。
9. Antigravity 要直接呼叫時，依 [模型操作路徑](../docs/01_antigravity.md) 的設定步驟接入，再貼 [P03](../prompts/03_mcp.txt)。確認工具紀錄，而不是只有報告說「已使用 MCP」。
10. 查 `DEMO-US-032`，觀察三年保固；說明為什麼不能拿來補台灣版。
11. 讀不存在 ID，應回 `not_found`；用錯的資料庫路徑則應回報工具失敗，不把它說成「產品不存在」。
12. 依工具回傳結果，重新產出 L01 比較表。保存原始工具輸出及來源 ID。

## 驗收

- [ ] 同市場一配置一列，US 資料沒有混入 TW。
- [ ] 修改後缺漏明確標「待確認」。
- [ ] 有真正 MCP 握手、list_tools 與 call_tool 的證據。
- [ ] 未找到與查詢失敗能區分。
- [ ] 查詢服務只提供兩個固定參數工具，不接受任意 SQL、不修改資料庫。

選做：用 [P09](../prompts/09_comparison_page.txt) 將結果做成 HTML 比較頁，再人工逐欄核對。
