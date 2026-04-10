#!/usr/bin/env bash
# ================================================================
# HP MCP Server 啟動腳本
# 用途：啟動 HP 工具 MCP Server，供 LangGraph Agent 或 Claude Desktop 使用
# 使用方式：bash scripts/start_mcp_server.sh
# ================================================================

set -e

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SERVER="$REPO_ROOT/scripts/hp_mcp_server.py"

# ── 1. 確認 Python 版本 ──────────────────────────────────────────
echo "🔍 Python 版本："
python3 --version

# ── 2. 安裝相依套件（首次執行或更新時使用）──────────────────────────
if ! python3 -c "import fastmcp" 2>/dev/null; then
    echo "📦 安裝 fastmcp ..."
    pip install fastmcp
fi

# ── 3. 啟動 MCP Server（stdio 模式）─────────────────────────────
echo ""
echo "✅ 啟動 HP MCP Server ..."
echo "   Server 檔案：$SERVER"
echo "   傳輸模式：stdio"
echo "   （等待 MCP Client 連線，按 Ctrl+C 停止）"
echo ""
exec python3 "$SERVER"
