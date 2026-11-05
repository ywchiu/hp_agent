"""檢查頁碼、連結、明文原始碼同步、notebook 語法與發布狀態。"""
import ast
import hashlib
import json
from pathlib import Path
import re
from build_notebooks import documents

root=Path(__file__).resolve().parents[1]
errors=[]
course=json.loads((root/'course.json').read_text())
pages=set()
for row in json.loads((root/'slide_map.json').read_text()):
    pages.update(range(row['start'],row['end']+1))
    if not (root/row['guide']).exists():
        errors.append('missing guide: '+row['guide'])
if pages!=set(range(1,course['pdf_pages']+1)):
    errors.append('page mapping incomplete')
for path in root.rglob('*.md'):
    if any(part in {'runs','.venv','__pycache__'} for part in path.relative_to(root).parts):
        continue
    for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
        if '://' not in target and not target.startswith('#') and not (path.parent/target.split('#')[0]).exists():
            errors.append(f'{path.relative_to(root)}: broken link {target}')
for folder in ['src','day1','day2','scripts','tests']:
    for path in (root/folder).rglob('*.py'):
        ast.parse(path.read_text())
for name, checksum in json.loads((root/'NOTEBOOK_SOURCES.json').read_text()).items():
    if hashlib.sha256((root/name).read_bytes()).hexdigest()!=checksum:
        errors.append(name+': source changed; rebuild notebooks')
expected=documents()
actual={p.name for p in (root/'notebooks').glob('*.ipynb')}
if not set(expected).issubset(actual) or "00_setup.ipynb" in actual:
    errors.append('notebook list differs from generator')
for name, generated in expected.items():
    doc=json.loads((root/'notebooks'/name).read_text())
    if doc!=generated:
        errors.append(name+': stale notebook; rebuild')
    if doc['metadata']['hp_workshop']['day'] in (1,2):
        if '狀態圖' not in ''.join(doc['cells'][0]['source']):
            errors.append(name+': missing opening state diagram')
        text='\n'.join(''.join(c['source']) for c in doc['cells'])
        if not all(f'第 {i} 步' in text for i in range(1,7)):
            errors.append(name+': incomplete learner steps')
    for c in doc['cells']:
        if c['cell_type']!='code':
            continue
        source=''.join(c['source'])
        if doc['metadata']['hp_workshop']['day']==2 and c['metadata'].get('cellView')=='form' and not re.search(r'^#\s*@title\s',source,re.M):
            errors.append(name+': folded Colab cell needs a visible title')
        if source.startswith('%%writefile '):
            source=source.split('\n',1)[1]
        ast.parse(source)
        if 'b64decode' in source or 'import base64' in source:
            errors.append(name+': encoded loader')
        if c.get('outputs') or c.get('execution_count') is not None:
            errors.append(name+': published output must be cleared')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {course["pdf_pages"]} pages, {len(expected)} plain-source notebooks, links, syntax, opening diagrams and learner steps.')
