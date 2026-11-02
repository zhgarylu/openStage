"""Collect an all-or-nothing GitHub snapshot; never publishes a ranking."""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]

def fetch(repo, token):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "OpenStage-validation/0.1", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request("https://api.github.com/repos/" + repo, headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        data = json.load(response)
    return {"id": data["id"], "full_name": data["full_name"], "stars": data["stargazers_count"], "forks": data["forks_count"], "pushed_at": data["pushed_at"], "archived": data["archived"], "html_url": data["html_url"]}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dry-run', action='store_true', help='Use offline fixture; do not write files')
    args = parser.parse_args()
    if args.dry_run:
        records = json.loads((ROOT/'tests/fixtures/snapshot.json').read_text())['projects']
    else:
        seeds = json.loads((ROOT/'config/seeds.json').read_text())
        token = os.environ.get('GH_PAT') or os.environ.get('GITHUB_TOKEN', '')
        try:
            records = [fetch(repo, token) for repo in seeds]
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as error:
            print(f'采集失败，未写入快照：{type(error).__name__}', file=sys.stderr)
            return 1
    if len({r['id'] for r in records}) != len(records):
        print('重复仓库 ID，未写入快照', file=sys.stderr)
        return 1
    now = dt.datetime.now(dt.timezone.utc)
    payload = {'captured_at': now.isoformat(), 'projects': records}
    if args.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        target = ROOT/'data/snapshots'/f'{now.date()}.json'
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix('.tmp')
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n')
        temporary.replace(target)
        print(f'已保存 {len(records)} 个项目至 {target}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
