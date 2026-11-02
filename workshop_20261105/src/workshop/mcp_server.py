import argparse
from mcp.server.fastmcp import FastMCP
from workshop.catalog import find_products, read_product


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--db', required=True)
    args = parser.parse_args()
    server = FastMCP('company-database')

    @server.tool()
    def find_products_by_model(model: str, market: str) -> dict:
        """依型號與市場查配置；market 使用 TW 或 US。"""
        return {'status': 'ok', 'products': find_products(args.db, model, market)}

    @server.tool()
    def read_product_by_id(product_id: str) -> dict:
        """讀取指定資料 ID，保留缺欄位。"""
        return read_product(args.db, product_id)

    server.run(transport='stdio')


if __name__ == '__main__':
    main()
