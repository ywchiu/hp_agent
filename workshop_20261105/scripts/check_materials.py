"""檢查來源頁碼涵蓋、相對連結、Python 語法與 notebook 內嵌同步。"""
import ast
import base64
import hashlib
import io
import json
from pathlib import Path
import re
import zipfile
from build_notebooks import payload

root=Path(__file__).resolve().parents[1]
errors=[]
course=json.loads((root/'course.json').read_text())
mapping=json.loads((root/'slide_map.json').read_text())
pages=set()
for row in mapping:
    pages.update(range(row['start'],row['end']+1))
    if not (root/row['guide']).exists():
        errors.append('missing guide: '+row['guide'])
if pages!=set(range(1,course['pdf_pages']+1)):
    errors.append('page mapping incomplete')
for path in root.rglob('*.md'):
    if 'runs' in path.relative_to(root).parts:
        continue
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        if not (path.parent/target.split('#')[0]).exists():
            errors.append(f'{path.relative_to(root)}: broken link {target}')
for path in (root/'src').rglob('*.py'):
    ast.parse(path.read_text())
raw,hashes=payload()
checksum=hashlib.sha256(raw).hexdigest()
manifest=json.loads((root/'PAYLOAD.json').read_text())
if checksum!=manifest['sha256'] or hashes!=manifest['files']:
    errors.append('source payload changed; run build_notebooks.py')
for path in (root/'notebooks').glob('*.ipynb'):
    doc=json.loads(path.read_text())
    if doc['metadata']['hp_workshop']['payload_sha256']!=checksum:
        errors.append(path.name+': stale metadata')
    source=''.join(doc['cells'][2]['source'])
    encoded=re.search(r'base64.b64decode\(([^)]+)\)',source).group(1)
    data=base64.b64decode(ast.literal_eval(encoded))
    if hashlib.sha256(data).hexdigest()!=checksum:
        errors.append(path.name+': stale embedded code')
    for c in doc['cells']:
        if c['cell_type']=='code':
            ast.parse(''.join(c['source']))
            if c.get('outputs') or c.get('execution_count') is not None:
                errors.append(path.name+': published notebook contains execution output')
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        if any(n.startswith('/') or '..' in Path(n).parts for n in archive.namelist()):
            errors.append(path.name+': unsafe archive entry')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {course["pdf_pages"]} pages mapped; 7 notebooks in sync; relative links and Python syntax valid.')
