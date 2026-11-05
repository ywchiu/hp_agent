"""從明文原始碼產生 notebooks；第一天下午不需要下載整個專案。"""
import hashlib
import json
from pathlib import Path
from day1_cells import day1_lessons

ROOT = Path(__file__).resolve().parents[1]


def cell(kind, source, index, folded=False):
    metadata = {'cellView': 'form', 'jupyter': {'source_hidden': True}} if folded else {}
    result = {'cell_type': kind, 'id': f'cell-{index:03}', 'metadata': metadata,
              'source': source.splitlines(keepends=True)}
    if kind == 'code':
        result.update(execution_count=None, outputs=[])
    return result


def source_files():
    return sorted([ROOT/'data/products.json', ROOT/'day1/requirements.txt']+
                  list((ROOT/'day1').glob('*.py'))+list((ROOT/'day1').glob('*.md')))


def documents():
    version = json.loads((ROOT/'course.json').read_text())['material_version']
    return {name: {'nbformat': 4, 'nbformat_minor': 5,
                  'metadata': {'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
                               'language_info': {'name': 'python', 'version': '3.11'}, 'colab': {'name': name},
                               'hp_workshop': {'version': version, 'day': 1}},
                  'cells': [cell(kind, source, i, folded) for i, (kind, source, folded) in enumerate(cells)]}
            for name, cells in day1_lessons(ROOT).items()}


def build():
    docs = documents()
    for name, doc in docs.items():
        (ROOT/'notebooks'/name).write_text(json.dumps(doc, ensure_ascii=False, indent=1)+'\n')
    paths = source_files()
    manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    (ROOT/'NOTEBOOK_SOURCES.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n')
    print(f'Built {len(docs)} notebooks from plain source files.')


if __name__ == '__main__':
    build()
