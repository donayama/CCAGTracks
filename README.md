# ACE-Step Series Repository

ACE-Step 1.5 で生成する「架空ゲームサントラ風」シリーズを、`#NN` 単位で再現可能に管理するリポジトリ。

## 何がどこにあるか
- `docs/`: 運用ルール、ワークフロー、ライセンスFAQ、参考資料
- `tools/acestep/`: ComfyUI APIワークフローとキュー投入/タグ付けスクリプト
- `prompts/`: プロンプト生成プロンプトと各種テンプレート
- `series/`: 作品本体（`jobs.toml`、`liner.md`、`assets/`、`pages/`）
- `site/`: GitHub Pages で公開する最小サイト

## 最短の生成手順
1. 作品フォルダを作る:
   - `series/CCAG/#NN_slug/liner.md`
   - `series/CCAG/#NN_slug/jobs.toml`
2. キュー投入:
   - `python tools/acestep/queue.py --jobs series/CCAG/#NN_slug/jobs.toml --workflow tools/acestep/AceStep1.5API.json`
3. ComfyUI 実行後、mp3 を `series/CCAG/#NN_slug/assets/mp3/` に配置
4. タグ付け:
   - `python tools/acestep/tag.py --jobs series/CCAG/#NN_slug/jobs.toml --mp3dir series/CCAG/#NN_slug/assets/mp3`
5. `series/.../pages/index.md` と `site/` の導線ページを更新

詳細は `docs/workflow_acestep15.md` を参照。

## ライセンス（静けさ優先）
- 音源・ライナーノーツ・ページ本文: **CC BY-NC 4.0**
- ツール/スクリプト/プロンプト生成プロンプト: **Apache-2.0**
- 個別の利用相談には原則対応しません。FAQの範囲で判断してください。

参照:
- `docs/license_faq.md`
- `LICENSES/LICENSE-MUSIC-CC-BY-NC-4.0.txt`
- `LICENSES/LICENSE-CODE-Apache-2.0.txt`

## Git LFS
大きな生成物は Git LFS 前提。
- `git lfs install`
- `.gitattributes` で `*.mp3 *.wav *.flac *.png *.mp4` などを追跡

## GitHub Pages（`/site` 公開）
このリポジトリは GitHub Actions で `site/` を Pages にデプロイする想定。

1. Repository Settings → Pages → Source を `GitHub Actions` に設定
2. main へ push
3. `.github/workflows/pages.yml` が `site/` をそのまま公開
