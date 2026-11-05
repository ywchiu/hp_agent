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


if __name__=='__main__':
    blue='#DBEAFE';green='#D1FAE5';yellow='#FEF3C7';purple='#EDE9FE'
    build('03_rag','L03｜RAG：問題、片段與可驗證的引用', [('start','START\n交辦問題',green),('retrieve','retrieve 檢索\n排除桌機／未核實線索',blue),('answer','answer 模型回答\n只依本次片段',purple),('check','check 檢查\n引用 ID 存在嗎？',yellow),('end','END\n答案＋缺口＋來源',green)], [('start','retrieve','',False),('retrieve','answer','',False),('answer','check','',False),('check','end','存在不等於支持結論',False)], 'question 問題 → rows 片段 → report 回答 → validation 引用檢查\n詞彙檢索，不使用 embedding；引用的事實支持程度仍由人核對。')
    build('04_team','L04｜研究團隊：獨立模型呼叫與有界修訂',[('plan','plan / Planner\n訂範圍與缺口',blue),('research','research\nHP／Lenovo／Dell\n各呼叫一次模型',purple),('write','write / Writer\n彙整需求與證據',blue),('review','review / Reviewer\n回到證據查核',yellow),('end','END\n矩陣、報告、待詢價',green)], [('plan','research','',False),('research','write','',False),('write','review','',False),('review','end','到修訂上限',False),('review','write','最多修訂一輪',True)], 'task 任務、plan 計畫、notes 品牌交接、report 報告、review 意見、revisions 次數\n共用模型，角色輸入分開；27 格矩陣作為證據清單，不把缺口填成合格。')
    build('05_recovery','L05｜跨程序恢復：checkpoint 與操作帳本',[('hp','HP 節點\n保存 checkpoint',blue),('lenovo','Lenovo 節點\n帳本已寫入→故意中斷',yellow),('dell','Dell 節點\n恢復後才研究',blue),('finish','finish 彙整\n三品牌報告',purple),('end','END\n三筆唯一結果',green)], [('hp','lenovo','',False),('lenovo','dell','恢復後接續',False),('dell','finish','',False),('finish','end','',False),('lenovo','lenovo','新程序重進；讀回帳本，不重查模型',True)], 'results 已完成品牌 + checkpoints.sqlite 下一步；operations.sqlite 已提交結果\n中斷後 checkpoint 只有 HP，但帳本有 HP、Lenovo。兩者位於不同交易。')
    build('06_review','L06｜interrupt：人決定要不要保存詢價草稿',[('draft','模型產生 RFQ\n台灣120台詢價草稿',purple),('review','review / interrupt\n暫停等候人工決定',yellow),('decision','人工選擇\n改稿／核准／駁回',blue),('archive','archive 或 END\n核准存本機；駁回結束',blue),('end','END\n回執 sent=False',green)], [('draft','review','',False),('review','decision','',False),('decision','archive','核准／駁回',False),('archive','end','',False),('decision','review','修改→新 hash→重新審核',True)], 'draft 草稿（對象、主旨、內容、需求／證據hash）、decision 決定、receipt 回執\n另可讀取真實 PDF 快照比較：內容變動待審，取得失敗不覆蓋有效基準。')
