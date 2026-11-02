import asyncio
import json
import os
import sys
from workshop.catalog import ROOT
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def inspect_database(path):
    params = StdioServerParameters(command=sys.executable,
                                  args=['-m', 'workshop.mcp_server', '--db', str(path)],
                                  env=dict(os.environ, PYTHONPATH=str(ROOT/'src')))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            names = [t.name for t in (await session.list_tools()).tools]
            calls = [await session.call_tool('find_products_by_model', {'model':'DemoBook A', 'market':'TW'}),
                     await session.call_tool('read_product_by_id', {'product_id':'DEMO-TW-032'})]
            return {'tools': names, 'results': [json.loads(r.content[0].text) for r in calls]}


def run(path):
    return asyncio.run(inspect_database(path))
