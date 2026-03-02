# ACE-Step 1.5 Workflow

## Inputs
- `series/<SERIES_ID>/#NN_<slug>/jobs.toml`
- `tools/acestep/AceStep1.5API.json` (ComfyUI workflow)

## Steps
1. **Plan**
   - `liner.md` を書く（世界観/狙い/参考ワード）
   - `jobs.toml` を作る（テンプレ推奨）
2. **Queue**
   - `python tools/acestep/queue.py --jobs series/CCAG/#07_neon_exploit/jobs.toml --workflow tools/acestep/AceStep1.5API.json`
3. **Generate**
   - ComfyUIで実行し、mp3を出力
4. **Store**
   - 出力 mp3 を `assets/mp3/` に配置
5. **Tag**
   - `python tools/acestep/tag.py --jobs series/CCAG/#07_neon_exploit/jobs.toml --mp3dir series/CCAG/#07_neon_exploit/assets/mp3`
6. **Publish**
   - `pages/index.md` と `site/*` のリンクを更新
   - GitHub Pages を更新

## One-line Flow
`jobs.toml -> queue.py -> ComfyUI -> mp3 -> tag.py -> assets配置 -> Pages更新`
