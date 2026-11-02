"""兩個限制查詢的唯讀工具；不接受任意 SQL。"""
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(name):
    return json.loads((ROOT / 'data' / name).read_text(encoding='utf-8'))


def seed(path):
    path = Path(path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS products (id TEXT PRIMARY KEY, model TEXT, market TEXT, body TEXT)')
        for row in load('products.json'):
            db.execute('INSERT OR IGNORE INTO products VALUES (?,?,?,?)',
                       (row['id'], row['model'], row['market'], json.dumps(row, ensure_ascii=False)))
    return path


def query(path, sql, values):
    with sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True) as db:
        return [json.loads(row[0]) for row in db.execute(sql, values)]


def find_products(path, model, market):
    return query(path, 'SELECT body FROM products WHERE model=? AND market=? ORDER BY id', (model, market))


def read_product(path, product_id):
    rows = query(path, 'SELECT body FROM products WHERE id=?', (product_id,))
    return {'status': 'ok', 'product': rows[0]} if rows else {'status': 'not_found', 'product': None}
