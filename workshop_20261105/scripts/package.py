"""只封裝可發布教材，不帶執行狀態或私人環境。"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

p=argparse.ArgumentParser()
p.add_argument('--out',required=True)
args=p.parse_args()
root=Path(__file__).resolve().parents[1]
output=Path(args.out).resolve()
output.parent.mkdir(parents=True,exist_ok=True)
excluded={'runs','.venv','.git','__pycache__','.ipynb_checkpoints'}
paths=[]
for path in sorted(root.rglob('*')):
    relative=path.relative_to(root)
    if not path.is_file() or any(part in excluded or part.endswith('.egg-info') for part in relative.parts):
        continue
    if path.name.startswith('.env') or path.suffix in {'.pyc','.sqlite','.db','.zip'}:
        continue
    paths.append(path)
manifest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
with zipfile.ZipFile(output,'w',zipfile.ZIP_DEFLATED) as z:
    for path in paths:
        z.write(path,Path(root.name)/path.relative_to(root))
    z.writestr(root.name+'/PACKAGE_MANIFEST.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None
print(f'{output} ({len(paths)} files + manifest; {output.stat().st_size} bytes)')
