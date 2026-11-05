"""課堂用 SQLite 唯讀 MCP。僅初始化寫入，提供查詢的工具沒有寫入功能。"""
import argparse
import json
from pathlib import Path
import sqlite3
from mcp.server.fastmcp import FastMCP


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--db', required=True)
    args = parser.parse_args()
    path = Path(args.db).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, model TEXT, market TEXT, body TEXT)')
        for product in json.loads(Path(args.data).read_text(encoding='utf-8')):
            db.execute('INSERT OR IGNORE INTO products VALUES (?,?,?,?)', (product['id'], product['model'],
                product['market'], json.dumps(product, ensure_ascii=False)))

    def query(sql, parameters):
        with sqlite3.connect(path.as_uri()+'?mode=ro', uri=True) as db:
            return [json.loads(row[0]) for row in db.execute(sql, parameters)]

    server = FastMCP('company-database')

    @server.tool()
    def find_products_by_model(model: str, market: str) -> dict:
        """依型號與市場找配置，market 使用 TW 或 US。"""
        rows = query('SELECT body FROM products WHERE model=? AND market=? ORDER BY id', (model, market))
        return {'status': 'ok' if rows else 'not_found', 'products': rows}

    @server.tool()
    def read_product_by_id(product_id: str) -> dict:
        """讀取指定 ID 的詳細產品資料；保留空欄位。"""
        rows = query('SELECT body FROM products WHERE id=?', (product_id,))
        return {'status': 'ok' if rows else 'not_found', 'product': rows[0] if rows else None}

    server.run(transport='stdio')


if __name__ == '__main__':
    main()
