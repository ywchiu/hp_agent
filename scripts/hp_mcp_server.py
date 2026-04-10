"""
HP MCP Server — 提供庫存查詢、保固確認、維修 SOP 三項工具
啟動方式：python scripts/hp_mcp_server.py
"""
from fastmcp import FastMCP

mcp = FastMCP("HP Tools")

# ─── 模擬資料庫 ─────────────────────────────────────────────────
_INVENTORY = {
    "HP EliteBook 840": {"stock": 15, "location": "台北倉"},
    "HP LaserJet Pro":  {"stock": 3,  "location": "新竹倉"},
    "HP ZBook Studio":  {"stock": 0,  "location": "缺貨"},
}

_WARRANTY = {
    "SN12345": {"status": "有效", "expire": "2026-12-31", "model": "HP EliteBook 840"},
    "SN99999": {"status": "過期", "expire": "2024-01-01", "model": "HP LaserJet Pro"},
}

_SOP = {
    "無法開機":   "1. 確認電源線 2. 嘗試硬重啟 3. 進 BIOS 診斷 4. 聯絡技術支援",
    "印表機卡紙": "1. 關閉電源 2. 打開前蓋 3. 輕輕取出紙張 4. 重新對齊紙張後重啟",
}

# ─── MCP Tools ──────────────────────────────────────────────────
@mcp.tool()
def check_inventory(product: str) -> dict:
    """查詢 HP 產品庫存數量與倉庫位置"""
    return _INVENTORY.get(product, {"stock": "未知", "location": "查無此產品"})


@mcp.tool()
def check_warranty(serial_number: str) -> dict:
    """根據序號確認 HP 產品保固狀態與到期日"""
    return _WARRANTY.get(serial_number, {"status": "查無資料", "expire": None})


@mcp.tool()
def get_repair_sop(issue: str) -> str:
    """取得 HP 常見問題的維修 SOP 步驟"""
    for key, sop in _SOP.items():
        if key in issue:
            return sop
    return "請聯絡 HP 技術支援：0800-012-345"


# ─── MCP Resources ──────────────────────────────────────────────
PRODUCT_CATALOG = [
    {"line": "EliteBook", "segment": "商務筆電", "range": "800 / 1000 系列"},
    {"line": "ZBook",     "segment": "工作站筆電", "range": "Studio / Fury"},
    {"line": "LaserJet",  "segment": "雷射印表機", "range": "Pro / Enterprise"},
]

@mcp.resource("kb://products")
def list_products() -> list:
    """列出 HP 知識庫中的產品線（靜態目錄）"""
    return PRODUCT_CATALOG


if __name__ == "__main__":
    mcp.run(transport="stdio")
