import argparse
import json
from pathlib import Path
from workshop.catalog import seed
from workshop.flows import basic_report, retrieve, research, recovery, save


def main():
    p=argparse.ArgumentParser()
    p.add_argument('lab',choices=['basic','rag','research','mcp','recover-start','recover-resume'])
    p.add_argument('--out',default='runs/demo')
    p.add_argument('--thread',default='research-demo-01')
    args=p.parse_args()
    out=Path(args.out)
    out.mkdir(parents=True,exist_ok=True)
    if args.lab=='basic':
        result=basic_report()
    elif args.lab=='rag':
        result={'before':retrieve(current_only=False),'after':retrieve()}
    elif args.lab=='research':
        result=research()
    elif args.lab=='mcp':
        from workshop.mcp_client import run
        result=run(seed(out/'catalog.sqlite'))
    else:
        result=recovery(out,args.thread,resume=args.lab=='recover-resume',crash=args.lab=='recover-start')
    save(out/(args.lab+'.json'),result)
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
