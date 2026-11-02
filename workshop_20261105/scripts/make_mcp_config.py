"""用本機實際 Python 產生可合併設定；不修改使用者全域設定。"""
import json
from pathlib import Path
import sys

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'src'))
from workshop.catalog import seed

db=seed(root/'runs/mcp/catalog.sqlite')
config={'mcpServers':{'company-database':{
    'command':sys.executable,
    'args':['-m','workshop.mcp_server','--db',str(db)],
    'env':{'PYTHONPATH':str(root/'src')}
}}}
out=root/'runs/mcp/antigravity_mcp.json'
out.write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(out)
print('將此檔的 company-database 項目合併到你使用版本的 MCP 設定，保留既有項目。')
