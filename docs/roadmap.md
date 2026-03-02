# Roadmap / 運用ルール（Series Repo）

## 目的
ACE-Step 1.5で生成した「架空ゲームサントラ風」シリーズを、ナンバリング `#NN` 単位で管理し、
GitHub Pages と YouTube へ公開する。

## 基本ルール
- 作品単位: `series/<SERIES_ID>/#NN_<slug>/`
- `liner.md`: 人間向けライナーノーツ（YouTube説明欄に転用可）
- `jobs.toml`: 生成の真実（再現性の根拠）
- 生成物:
  - `assets/mp3/` … mp3（Git LFS）
  - `assets/cover/` … ジャケット
  - `assets/video/` … YouTube用レンダ（任意）
- 公開ページ: `pages/index.md`（作品ページ本文）

## 命名
- Series ID: `CCAG` のような短いID
- ナンバリング: `#07` のように2桁固定推奨
- slug: `neon_exploit` のような lower_snake_case
- 作品フォルダ: `series/CCAG/#07_neon_exploit/`
- トラック名: `NN. Title` 形式を基本とする
- `jobs.toml` の `label`: `NN. Title NN-x-y` を必須にする

## 生成→公開（最短）
1. `jobs.toml` を作る（またはテンプレから複製）
2. `tools/acestep/queue.py` でキュー投入（ComfyUIへ）
3. 出力 mp3 を `assets/mp3/` へ配置
4. `tools/acestep/tag.py` で mp3 タグ付け
5. `pages/index.md` を更新（tracklist / credits / license）
6. `site/` を更新（一覧リンク）

## 問い合わせ方針（静けさ優先）
- 個別問い合わせ（商用可否の個別判断、例外許諾、個別サポート）は原則対応しない
- 判断基準は `docs/license_faq.md` と各ライセンス本文のみ
- FAQ外の用途は「利用しない」を推奨
