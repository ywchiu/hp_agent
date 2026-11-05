"""只供離線驗證的模型替身，不是教材的研究模型。"""
import json
from types import SimpleNamespace


class Item:
    def __init__(self, **fields):
        self.fields=fields
        self.type=fields['type']
    def model_dump(self, **kwargs):
        return dict(self.fields)


def tool(name, arguments, number=1):
    return Item(type='function_call', name=name, arguments=json.dumps(arguments), call_id=f'call_{number}', id=f'fc_{number}')


def response(calls=(), text=''):
    output=list(calls) or [Item(type='message', role='assistant', content=[{'type':'output_text','text':text,'annotations':[]}])]
    return SimpleNamespace(output=output, output_text=text)


class FakeClient:
    def __init__(self, sequence=None, **kwargs):
        self.sequence=list(sequence) if sequence is not None else None
        self.requests=[]
        self.responses=self
        self.closed=False

    async def create(self, **kwargs):
        self.requests.append(kwargs)
        if self.sequence is not None:
            return self.sequence.pop(0)
        messages=kwargs['input']
        task=messages[0]['content']
        results=[m for m in messages if m.get('type')=='function_call_output']
        if not results:
            if '999' in task:
                return response([tool('read_product_by_id',{'product_id':'DEMO-TW-999'})])
            return response([tool('find_products_by_model',{'model':'DemoBook A','market':'TW'})])
        if len(results)==1 and '999' not in task:
            return response([tool('read_product_by_id',{'product_id':'DEMO-TW-016'},2),
                             tool('read_product_by_id',{'product_id':'DEMO-TW-032'},3)])
        text='離線模型替身的測試報告（不是實際模型回答）。DEMO-TW-016：1 年；DEMO-TW-032：待確認。2026-10-26。'
        if '999' in task:
            text='離線模型替身：DEMO-TW-999 查不到資料，需向資料管理人員確認 ID。'
        return response(text=text)

    async def close(self):
        self.closed=True
