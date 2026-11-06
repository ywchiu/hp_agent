"""第二天各 graph 的可編輯狀態圖。"""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree
OUT=Path(__file__).resolve().parents[1]/'day2/assets'


def build(name,title,labels,edges,note):
    doc=Element('mxfile',host='drawio');diagram=SubElement(doc,'diagram',name=title)
    model=SubElement(diagram,'mxGraphModel',page='1',pageWidth='1260',pageHeight='660')
    root=SubElement(model,'root');SubElement(root,'mxCell',id='0');SubElement(root,'mxCell',id='1',parent='0')
    def box(id,text,x,y,w,h,color='#DBEAFE',shape='rounded=1;'):
        cell=SubElement(root,'mxCell',id=id,value=text,parent='1',vertex='1',style=f'{shape}whiteSpace=wrap;html=1;fillColor={color};strokeColor=#64748B;fontColor=#0F172A;fontFamily=PingFang TC;fontSize=18;spacing=12;')
        SubElement(cell,'mxGeometry',x=str(x),y=str(y),width=str(w),height=str(h),**{'as':'geometry'})
    box('title',title,20,15,1190,55,'#FFFFFF','text;strokeColor=none;')
    box('state','State 工作紀錄：'+note,20,85,1190,100,'#F1F5F9')
    for i,(id,text,color) in enumerate(labels): box(id,text,20+i*245,250,210,105,color)
    for i,(a,b,label,loop) in enumerate(edges):
        style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;strokeWidth=2;fontFamily=PingFang TC;fontSize=16;labelBackgroundColor=#FFFFFF;'
        if loop: style+='exitX=0.5;exitY=1;entryX=0.5;entryY=1;'
        cell=SubElement(root,'mxCell',id='e'+str(i),value=label,parent='1',edge='1',source=a,target=b,style=style)
        geo=SubElement(cell,'mxGeometry',relative='1',y='0' if loop else '-65',**{'as':'geometry'})
        if loop:
            xs={id:125+j*245 for j,(id,_,_) in enumerate(labels)}
            points=SubElement(geo,'Array',**{'as':'points'})
            for x,y in [(xs[a],440),(xs[b],440)]:SubElement(points,'mxPoint',x=str(x),y=str(y))
    box('boundary','真實公開來源 + 教學採購需求｜官網規格 ≠ 台灣指定 SKU／報價／服務權益\n不確定就留下供應商問題。完整步驟與驗收請看圖下方。',20,510,1190,80,'#F8FAFC')
    OUT.mkdir(parents=True,exist_ok=True);ElementTree(doc).write(OUT/(name+'.drawio'),encoding='utf-8',xml_declaration=True)


def build_review():
    """區分流程外的比較規則與實際 LangGraph 人工審核。"""
    build('06_review','L06｜來源觀察、兩週比較與人工審核',
        [('draft','模型產生 RFQ\n台灣120台詢價草稿','#EDE9FE'),
         ('review','review / interrupt\n暫停等候人工決定','#FEF3C7'),
         ('decision','人工選擇\n等待／修改\n核准／駁回','#DBEAFE'),
         ('archive','archive 或 END\n核准存本機；駁回結束','#DBEAFE'),
         ('end','END\n回執 sent=False','#D1FAE5')],
        [('draft','review','',False),('review','decision','',False),
         ('decision','archive','核准／駁回',False),('archive','end','',False),
         ('decision','review','修改 → 新指紋 → 重新審核',True)],
        '流程外：真實PDF快照與歷史；教學模擬報價比較（兩者分開標示）\nLangGraph：draft 含來源／比較附件、decision 決定、receipt 回執；版本改變需重新審核。')
    from xml.etree.ElementTree import parse
    path=OUT/'06_review.drawio'; doc=parse(path); root=doc.find('.//root')
    doc.find('.//mxGraphModel').set('pageHeight','860')
    for cell in root.findall('mxCell'):
        geo=cell.find('mxGeometry')
        if geo is None: continue
        if cell.get('id') in {'draft','review','decision','archive','end'}: geo.set('y','440')
        if cell.get('id')=='e4':
            for point in geo.findall('./Array/mxPoint'): point.set('y','625')
        if cell.get('id')=='boundary':
            geo.set('y','690');cell.set('value','價格40,000 → 34,000為教學模擬，非真實報價；PDF改動不等於降價。\n三種獨立分支演練：核准1筆／改稿再審1筆／駁回0筆；重跑不增加，實際寄送皆0。')
    def box(id,text,x,w,color):
        cell=SubElement(root,'mxCell',id=id,value=text,parent='1',vertex='1',
            style=f'rounded=1;whiteSpace=wrap;html=1;fillColor={color};strokeColor=#64748B;fontColor=#0F172A;fontFamily=PingFang TC;fontSize=18;spacing=12;')
        SubElement(cell,'mxGeometry',x=str(x),y='225',width=str(w),height='110',**{'as':'geometry'})
    box('live','真實官方PDF觀察\n時間、指紋、有效基準\n失敗不覆蓋；不推定價格',20,270,'#F1F5F9')
    box('weeks','兩週教學模擬報價\n先對齊SKU／市場／稅別\n再計算變動率與門檻',345,270,'#EDE9FE')
    box('route','比較規則判定（流程外）\n重大變化 → 進入待審\n條件不符／資料不足 → 補查',670,300,'#FEF3C7')
    box('record','無重大變化\n保留紀錄\n不新增待審任務',1025,185,'#D1FAE5')
    for id,a,b,label in [('compare','weeks','route',''),('unchanged','route','record','未達門檻')]:
        c=SubElement(root,'mxCell',id=id,parent='1',edge='1',source=a,target=b,value=label,
            style='edgeStyle=orthogonalEdgeStyle;endArrow=block;strokeWidth=2;fontFamily=PingFang TC;fontSize=15;labelBackgroundColor=#FFFFFF;')
        SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'})
    c=SubElement(root,'mxCell',id='major',parent='1',edge='1',source='route',target='draft',value='重大變化：建立指定版本的待審任務',
        style='edgeStyle=orthogonalEdgeStyle;endArrow=block;strokeWidth=2;exitX=0.5;exitY=1;entryX=0.5;entryY=0;fontFamily=PingFang TC;fontSize=16;labelBackgroundColor=#FFFFFF;')
    g=SubElement(c,'mxGeometry',relative='1',**{'as':'geometry'}); points=SubElement(g,'Array',**{'as':'points'})
    for x,y in [(820,390),(125,390)]:SubElement(points,'mxPoint',x=str(x),y=str(y))
    doc.write(path,encoding='utf-8',xml_declaration=True)


if __name__=='__main__':
    blue='#DBEAFE';green='#D1FAE5';yellow='#FEF3C7';purple='#EDE9FE'
    build('03_rag','L03｜RAG：問題、片段與可驗證的引用', [('start','START\n交辦問題',green),('retrieve','retrieve 檢索\n排除桌機／未核實線索',blue),('answer','answer 模型回答\n只依本次片段',purple),('check','check 檢查\n引用 ID 存在嗎？',yellow),('end','END\n答案＋缺口＋來源',green)], [('start','retrieve','',False),('retrieve','answer','',False),('answer','check','',False),('check','end','存在不等於支持結論',False)], 'question 問題 → rows 片段 → report 回答 → validation 引用檢查\n詞彙檢索，不使用 embedding；引用的事實支持程度仍由人核對。')
    build('04_team','L04｜研究團隊：獨立模型呼叫與有界修訂',[('plan','plan / Planner\n訂範圍與缺口',blue),('research','research\nHP／Lenovo／Dell\n各呼叫一次模型',purple),('write','write / Writer\n彙整需求與證據',blue),('review','review / Reviewer\n回到證據查核',yellow),('end','END\n矩陣、報告、待詢價',green)], [('plan','research','',False),('research','write','',False),('write','review','',False),('review','end','到修訂上限',False),('review','write','最多修訂一輪',True)], 'task 任務、plan 計畫、notes 品牌交接、report 報告、review 意見、revisions 次數\n共用模型，角色輸入分開；27 格矩陣作為證據清單，不把缺口填成合格。')
    build('05_recovery','L05｜跨程序恢復：checkpoint 與操作帳本',[('hp','HP 節點\n保存 checkpoint',blue),('lenovo','Lenovo 節點\n帳本已寫入→故意中斷',yellow),('dell','Dell 節點\n恢復後才研究',blue),('finish','finish 彙整\n三品牌報告',purple),('end','END\n三筆唯一結果',green)], [('hp','lenovo','',False),('lenovo','dell','恢復後接續',False),('dell','finish','',False),('finish','end','',False),('lenovo','lenovo','新程序重進；讀回帳本，不重查模型',True)], 'results 已完成品牌 + checkpoints.sqlite 下一步；operations.sqlite 已提交結果\n中斷後 checkpoint 只有 HP，但帳本有 HP、Lenovo。兩者位於不同交易。')
    build_review()
