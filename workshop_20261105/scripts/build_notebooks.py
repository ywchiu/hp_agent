"""從共用原始碼與 lesson_cells.json 產生七份可獨立上傳的 notebook。"""
import base64
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT=Path(__file__).resolve().parents[1]


def payload():
    paths=[]
    for folder in ['src','data','skills','tests']:
        paths.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts
                     and not any(part.endswith('.egg-info') for part in p.parts))
    paths.extend(ROOT/p for p in ['requirements.txt','course.json'])
    hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
    stream=io.BytesIO()
    with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as z:
        for name in hashes:
            info=zipfile.ZipInfo(name,date_time=(2026,11,2,0,0,0))
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,(ROOT/name).read_bytes())
    raw=stream.getvalue()
    return raw,hashes


def build():
    material_version=json.loads((ROOT/'course.json').read_text())['material_version']
    requirements=[line.strip() for line in (ROOT/'requirements.txt').read_text().splitlines()
                  if line.strip() and not line.startswith('#')]
    raw,hashes=payload()
    checksum=hashlib.sha256(raw).hexdigest()
    encoded=base64.b64encode(raw).decode()
    setup=f'''# Step 1：安裝本版指定套件（CPU，不需模型 API Key）
import os, sys, subprocess
if os.environ.get("HP_WORKSHOP_SKIP_INSTALL") != "1":
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + {requirements!r})
print("套件已就緒；接著展開內嵌教材。")
'''
    bootstrap=f'''# Step 2：展開此版本自帶的程式、資料、Skill；不需要先上 GitHub
import base64, hashlib, io, json, os, pathlib, sys, tempfile, zipfile
PAYLOAD_SHA256 = {checksum!r}
MATERIAL_VERSION = {material_version!r}
raw = base64.b64decode({encoded!r})
assert hashlib.sha256(raw).hexdigest() == PAYLOAD_SHA256
ROOT = pathlib.Path(tempfile.mkdtemp(prefix="hp_workshop_010_"))
with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    archive.extractall(ROOT)
sys.path.insert(0, str(ROOT / "src"))
os.environ["PYTHONPATH"] = str(ROOT / "src")
OUT = ROOT / "runs" / "my_work"
OUT.mkdir(parents=True)
print("教材版本", MATERIAL_VERSION, "；模擬資料；模型 API 呼叫數 0")
print("教材：", ROOT)
print("成果：", OUT)
'''
    export='''# 最後一步：下載成果。Colab 的暫存檔不會因儲存 notebook 而自動保留。
import shutil
artifact = shutil.make_archive(str(ROOT / "my_work_010"), "zip", OUT)
print("成果 ZIP：", artifact)
try:
    from google.colab import files
except ImportError:
    print("本機環境：請從上面路徑取得 ZIP。")
else:
    files.download(artifact)
'''
    lessons=json.loads((ROOT/'scripts/lesson_cells.json').read_text())
    for filename,lesson in lessons.items():
        cells=[('markdown',lesson['intro'].replace('{{VERSION}}',material_version)),('code',setup),('code',bootstrap)]
        cells.extend((c['type'],c['source']) for c in lesson['cells'])
        cells.extend([('markdown','## 保存與交付\n\n請先核對本章驗收結果，再下載成果；每章使用獨立資料夾。'),('code',export)])
        result=[]
        for i,(kind,source) in enumerate(cells):
            cell={'cell_type':kind,'id':f'cell-{i:03}','metadata':{},'source':source.splitlines(keepends=True)}
            if kind=='code':
                cell.update(execution_count=None,outputs=[])
            result.append(cell)
        doc={'nbformat':4,'nbformat_minor':5,'metadata':{
            'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},
            'language_info':{'name':'python','version':'3.11'},
            'hp_workshop':{'version':material_version,'payload_sha256':checksum}},'cells':result}
        (ROOT/'notebooks'/filename).write_text(json.dumps(doc,ensure_ascii=False,indent=1)+'\n')
    (ROOT/'PAYLOAD.json').write_text(json.dumps({'sha256':checksum,'files':hashes},ensure_ascii=False,indent=2)+'\n')
    print(f'Built {len(lessons)} notebooks; payload {len(raw)} bytes; {checksum}')


if __name__=='__main__':
    build()
