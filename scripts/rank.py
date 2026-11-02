"""Calculate comparable snapshot deltas; output a draft, never publish automatically."""
import argparse
import datetime as dt
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def calculate(old, new):
    previous = {p['id']: p for p in old['projects']}
    rows = []
    for project in new['projects']:
        before = previous.get(project['id'])
        if before is None:
            continue
        delta = project['stars'] - before['stars']
        rows.append({'id': project['id'], 'full_name': project['full_name'], 'stars': project['stars'], 'delta7': delta, 'growth_pct': round(delta / before['stars'] * 100, 1) if before['stars'] else None})
    return sorted(rows, key=lambda p: (-p['delta7'], p['id']))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Use constructed fixtures; do not write files')
    args = parser.parse_args()
    if args.dry_run:
        old = json.loads((ROOT/'tests/fixtures/snapshot.json').read_text())
        new = json.loads(json.dumps(old))
        new['captured_at'] = '2026-11-08T22:30:00+00:00'
        new['projects'][0]['stars'] = 130
    else:
        snapshots = sorted((ROOT/'data/snapshots').glob('*.json'))
        if not snapshots:
            print('没有快照', file=sys.stderr); return 2
        new = json.loads(snapshots[-1].read_text())
        target = dt.datetime.fromisoformat(new['captured_at']) - dt.timedelta(days=7)
        candidates = []
        for path in snapshots[:-1]:
            candidate = json.loads(path.read_text())
            distance = abs((dt.datetime.fromisoformat(candidate['captured_at']) - target).total_seconds())
            if distance <= 6 * 3600: candidates.append((distance,candidate))
        if not candidates:
            print('缺少可比较的七日前快照；不生成榜单', file=sys.stderr); return 2
        old = min(candidates,key=lambda x:x[0])[1]
    week = dt.datetime.fromisoformat(new['captured_at']).strftime('%G-W%V')
    eligible = {p['id'] for p in new['projects'] if not p.get('archived', False) and p.get('pushed_at') and (dt.datetime.fromisoformat(new['captured_at']) - dt.datetime.fromisoformat(p['pushed_at'].replace('Z','+00:00'))).total_seconds() <= 30 * 86400}
    rows = [p for p in calculate(old,new) if p['id'] in eligible and p['delta7'] >= 30]
    meta = {p['id']:p for p in new['projects']}
    curated = {p['id']:p for p in json.loads((ROOT/'data/projects.json').read_text())['projects']} if not args.dry_run else {}
    for row in rows:
        row['review_flags'] = list(curated.get(row['id'], {}).get('flags', []))
        forks = meta[row['id']].get('forks', 0)
        if (row['stars'] < 500 and row['delta7'] / max(row['stars'], 1) > 1) or (row['delta7'] > 200 and forks / max(row['stars'], 1) < 0.005):
            row['review_flags'].append('unusual_growth_review')
    result = {'week':week, 'review_state':'pending', 'start':old['captured_at'], 'end':new['captured_at'], 'projects':rows}
    if args.dry_run:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        week = dt.datetime.fromisoformat(new['captured_at']).strftime('%G-W%V')
        target = ROOT/'data/weekly'/f'{week}.draft.json'
        target.parent.mkdir(parents=True,exist_ok=True)
        if (ROOT/'data/weekly/approved'/f'{week}.json').exists():
            print('本期已审核，未覆盖草稿', file=sys.stderr); return 1
        target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
        print(f'已生成待审核草稿：{target}')
    return 0
if __name__ == '__main__': raise SystemExit(main())
