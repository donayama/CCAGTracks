"""
tag.py
ComfyUI AceStep 1.5 生成 MP3 へのID3タグ一括書き込みスクリプト

使い方 (repo root 基準):
    python tools/acestep/tag.py --jobs series/CCAG/#07_neon_exploit/jobs.toml --mp3dir series/CCAG/#07_neon_exploit/assets/mp3
    python tools/acestep/tag.py --jobs series/CCAG/#07_neon_exploit/jobs.toml --mp3dir series/CCAG/#07_neon_exploit/assets/mp3 --dry-run

必要ライブラリ: mutagen
    C:\\ComfyUIPortable\\python_embeded\\python.exe -m pip install mutagen

タグ埋め込み内容:
    TIT2  トラックタイトル   label から "NN. タイトル" 部分
    TALB  アルバムタイトル   TOMLヘッダー 1行目コメント
    TPE1  アーティスト       TOMLヘッダー 2行目コメント
    TPUB  レーベル           TOMLヘッダー 3行目コメント (レーベル部分)
    TDRC  年                 TOMLヘッダー 3行目コメント (年部分)
    TRCK  トラック番号       label先頭の "NN." から
    COMM  コメント           バリエーション番号 (xx-y) + tags全文
"""

import argparse
import re
import sys
import tomllib
from pathlib import Path


# ── ヘッダーコメント解析 ─────────────────────────────────────────────────────
def parse_toml_header(toml_path: Path) -> dict:
    """
    TOMLファイル冒頭の連続する # コメント行からアルバム情報を抽出する。
    1行目: アルバムタイトル
    2行目: "Composed by <アーティスト>" または単純な名前
    3行目: "<レーベル> / <年>" 形式
    """
    info = {"album": "", "artist": "", "label": "", "year": ""}
    comment_lines = []

    with toml_path.open(encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("#"):
                text = stripped.lstrip("#").strip()
                if text:  # 空コメント行はスキップ
                    comment_lines.append(text)
            elif stripped == "":
                # 空行はヘッダーブロック内なら継続
                if comment_lines:
                    continue
            else:
                break  # コメントブロック終了

    if len(comment_lines) >= 1:
        info["album"] = comment_lines[0]
    if len(comment_lines) >= 2:
        # "Composed by Xxx" → "Xxx" に正規化
        artist_raw = comment_lines[1]
        m = re.match(r"(?:Composed|Written|Music)\s+by\s+(.+)", artist_raw, re.IGNORECASE)
        info["artist"] = m.group(1).strip() if m else artist_raw
    if len(comment_lines) >= 3:
        # "Breach Point Studios / 2022" → label / year
        parts = comment_lines[2].split("/", 1)
        info["label"] = parts[0].strip()
        if len(parts) == 2:
            year_match = re.search(r"\d{4}", parts[1])
            info["year"] = year_match.group(0) if year_match else parts[1].strip()

    return info


# ── label 解析 ────────────────────────────────────────────────────────────────
_LABEL_RE = re.compile(
    r"^(\d+)\.\s+"          # (1) トラック番号  "01. "
    r"(.+?)\s+"             # (2) タイトル      "Zero Second: First Corridor "
    r"(\d+-\d+-\d+)\s*$"    # (3) バリアント    "01-0-0"
)

def parse_label(label: str) -> tuple[str, str, str]:
    """
    "01. Zero Second: First Corridor 01-0-0"
    → (track_num="01", title="Zero Second: First Corridor", variant="0-0")

    バリアントは先頭のトラック番号部分(01-)を除いた xx-y を返す。
    """
    m = _LABEL_RE.match(label.strip())
    if not m:
        raise ValueError(f"label のフォーマットが不正です: {label!r}\n"
                         f"期待形式: 'NN. タイトル NN-x-y'")
    track_num = m.group(1)          # "01"
    title     = m.group(2).strip()  # "Zero Second: First Corridor"
    variant_full = m.group(3)       # "01-0-0"

    # バリアント: トラック番号部分を除いた xx-y
    variant_parts = variant_full.split("-", 1)  # ["01", "0-0"]
    variant = variant_parts[1] if len(variant_parts) == 2 else variant_full  # "0-0"

    return track_num, title, variant


# ── MP3 タグ書き込み ──────────────────────────────────────────────────────────
def write_tags(mp3_path: Path, job: dict, album_info: dict,
               track_num: str, title: str, variant: str,
               total_tracks: int, dry_run: bool) -> None:
    from mutagen.id3 import (ID3, ID3NoHeaderError,
                              TIT2, TALB, TPE1, TPUB, TDRC, TRCK, COMM)

    try:
        tags = ID3(mp3_path)
    except ID3NoHeaderError:
        tags = ID3()

    tags["TIT2"] = TIT2(encoding=3, text=title)
    tags["TALB"] = TALB(encoding=3, text=album_info["album"])
    tags["TPE1"] = TPE1(encoding=3, text=album_info["artist"])
    tags["TPUB"] = TPUB(encoding=3, text=album_info["label"])
    tags["TDRC"] = TDRC(encoding=3, text=album_info["year"])
    tags["TRCK"] = TRCK(encoding=3, text=f"{int(track_num)}/{total_tracks}")

    # COMM: バリアント番号 + tags全文
    comm_text = f"variant: {variant}\n\n{job.get('tags', '').strip()}"
    tags["COMM::eng"] = COMM(encoding=3, lang="eng", desc="", text=comm_text)

    if not dry_run:
        tags.save(mp3_path)


# ── mp3 ファイルリスト取得（ナンバリング昇順） ──────────────────────────────
def collect_mp3s(mp3dir: Path) -> list[Path]:
    files = sorted(mp3dir.glob("*.mp3"), key=lambda p: p.name)
    return files


def infer_rename_prefix(jobs_path: Path) -> str:
    """
    jobs パスからデフォルト接頭辞を推定する。
    例: series/CCAG/#13_skydragon_scramble/jobs.toml -> CCAG#13
    """
    path_text = jobs_path.as_posix()
    m = re.search(r"/series/([^/]+)/#(\d+)_", f"/{path_text}")
    if m:
        return f"{m.group(1)}#{int(m.group(2)):02d}"
    return "track"


def read_trck_number(mp3_path: Path) -> int:
    """
    MP3 の TRCK からトラック番号を整数で返す。
    TRCK が '3/12' の場合は 3 を返す。
    """
    from mutagen.id3 import ID3

    tags = ID3(mp3_path)
    trck_frame = tags.get("TRCK")
    if trck_frame is None or not trck_frame.text:
        raise ValueError("TRCK タグが見つかりません")

    raw = str(trck_frame.text[0]).strip()
    if not raw:
        raise ValueError("TRCK タグが空です")
    head = raw.split("/", 1)[0].strip()
    if not head.isdigit():
        raise ValueError(f"TRCK が数値として解釈できません: {raw!r}")
    return int(head)


def read_variant_from_comm(mp3_path: Path) -> str | None:
    """
    MP3 の COMM から `variant: x-y` を読み取り、x-y を返す。
    見つからない・形式不正の場合は None を返す。
    """
    from mutagen.id3 import ID3

    tags = ID3(mp3_path)
    for key, frame in tags.items():
        if not key.startswith("COMM"):
            continue
        if not frame.text:
            continue
        text = str(frame.text[0]).strip()
        m = re.search(r"(?mi)^\s*variant\s*:\s*(\d+-\d+)\s*$", text)
        if m:
            return m.group(1)
    return None


def rename_mp3s_by_trck(mp3_paths: list[Path], prefix: str, dry_run: bool,
                        variants_by_path: dict[Path, str] | None = None) -> int:
    """
    TRCK タグに基づいて MP3 を改名する。
    variant(x-y) が取得できる場合は `PREFIX_trackNN_x-y.mp3` を優先する。
    同一候補名が重複する場合は `_v02` 形式のサフィックスを付与する。
    """
    collisions: dict[str, int] = {}
    renamed = 0

    for src in mp3_paths:
        try:
            track_no = read_trck_number(src)
        except Exception as e:
            print(f"[RENAME][SKIP] {src.name} -> TRCK 読み取り失敗: {e}")
            continue

        variant = ""
        if variants_by_path and src in variants_by_path:
            variant = variants_by_path[src].strip()
        if not variant:
            try:
                variant = read_variant_from_comm(src) or ""
            except Exception:
                variant = ""

        base = f"{prefix}_track{track_no:02d}"
        if variant and re.fullmatch(r"\d+-\d+", variant):
            base = f"{base}_{variant}"

        collisions[base] = collisions.get(base, 0) + 1
        seq = collisions[base]
        dst_name = f"{base}.mp3" if seq == 1 else f"{base}_v{seq:02d}.mp3"
        dst = src.with_name(dst_name)

        if src.name == dst.name:
            print(f"[RENAME][KEEP] {src.name}")
            continue
        if dst.exists():
            print(f"[RENAME][SKIP] {src.name} -> {dst.name} (既存ファイルあり)")
            continue

        if dry_run:
            print(f"[RENAME][DRY ] {src.name} -> {dst.name}")
        else:
            src.rename(dst)
            print(f"[RENAME][DONE] {src.name} -> {dst.name}")
        renamed += 1

    return renamed


# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="AceStep 生成 MP3 に jobs.toml の情報を ID3 タグとして書き込む"
    )
    parser.add_argument("--jobs",   required=True, help="ジョブリスト TOML のパス")
    parser.add_argument("--mp3dir", required=True, help="MP3 ファイルが格納されたフォルダ")
    parser.add_argument("--dry-run", action="store_true",
                        help="タグを実際には書き込まず確認のみ行う")
    parser.add_argument("--rename-by-trck", action="store_true",
                        help="TRCK タグに基づき MP3 を PREFIX_trackNN(_x-y).mp3 形式へ改名する")
    parser.add_argument("--rename-prefix", default="",
                        help="改名時の接頭辞（未指定時は jobs パスから自動推定）")
    parser.add_argument("--rename-only", action="store_true",
                        help="タグを書き換えず、既存 TRCK タグだけで改名する")
    args = parser.parse_args()

    jobs_path = Path(args.jobs)
    mp3dir    = Path(args.mp3dir)

    if not jobs_path.exists():
        sys.exit(f"[ERROR] ジョブファイルが見つかりません: {jobs_path}")
    if not mp3dir.is_dir():
        sys.exit(f"[ERROR] MP3 フォルダが見つかりません: {mp3dir}")

    # ── TOML 読み込み ──
    mp3_files = collect_mp3s(mp3dir)
    if args.rename_only:
        if not args.rename_by_trck:
            sys.exit("[ERROR] --rename-only を使う場合は --rename-by-trck も指定してください。")
        variants_for_renaming: dict[Path, str] = {}
        try:
            with jobs_path.open("rb") as f:
                toml_data = tomllib.load(f)
            jobs = toml_data.get("job", [])
            pair_count = min(len(jobs), len(mp3_files))
            for i in range(pair_count):
                label = jobs[i].get("label", "")
                try:
                    _, _, variant = parse_label(label)
                    variants_for_renaming[mp3_files[i]] = variant
                except Exception:
                    continue
        except Exception as e:
            print(f"[WARN] jobs.toml から枝番を読めなかったため COMM/TRCK ベースで改名します: {e}")

        prefix = args.rename_prefix.strip() or infer_rename_prefix(jobs_path)
        print(f"リネームのみ実行: prefix={prefix!r}  MP3数={len(mp3_files)}")
        if args.dry_run:
            print("※ DRY-RUN モード（ファイルは変更されません）")
        renamed_count = rename_mp3s_by_trck(mp3_files, prefix, args.dry_run, variants_for_renaming)
        rename_status = "確認完了" if args.dry_run else "改名完了"
        print(f"{rename_status}: {renamed_count} 件")
        return

    album_info = parse_toml_header(jobs_path)

    with jobs_path.open("rb") as f:
        toml_data = tomllib.load(f)

    jobs = toml_data.get("job", [])
    if not jobs:
        sys.exit("[ERROR] TOML に [[job]] エントリが見つかりません。")

    if len(mp3_files) < len(jobs):
        print(f"[WARN] MP3 ファイル数 ({len(mp3_files)}) が "
              f"ジョブ数 ({len(jobs)}) より少ないです。")
    if len(mp3_files) > len(jobs):
        print(f"[WARN] MP3 ファイル数 ({len(mp3_files)}) が "
              f"ジョブ数 ({len(jobs)}) より多いです。余分なファイルは無視されます。")

    # ── ユニークなトラック番号の総数を算出（TRCK の分母用） ──
    track_nums = set()
    for job in jobs:
        try:
            tn, _, _ = parse_label(job["label"])
            track_nums.add(int(tn))
        except (ValueError, KeyError):
            pass
    total_tracks = len(track_nums)

    # ── アルバム情報表示 ──
    print(f"アルバム : {album_info['album']}")
    print(f"アーティスト: {album_info['artist']}")
    print(f"レーベル : {album_info['label']}  年: {album_info['year']}")
    print(f"総トラック数: {total_tracks}  ジョブ数: {len(jobs)}  MP3数: {len(mp3_files)}")
    if args.dry_run:
        print("※ DRY-RUN モード（ファイルは変更されません）")
    print("─" * 70)

    # ── jobs順 × mp3ファイル順で1対1に割り当て ──
    pair_count = min(len(jobs), len(mp3_files))
    errors = 0
    variants_for_renaming: dict[Path, str] = {}

    for i in range(pair_count):
        job      = jobs[i]
        mp3_path = mp3_files[i]
        label    = job.get("label", "")

        try:
            track_num, title, variant = parse_label(label)
            variants_for_renaming[mp3_path] = variant
        except ValueError as e:
            print(f"[{i+1:>3}] [SKIP] {e}")
            errors += 1
            continue

        action = "DRY" if args.dry_run else "TAG"
        print(f"[{i+1:>3}] [{action}] {mp3_path.name}")
        print(f"       TIT2={title!r}  TRCK={int(track_num)}/{total_tracks}"
              f"  variant={variant!r}")

        try:
            write_tags(mp3_path, job, album_info,
                       track_num, title, variant,
                       total_tracks, args.dry_run)
        except Exception as e:
            print(f"       [ERROR] タグ書き込み失敗: {e}")
            errors += 1

    print("─" * 70)
    status = "確認完了" if args.dry_run else "書き込み完了"
    print(f"{status}: {pair_count} 件処理  エラー: {errors} 件")

    if args.rename_by_trck:
        prefix = args.rename_prefix.strip() or infer_rename_prefix(jobs_path)
        print("─" * 70)
        print(f"リネーム開始: prefix={prefix!r}")
        renamed_count = rename_mp3s_by_trck(mp3_files[:pair_count], prefix, args.dry_run, variants_for_renaming)
        rename_status = "確認完了" if args.dry_run else "改名完了"
        print(f"{rename_status}: {renamed_count} 件")


if __name__ == "__main__":
    main()
