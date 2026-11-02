"""Approve a draft after editorial review. Specify each approved repository ID."""
import argparse,datetime as dt,json,re,sys
from pathlib import Path
from scripts.build_data import ROOT,write_json

def approve(draft, ids, reviewer, now):
    if draft.get('review_state')!='pending' or not reviewer.strip(): raise ValueError('草稿状态或审核人无效')
    rows=draft.get('projects',[])
    by_id={p['id']:p for p in rows}
    if len(by_id)!=len(rows): raise ValueError('项目 ID 重复')
    if not ids or len(ids)>10 or len(set(ids))!=len(ids) or any(i not in by_id for i in ids): raise ValueError('请提供不重复且属于草稿的项目 ID')
    return {**draft,'review_state':'approved','reviewed_by':reviewer.strip(),'reviewed_at':now,'projects':[by_id[i] for i in ids]}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('week',help='ISO 周，如 2026-W45')
    parser.add_argument('--reviewer',required=True,help='审核人')
    parser.add_argument('--ids',required=True,help='按发布顺序列出项目 ID，以逗号分隔')
    args=parser.parse_args()
    if not re.fullmatch(r'\d{4}-W\d{2}',args.week):parser.error('周格式无效')
    draft_path=ROOT/'data/weekly'/f'{args.week}.draft.json'
    out=ROOT/'data/weekly/approved'/f'{args.week}.json'
    if out.exists():parser.error('该期已发布；请先通过版本管理审查更改')
    try:
        result=approve(json.loads(draft_path.read_text()),[int(s.strip()) for s in args.ids.split(',')],args.reviewer,dt.datetime.now(dt.timezone.utc).isoformat())
    except (OSError,ValueError,KeyError) as e:
        print(f'审核失败：{e}',file=sys.stderr); return 1
    write_json(out,result)
    print(f'审核完成：{out}；运行 python3 -m scripts.build_data 更新站点。')
    return 0
if __name__=='__main__':raise SystemExit(main())
