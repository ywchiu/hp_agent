"""離線模型驗證：真實 LangGraph／MCP，以模型替身執行；不使用真實 Key。"""
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
import time
import nbformat
from nbclient import NotebookClient

p=argparse.ArgumentParser()
p.add_argument('--out',default=None)
p.add_argument('--day', choices=['1','2','all'], default='1')
args=p.parse_args()
root=Path(__file__).resolve().parents[1]
out=Path(args.out or tempfile.mkdtemp(prefix='hp_notebook_qa_')).resolve()
out.mkdir(parents=True,exist_ok=True)
# 將測試 kernel 固定到這個 interpreter，避免使用另一個未裝套件的全域 kernel。
kernel_dir=out/'jupyter/kernels/python3'
kernel_dir.mkdir(parents=True,exist_ok=True)
(kernel_dir/'kernel.json').write_text(json.dumps({'argv':[sys.executable,'-m','ipykernel_launcher','-f','{connection_file}'],
                                               'display_name':'Workshop QA','language':'python'}))
os.environ['JUPYTER_PATH']=str(out/'jupyter')
os.environ['HP_WORKSHOP_SKIP_INSTALL']='1'
os.environ['IPYTHONDIR']=str(out/'ipython')
results=[]
for path in sorted((root/'notebooks').glob('*.ipynb')):
    nb=nbformat.read(path,as_version=4)
    day=nb.metadata.hp_workshop.get('day',2)
    if args.day!='all' and int(args.day)!=day:
        continue
    work=out/path.stem
    work.mkdir(parents=True,exist_ok=True)
    if day==1:
        # 注入只存在於測試副本的模型替身；發布 notebook 不含此格。
        nb.cells.insert(0,nbformat.v4.new_code_cell(
            f'import sys, openai\nsys.path.insert(0, {str(root/"tests")!r})\n'
            'from day1_fakes import FakeClient\n'
            'openai.AsyncOpenAI = FakeClient\n'))
        for c in nb.cells:
            if c.cell_type=='code' and 'API_KEY = getpass(' in c.source:
                # nbclient 不支援互動輸入；僅在測試副本取代此提示。
                c.source='getpass = lambda *a, **k: "qa-only-not-a-key"\n'+c.source
    start=time.monotonic()
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(work)}}).execute()
    nbformat.write(nb,out/path.name)
    results.append({'notebook':path.name,'status':'passed','model':'test double' if day==1 else 'no model',
                    'code_cells':sum(c.cell_type=='code' for c in nb.cells),
                    'seconds':round(time.monotonic()-start,2)})
    print(path.name,'PASS',flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(out)
