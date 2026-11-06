"""預設使用模型替身驗證第一天；--live-model 讀取 .env，實際呼叫模型。"""
import argparse
import json
import os
from pathlib import Path
import sys
import shutil
import tempfile
import time
import nbformat
from nbclient import NotebookClient

p=argparse.ArgumentParser()
p.add_argument('--out',default=None)
p.add_argument('--notebook',default=None,help='只驗證指定檔名，例如04_research_loop.ipynb')
p.add_argument('--day', choices=['1','2','all'], default='1')
p.add_argument('--live-model', action='store_true', help='讀取指定 .env，真的呼叫模型 API')
p.add_argument('--pdf', type=Path, nargs='+', help='L03實測需提供真正PDF，可給三品牌各一份')
p.add_argument('--env-file', type=Path, default=Path(__file__).resolve().parents[2]/'.env')
args=p.parse_args()
root=Path(__file__).resolve().parents[1]
live_key=None
if args.live_model:
    from dotenv import dotenv_values
    values=dotenv_values(args.env_file)
    live_key=values.get('OPENAI_API_KEY') or values.get('OPENAIAPI_KEY')
    if not live_key:
        raise SystemExit('指定 .env 沒有可用的模型 Key。')
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
    if args.notebook and path.name!=args.notebook:
        continue
    nb=nbformat.read(path,as_version=4)
    day=nb.metadata.hp_workshop.get('day',2)
    if args.day!='all' and int(args.day)!=day:
        continue
    work=out/path.stem
    work.mkdir(parents=True,exist_ok=True)
    if path.name=='03_rag.ipynb':
        if not args.pdf:
            raise SystemExit('L03請加 --pdf 三品牌PDF路徑；測試會實際讀檔與embedding。')
        for pdf in args.pdf:
            shutil.copyfile(pdf,work/pdf.name)
        for cell in nb.cells:
            if cell.cell_type=='code' and 'PDF_FILES = ' in cell.source:
                lines=cell.source.splitlines()
                lines=[f'PDF_FILES = {", ".join(pdf.name for pdf in args.pdf)!r}' if line.startswith('PDF_FILES = ') else line for line in lines]
                cell.source='\n'.join(lines)+'\n'
    if day in (1,2):
        # 注入只存在於測試副本的模型替身；發布 notebook 不含此格。
        if not args.live_model and day==1:
            nb.cells.insert(0,nbformat.v4.new_code_cell(
                f'import sys, openai\nsys.path.insert(0, {str(root/"tests")!r})\n'
                'from day1_fakes import FakeClient\n'
                'openai.AsyncOpenAI = FakeClient\n'))
        if not args.live_model and day==2:
            raise SystemExit('第二天請加 --live-model；不把固定回覆當成模型驗證。')
        for c in nb.cells:
            if c.cell_type=='code' and 'API_KEY = getpass(' in c.source:
                # nbclient 不支援互動輸入；僅在測試副本取代此提示。
                source='getpass = lambda *a, **k: os.environ.pop("HP_WORKSHOP_QA_KEY")\n' if args.live_model else 'getpass = lambda *a, **k: "qa-only-not-a-key"\n'
                c.source=source+c.source
    start=time.monotonic()
    kernel_env=dict(os.environ)
    if live_key:
        kernel_env['HP_WORKSHOP_QA_KEY']=live_key
    try:
        NotebookClient(nb,timeout=360,kernel_name='python3',resources={'metadata':{'path':str(work)}}).execute(env=kernel_env)
    except Exception as error:
        message=str(error)
        if live_key:
            message=message.replace(live_key,'[REDACTED]')
        raise SystemExit(message) from None
    nbformat.write(nb,out/path.name)
    results.append({'notebook':path.name,'status':'passed','model':'gpt-6-luna' if args.live_model else 'test double' if day==1 else 'no model',
                    'code_cells':sum(c.cell_type=='code' for c in nb.cells),
                    'seconds':round(time.monotonic()-start,2)})
    print(path.name,'PASS',flush=True)
(out/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(out)
