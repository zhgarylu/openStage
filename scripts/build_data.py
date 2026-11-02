"""Build the public site dataset from curated projects and approved issues."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def write_json(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp=path.with_suffix('.tmp')
    tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
    tmp.replace(path)
def build(root=ROOT):
    catalog=json.loads((root/'data/projects.json').read_text())
    snapshots=sorted((root/'data/snapshots').glob('*.json'))
    if snapshots:
        current=json.loads(snapshots[-1].read_text())
        meta={p['id']:p for p in current['projects']}
        for p in catalog['projects']:
            update=meta.get(p['id'])
            if update:
                for field in ('stars','forks','pushed_at','full_name','html_url','archived'):
                    if field in update:p[field]=update[field]
                p['captured_at']=current['captured_at']
        catalog['captured_at']=current['captured_at']
    approved=[]
    for file in sorted((root/'data/weekly/approved').glob('*.json'),reverse=True):
        issue=json.loads(file.read_text())
        if issue.get('review_state')=='approved' and issue.get('reviewed_by') and issue.get('reviewed_at'):
            approved.append(issue)
    write_json(root/'site/src/data/projects.json',catalog)
    write_json(root/'site/src/data/weekly.json',approved)
if __name__=='__main__':build()
