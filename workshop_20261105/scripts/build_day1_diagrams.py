"""產生可編輯的 draw.io 狀態圖；PNG 由 draw.io 桌面 CLI 匯出。"""
from pathlib import Path
from xml.etree.ElementTree import Element, SubElement, ElementTree

OUT = Path(__file__).resolve().parents[1]/'day1/assets'


def build(name, title, tools, context):
    doc = Element('mxfile', host='drawio')
    diagram = SubElement(doc, 'diagram', name=title)
    model = SubElement(diagram, 'mxGraphModel', page='1', pageWidth='1100', pageHeight='780')
    root = SubElement(model, 'root')
    SubElement(root, 'mxCell', id='0')
    SubElement(root, 'mxCell', id='1', parent='0')

    def box(id, text, x, y, w, h, color='#DBEAFE', shape='rounded=1;'):
        cell = SubElement(root, 'mxCell', id=id, value=text, parent='1', vertex='1',
            style=f'{shape}whiteSpace=wrap;html=1;fillColor={color};strokeColor=#64748B;fontColor=#0F172A;fontFamily=PingFang TC;fontSize=18;spacing=10;')
        SubElement(cell, 'mxGeometry', x=str(x), y=str(y), width=str(w), height=str(h), **{'as':'geometry'})

    def edge(id, source, target, label='', style='', points=()):
        cell = SubElement(root, 'mxCell', id=id, value=label, parent='1', edge='1', source=source, target=target,
            style='edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;strokeWidth=2;fontFamily=PingFang TC;fontSize=16;labelBackgroundColor=#FFFFFF;'+style)
        geometry=SubElement(cell, 'mxGeometry', relative='1', **{'as':'geometry'})
        if points:
            array=SubElement(geometry, 'Array', **{'as':'points'})
            for x,y in points:
                SubElement(array, 'mxPoint', x=str(x), y=str(y))

    box('title', title, 30, 15, 1020, 60, '#FFFFFF', 'text;strokeColor=none;')
    box('state', '共同狀態 State：問題與對話 messages｜工具紀錄 tool_log｜模型次數 turns｜報告 report\n每走完一個節點，就更新這份工作紀錄；本章不示範中斷持久保存。', 30, 90, 1020, 85, '#F1F5F9')
    box('start','START\n收到研究問題',50,240,180,70,'#D1FAE5','ellipse;')
    box('model','model 模型\n讀問題、證據與規則',300,230,230,90)
    box('route','接著做什麼？',610,215,190,120,'#FEF3C7','rhombus;')
    box('tools','tools 工具\n'+tools,340,410,350,95,'#EDE9FE')
    box('stop','stop 停止\n第 6 次仍要求工具：\n回報尚未完成',825,410,225,100,'#FEE2E2')
    box('end','END\n交付回答或待確認',840,230,210,90,'#D1FAE5','ellipse;')
    box('context',context,50,560,1000,85,'#F8FAFC')
    edge('a','start','model')
    edge('b','model','route')
    edge('c','route','end','沒有工具要求')
    edge('d','route','tools','需要工具，未達 6 次', 'exitX=0.5;exitY=1;entryX=1;entryY=0.5;', [(705,455)])
    edge('e','tools','model','工具結果寫回對話','exitX=0;exitY=0.5;entryX=0.5;entryY=1;',[(285,457),(285,360),(415,360)])
    edge('f','route','stop','仍需工具，已達 6 次','exitX=1;exitY=0.8;entryX=0.5;entryY=0;',[(935,340)])
    edge('g','stop','end','','exitX=1;exitY=0.5;entryX=1;entryY=0.5;',[(1080,460),(1080,275)])
    OUT.mkdir(parents=True,exist_ok=True)
    ElementTree(doc).write(OUT/(name+'.drawio'), encoding='utf-8', xml_declaration=True)


if __name__=='__main__':
    build('01_research_state','第一份研究：LangGraph 如何安排模型與工具',
          '查詢教材 JSON，傳回產品資料', '你只要改「研究問題」。模型選擇要查什麼，工具傳回資料，LangGraph 決定下一步。\n資料是模擬的；模型 API 與工具執行是真的。')
    build('02_skill_state','加入 Skill：流程相同，研究方法可以重複使用',
          '查詢教材 JSON，傳回產品資料', 'SKILL.md → 每次模型節點都會讀取的研究規則（旁路輸入，不是另一個工作節點）。\n你改白話規則，同一個問題重跑，核對欄位、未知值與採購問題是否符合新規則。')
    build('02b_mcp_state','接上 MCP：模型透過工具讀取 SQLite',
          'MCP Client → MCP Server → SQLite\n探索工具、查詢資料、傳回結果', '模型先透過 MCP 探索可用工具；每次工具呼叫都經過真實 stdio 協定與 SQLite 唯讀查詢。\nMCP 改變資料的取得方式；Skill 規則仍會傳給模型。不是正式企業系統，也不連官網。')
