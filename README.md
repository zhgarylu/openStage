# OpenStage 验证版

面向 AI 短片创作者的静态开源项目目录。当前收录 63 个 GitHub 公开项目：已核验搜索接口返回的仓库身份、元数据及公开描述，并据此整理中文用途；没有逐项安装或实测。显卡、难度与代码要求未核实时保持“未确认”。代码许可证由 GitHub 识别，不能代表模型权重或依赖的许可。

## 本地运行

需要 Node.js 22.23.4+（建议 24）和 Python 3.12+。

```sh
cd site
npm ci
npm run dev
```

`npm run build` 构建静态站；`npm run preview` 预览产物。`ASTRO_TELEMETRY_DISABLED=1` 可关闭 Astro 遥测。测试：`python3 -m unittest discover -s tests`。

## 采集和审核

- `config/seeds.json` 是人工选择的仓库清单，`data/projects.json` 是基于公开描述整理的编辑数据。核对新项目后可补充，两者应同步维护。
- `python3 -m scripts.snapshot --dry-run` 使用离线样例；`python3 -m scripts.snapshot` 使用 `GH_PAT`（或 `GITHUB_TOKEN`，不输出到日志）读取公共仓库。采集失败时不会写入部分结果。快照按 UTC 日期保存，每项使用稳定的 GitHub 仓库 ID；同日再次运行会替换当天快照。
- `python3 -m scripts.build_data` 将最新快照与编辑数据合并，并只将 `data/weekly/approved/` 中包含审核人和审核时间的期数写入站点数据。
- 每周需要约七日前（相差不超过 6 小时）的可比较快照。`python3 -m scripts.rank` 生成待审 JSON 草稿，包含最低涨星和活跃条件及风险提示；缺数据时不生成。不能把初期代理数据当七日涨星。
- 人工查看 `data/weekly/YYYY-Www.draft.json` 中的来源、数据和 `review_flags`，检查可能的声音/人物风险和异常增长，按想发布的顺序选择最多 10 个 ID：

```sh
python3 -m scripts.review 2026-W46 --reviewer '审核人' --ids 123,456
python3 -m scripts.build_data
cd site && npm run build
```

提交经过审核的 JSON 及站点数据后，网站周榜才展示该期。命令不会自动审核或对外发布；已审核期数不能通过该命令直接覆盖。

GitHub Actions 每日采集并在构建通过后提交数据，周一生成草稿；它不会代替人工审核，也没有配置线上部署。配置 `GH_PAT` secret 可提高 API 额度；未配置时使用仓库 `GITHUB_TOKEN`。仓库需要允许 Actions 写入内容。Actions 推送不会自动触发普通 push 工作流，因此采集工作流自身会先运行构建验证。定时任务可能延迟；以实际 `captured_at` 为准。首次推送后需检查 Actions 权限与实际运行结果。

## 主要限制

当前为人工筛选的固定种子池，不自动发现全部 GitHub 项目。真实周榜需等快照积累满 7 天并人工审核。没有配置在线托管、访客统计或自动告警 Issue；实际视频、显卡、许可证和链接仍需按项目逐一核查。首页背景由内置 imagegen 根据“黑白电影摄影棚、导演椅和摄影机、左侧留白”生成。
