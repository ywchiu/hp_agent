"""下午實作：可讀的恢復證據、比較規則與審核分支；不呼叫模型。"""
from copy import deepcopy
import json
import math
from pathlib import Path
try:
    import day2_case as case
except ImportError:
    import procurement as case


def recovery_table(state):
    rows = ["|品牌|Checkpoint 已完成|已提交唯一結果|下一個節點|", "|---|---|---|---|"]
    for brand in ("HP", "Lenovo", "Dell"):
        rows.append(f"|{brand}|{'是' if brand in state['completed_brands'] else '否'}|{state['effects'].get(brand, 0)}|{'待接續' if brand in state['next'] else '—'}|")
    rows += ["", "|執行順序|品牌|這次是否沿用已提交結果|", "|---|---|---|"]
    rows += [f"|{i}|{e['brand']}|{'沿用，不再呼叫模型' if e['reused'] else '本次取得結果'}|" for i,e in enumerate(state['execution'], 1)]
    return "\n".join(rows)


def compare_quotes(old, new, threshold=10):
    """先確認條件，再算幅度；PDF 指紋變動不會進到這裡冒充報價。"""
    fields = ('sku', 'market', 'currency', 'tax', 'configuration', 'simulation')
    if not isinstance(threshold, (int,float)) or isinstance(threshold,bool) or not math.isfinite(threshold) or threshold <= 0:
        raise ValueError('門檻必須是大於零的有限數字。')
    if old.get('status') != 'ok' or new.get('status') != 'ok':
        return {'route':'資料不足', 'reason':'取得失敗；保留有效基準，不把查不到當成產品消失。'}
    if any(not old.get(k) or not new.get(k) for k in fields[:-1]) or any(old.get(k)!=new.get(k) for k in fields):
        return {'route':'不可直接比較', 'reason':'SKU、市場、幣別、稅別、配置或模擬標示不同／缺失。'}
    prices = (old.get('price'), new.get('price'))
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or v<=0 for v in prices):
        return {'route':'資料不足', 'reason':'沒有可用的正式價格；不能自行猜測。'}
    change = (prices[1]-prices[0])/prices[0]*100
    return {'route':'重大變化待審' if abs(change)>=threshold else '無重大變化',
            'change_pct':round(change,2), 'threshold_pct':threshold,
            'reason':'同條件價格幅度達門檻。' if abs(change)>=threshold else '保存紀錄，不建立通知。',
            'event_id':case.digest({'old':{k:old.get(k) for k in (*fields,'price')}, 'new':{k:new.get(k) for k in (*fields,'price')}, 'threshold':threshold})}


def teaching_weeks(new_price=34000, threshold=10):
    # 投影片的 40000→34000 僅為規則演練，絕非 HP 官網或供應商報價。
    first = dict(status='ok', sku='TRAINING-32GB-1TB', market='TW', currency='TWD',
                 tax='含稅', configuration='32GB / 1TB', price=40000,
                 observed_at='模擬第一週', source='教學模擬報價單，非真實市場證據', simulation=True)
    second = dict(first, price=new_price, observed_at='模擬第二週')
    variants = [('同條件第二週',second), ('沒有變動',dict(first,observed_at='模擬第二週')),
                ('不同 SKU',dict(second,sku='TRAINING-OTHER')),
                ('官網讀取失敗',dict(second,status='data_error'))]
    return {'simulation':True, 'first':first, 'second':second,
            'comparisons':[dict(scenario=name, **compare_quotes(first,row,threshold)) for name,row in variants]}


def monitor_once(out, fetch=None):
    out=Path(out)
    current=(fetch or case.fetch_snapshot)()
    case.save(out/'latest.json',current)
    baseline=out/'baseline.json'
    if baseline.exists():
        old=json.loads(baseline.read_text())
        result={'old':old,'new':current,'status':case.compare_snapshots(old,current)}
    elif current['status']=='ok':
        case.save(baseline,current)
        result={'old':None,'new':current,'status':'baseline_created'}
    else:
        result={'old':None,'new':current,'status':'data_error'}
    # 每次觀察各留一份；基準絕不因失敗或檔案改動自動覆寫。
    history=out/'history.jsonl'
    with history.open('a',encoding='utf-8') as f:
        f.write(json.dumps(result,ensure_ascii=False)+'\n')
    case.save(out/'comparison.json',result)
    return result


def revise_once(out, requirement):
    requirement=requirement.strip()
    if not requirement: raise ValueError('請先填補充要求。')
    state=case.approval(out)
    if not state['pending']: return state
    marker='補充要求：'+requirement
    if marker in state['draft']['body']: return state
    before=deepcopy(state['draft'])
    updated=case.approval(out,decision={'action':'revise','hash':state['hash'],
        'text':state['draft']['body']+'\n\n'+marker})
    case.save(Path(out)/'revision.json',{'before':before,'old_hash':state['hash'],
        'after':updated['draft'],'new_hash':updated['hash'],'reason':requirement})
    return updated


def decide_once(out, action, reason):
    if action not in ('wait','approve','reject'): raise ValueError('未知決定。')
    state=case.approval(out)
    if action=='wait' or not state['pending']: return state
    if not reason.strip(): raise ValueError('核准或駁回前請填寫理由。')
    result=case.approval(out,decision={'action':action,'hash':state['hash']})
    case.save(Path(out)/'decision.json',{'action':action,'reason':reason,
        'draft_hash':state['hash'],'recipient':state['draft']['recipient'],
        'outbox_count':result['outbox_count'],'sent_count':result['sent_count']})
    return result


def exercise_branches(out, draft):
    """三份獨立測試 Thread；重用同一草稿，不額外產生模型用量。"""
    rows=[]
    for branch in ('approve','revise','reject'):
        folder=Path(out)/branch
        state=case.approval(folder,draft=deepcopy(draft))
        if branch=='revise' and state['pending']:
            state=revise_once(folder,'【分支演練】請附資料日期，並確認這是詢價而非訂購。')
            revision=json.loads((folder/'revision.json').read_text())
            try:
                case.approval(folder,decision={'action':'approve','hash':revision['old_hash']})
            except ValueError as e:
                if '草稿已更動' not in str(e): raise
            else: raise AssertionError('舊版本竟通過核准')
        action='reject' if branch=='reject' else 'approve'
        state=decide_once(folder,action,'教學分支驗證；僅存本機。')
        again=decide_once(folder,action,'重複操作驗證。')
        assert state['outbox_count']==again['outbox_count']==(0 if branch=='reject' else 1)
        assert state['sent_count']==0 and not state['pending']
        rows.append({'branch':branch,'outbox_count':state['outbox_count'],
                     'repeat_outbox_count':again['outbox_count'],'sent_count':0})
    return rows
