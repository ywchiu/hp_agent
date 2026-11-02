"""教學用 LangGraph 節點：固定資料與規則，模型研究由 Antigravity 操作。"""
import hashlib
import json
import sqlite3
from pathlib import Path
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import interrupt, Command
from workshop.catalog import ROOT, load


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def save(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


def basic_report(rows=None, skill_path=None):
    rows = rows if rows is not None else load('products.json')
    rule = Path(skill_path or ROOT / 'skills/product-research/SKILL.md').read_text(encoding='utf-8')
    class State(TypedDict, total=False):
        rows: list
        comparison: list
        missing: list
    def fetch(state):
        return {'rows': [r for r in rows if r['market'] == 'TW' and r['model'] == 'DemoBook A']}
    def compare(state):
        return {'comparison': [{'id':r['id'], 'memory_gb':r['memory_gb'], 'storage_gb':r['storage_gb'],
                                 'warranty':r['warranty_years'] if r['warranty_years'] is not None
                                 else ('待確認' if '[unknown_warranty]' in rule else '未填'),
                                 'source_date':r['updated']} for r in state['rows']],
                'missing':[r['id'] for r in state['rows'] if r['warranty_years'] is None]}
    g = StateGraph(State)
    g.add_node('fetch', fetch)
    g.add_node('compare', compare)
    g.add_edge(START, 'fetch')
    g.add_edge('fetch', 'compare')
    g.add_edge('compare', END)
    return g.compile().invoke({})


def retrieve(question='專案 P 出差採購需求', market='TW', current_only=True, k=2):
    """中文字元二元組檢索，示範 metadata filter；不是向量搜尋。"""
    grams = set(question[i:i+2] for i in range(len(question)-1))
    docs = [d for d in load('documents.json') if not current_only or (d['market']==market and d['current'])]
    scored = [(len(grams & set(d['text'][i:i+2] for i in range(len(d['text'])-1))), d) for d in docs]
    return [dict(d, score=score) for score, d in sorted(scored, key=lambda x:-x[0])[:k] if score > 0]


def research(max_rounds=2):
    """有界補查。角色是規則節點；並非四個自主模型 Agent。"""
    class State(TypedDict, total=False):
        round: int
        evidence: list
        gaps: list
        trace: list
        matrix: list
        stop_reason: str
    docs = {d['id']:d for d in load('documents.json')}
    def planner(s):
        return {'trace':s.get('trace', []) + [{'role':'Planner', 'round':s['round'], 'need':s.get('gaps', ['指定 SKU、服務證據'])}]}
    def researcher(s):
        ids = ['SERIES#1'] if s['round']==0 else ['SKU#1', 'SERVICE#3']
        return {'evidence':s.get('evidence', []) + [docs[i] for i in ids],
                'trace':s['trace']+[{'role':'Researcher','added':ids}]}
    def writer(s):
        ids = {d['id'] for d in s['evidence']}
        return {'matrix':[
            {'requirement':'32 GB', 'status':'符合' if 'SKU#1' in ids else '待確認', 'source':'SKU#1' if 'SKU#1' in ids else 'SERIES#1'},
            {'requirement':'三年到府', 'status':'待確認', 'source':'SERVICE#3' if 'SERVICE#3' in ids else None}],
            'trace':s['trace']+[{'role':'Writer','round':s['round']}]}
    def reviewer(s):
        gaps = [r['requirement'] for r in s['matrix'] if r['status']=='待確認']
        return {'gaps':gaps, 'round':s['round']+1,
                'trace':s['trace']+[{'role':'Reviewer','gaps':gaps}]}
    def finish(s):
        return {'stop_reason':'仍有缺口，已達補查上限' if s['gaps'] else '必要條件已有證據'}
    g = StateGraph(State)
    for n, f in [('planner',planner),('researcher',researcher),('writer',writer),('reviewer',reviewer),('finish',finish)]:
        g.add_node(n,f)
    g.add_edge(START,'planner')
    for a,b in [('planner','researcher'),('researcher','writer'),('writer','reviewer'),('finish',END)]:
        g.add_edge(a,b)
    g.add_conditional_edges('reviewer',lambda s:'again' if s['gaps'] and s['round']<=max_rounds else 'stop',
                            {'again':'planner','stop':'finish'})
    return g.compile().invoke({'round':0}, {'recursion_limit':30})


def ledger(path, key, content):
    """測試寄件器與取證工具：相同 key、不同內容必須拒絕。"""
    with sqlite3.connect(path) as db:
        db.execute('CREATE TABLE IF NOT EXISTS operations (key TEXT PRIMARY KEY, hash TEXT, body TEXT)')
        old = db.execute('SELECT hash, body FROM operations WHERE key=?',(key,)).fetchone()
        if old:
            if old[0] != digest(content):
                raise ValueError('operation key reused with different content')
            return {'key':key,'reused':True,'receipt':json.loads(old[1])}
        db.execute('INSERT INTO operations VALUES (?,?,?)',(key,digest(content),json.dumps(content,ensure_ascii=False)))
        return {'key':key,'reused':False,'receipt':content}


def recovery(directory, thread='research-demo-01', resume=False, crash=False):
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    class State(TypedDict, total=False):
        project_id: str
        run_id: str
        results: dict
        report: str
    config={'configurable':{'thread_id':thread}}
    with SqliteSaver.from_conn_string(str(directory/'checkpoints.sqlite')) as cp:
        g=StateGraph(State)
        for row in load('recovery.json'):
            def node(s, row=row):
                with (directory/'execution.jsonl').open('a',encoding='utf-8') as f:
                    f.write(json.dumps({'node':row['brand'],'thread_id':thread})+'\n')
                key=f"{s['run_id']}:{row['brand']}:source"
                result=ledger(directory/'operations.sqlite',key,row)
                if crash and row['brand']=='ASUS':
                    raise RuntimeError('DEMO_CRASH_AFTER_ASUS_WRITE')
                return {'results':dict(s.get('results',{}),**{row['brand']:result})}
            g.add_node(row['brand'],node)
        def report(s):
            text='\n'.join(f"{brand}: {item['receipt']['source_id']}; warranty={item['receipt']['warranty_years']}" for brand,item in s['results'].items())
            (directory/'report.md').write_text('# 模擬研究報告\n'+text+'\nASUS 保固待確認；本表不是即時產品規格。\n',encoding='utf-8')
            return {'report':text}
        g.add_node('report',report)
        for a,b in [(START,'Dell'),('Dell','Lenovo'),('Lenovo','ASUS'),('ASUS','report'),('report',END)]:
            g.add_edge(a,b)
        graph=g.compile(checkpointer=cp)
        previous=graph.get_state(config)
        if resume and not previous.values:
            raise ValueError('找不到原 Thread，不能稱為恢復')
        if not resume and previous.values:
            raise ValueError('Thread 已存在；使用 resume 或換一個輸出資料夾')
        try:
            graph.invoke(None if resume else {'project_id':'notebook-watch','run_id':thread,'results':{}},config)
        finally:
            state=graph.get_state(config)
            save(directory/'state.json',{'thread_id':thread,'next':list(state.next),'values':state.values})
        return state.values


def snapshot(price=34000, **updates):
    return dict({'project':'notebook-watch','sku':'TW-A32','market':'TW','currency':'TWD','tax':'included',
                 'price':price,'source_id':'SIM-W2','date':'2026-11-02','simulated':True},**updates)


def detect(old, new):
    if not old or new.get('price') is None or not new.get('source_id'):
        return {'status':'data_error','reason':'取得失敗或缺價格／來源；不更新有效基準'}
    if any(old.get(k)!=new.get(k) for k in ['project','sku','market','currency','tax']):
        return {'status':'not_comparable','reason':'比較條件不同'}
    if old.get('price') is None or old['price']<=0 or new['price']<=0:
        return {'status':'data_error','reason':'無有效價格'}
    percent=(new['price']-old['price'])/old['price']*100
    status='pending_review' if abs(percent)>=10 else 'no_major_change'
    event={'project':new['project'],'sku':new['sku'],'market':new['market'],'currency':new['currency'],
           'tax':new['tax'],'old_price':old['price'],'new_price':new['price'],'period':new['date']}
    return {'status':status,'percent':percent,'event_id':digest(event)[:20],'old':old,'new':new}


def new_product(record):
    valid=all(record.get(k) for k in ['sku','market','source_id','release_date'])
    return {'status':'pending_review' if valid else 'data_error','kind':'new_product',
            'event_id':digest({'kind':'new_product','record':record})[:20],'record':record}


def approval(directory, event, decision=None, thread='approval-01', crash=None):
    directory=Path(directory)
    directory.mkdir(parents=True,exist_ok=True)
    class State(TypedDict, total=False):
        event: dict
        draft: dict
        decision: str
        decisions: list
        approved_hash: str
        delivery: dict
    with SqliteSaver.from_conn_string(str(directory/'approval.sqlite')) as cp:
        def prepare(s):
            e=s['event']
            text=(f"本週同條件價格變動 {e['percent']:.1f}%；請檢查來源與資料日期。"
                  if 'percent' in e else '模擬新品事件：請核對發布來源、日期與影響。')
            return {'draft':{'version':1,'to':['test-manager@example.invalid'],'channel':'test-sink',
                             'attachment_hash':digest(s['event']),
                             'text':text}}
        def review(s):
            answer=interrupt({'draft':s['draft'],'hash':digest(s['draft']),'evidence':s['event']})
            if answer.get('hash')!=digest(s['draft']):
                raise ValueError('stale approval: 草稿或對象已改變，必須重新審核')
            action=answer.get('action')
            if action not in ['approve','revise','reject']:
                raise ValueError('unknown approval action')
            if action=='revise':
                draft=dict(s['draft'],version=s['draft']['version']+1,text=answer['text'])
                return {'draft':draft,'decision':'revise','approved_hash':'',
                        'decisions':s.get('decisions',[])+[dict(answer,version=s['draft']['version'])]}
            return {'decision':action,'approved_hash':digest(s['draft']) if action=='approve' else '',
                    'decisions':s.get('decisions',[])+[dict(answer,version=s['draft']['version'])]}
        def send(s):
            if s['approved_hash']!=digest(s['draft']):
                raise ValueError('approval does not match draft')
            if crash=='before':
                raise RuntimeError('DEMO_CRASH_BEFORE_SEND')
            result=ledger(directory/'outbox.sqlite',s['event']['event_id'],s['draft'])
            if crash=='after':
                raise RuntimeError('DEMO_CRASH_AFTER_SEND')
            return {'delivery':result}
        g=StateGraph(State)
        for n,f in [('prepare',prepare),('review',review),('send',send)]:
            g.add_node(n,f)
        g.add_edge(START,'prepare')
        g.add_edge('prepare','review')
        g.add_conditional_edges('review',lambda s:s['decision'],{'revise':'review','approve':'send','reject':END})
        g.add_edge('send',END)
        graph=g.compile(checkpointer=cp)
        config={'configurable':{'thread_id':thread}}
        previous=graph.get_state(config)
        if not previous.values and event.get('status')!='pending_review':
            raise ValueError('此事件不需要或尚不能進入通知審核')
        if previous.values and previous.values['event']!=event:
            raise ValueError('Thread 綁定其他事件')
        try:
            if not previous.values:
                graph.invoke({'event':event},config)
            elif decision and previous.next==('review',):
                # 在儲存 resume 值前拒絕失效決定，保留原本待審 interrupt。
                if decision.get('hash')!=digest(previous.values['draft']):
                    raise ValueError('stale approval: 請重新審核目前草稿')
                if decision.get('action') not in ['approve','revise','reject']:
                    raise ValueError('unknown approval action')
                graph.invoke(Command(resume=decision),config)
            elif decision:
                raise ValueError('目前沒有待審單；重複核准不執行')
            elif previous.next==('send',):
                graph.invoke(None,config)
        finally:
            state=graph.get_state(config)
            save(directory/'approval_state.json',{'thread_id':thread,'next':list(state.next),'values':state.values})
        return state.values
