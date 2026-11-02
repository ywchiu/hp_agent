"""在目前 Python kernel 逐格驗證；需 requirements-dev.txt。結果放指定暫存目錄。"""
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
    start=time.monotonic()
    NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(root)}}).execute()
    nbformat.write(nb,out/path.name)
    results.append({'notebook':path.name,'status':'passed','code_cells':sum(c.cell_type=='code' for c in nb.cells),
                    'seconds':round(time.monotonic()-start,2)})
    print(path.name,'PASS',flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(out)
