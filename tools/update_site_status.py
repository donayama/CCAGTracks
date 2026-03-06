#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
SERIES_DIR = ROOT / "series" / "CCAG"
SITE_INDEX = ROOT / "site" / "index.html"
SOURCE_DOC = ROOT / "docs" / "refs" / "LIMINAL_ATLAS_OST_Bible_v3.md"
RAW_BASE = "https://media.githubusercontent.com/media/donayama/CCAGTracks/main/"


def parse_titles(md_text: str) -> dict[int, tuple[str, str]]:
    lines = md_text.splitlines()
    out: dict[int, tuple[str, str]] = {}
    for i, line in enumerate(lines):
        m = re.match(r"^##\s+(\d{2})\.\s+(.+)$", line)
        if not m:
            continue
        num = int(m.group(1))
        if not (1 <= num <= 40):
            continue
        jp = m.group(2).strip()
        en = ""
        for j in range(i + 1, min(i + 8, len(lines))):
            m2 = re.match(r"^###\s+\*(.+)\*$", lines[j])
            if m2:
                en = m2.group(1).strip()
                break
        if en and num not in out:
            out[num] = (en, jp)
    return out


def find_album_dir(num: int) -> Path | None:
    prefix = f"#{num:02d}_"
    for p in SERIES_DIR.iterdir():
        if p.is_dir() and p.name.startswith(prefix):
            return p
    return None


def planned_tracks_from_jobs(jobs_path: Path) -> int:
    text = jobs_path.read_text(encoding="utf-8")
    nums = set(int(n) for n in re.findall(r"^#\s*(\d{2})\.", text, flags=re.MULTILINE))
    if nums:
        return len(nums)
    labels = set(int(n) for n in re.findall(r'^\s*label\s*=\s*"(\d{2})\.', text, flags=re.MULTILINE))
    return len(labels)


def first_cover_file(album_dir: Path) -> Path | None:
    cover_dir = album_dir / "assets" / "cover"
    if not cover_dir.exists():
        return None
    candidates = []
    for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
        candidates.extend(cover_dir.glob(ext))
    if not candidates:
        return None
    candidates.sort(key=lambda p: p.name.lower())
    return candidates[0]


def count_mp3(album_dir: Path) -> int:
    mp3_dir = album_dir / "assets" / "mp3"
    if not mp3_dir.exists():
        return 0
    return len(list(mp3_dir.glob("*.mp3")))


def cover_cell(cover: Path | None, num: int) -> str:
    if cover is None:
        return "—"
    rel = cover.relative_to(ROOT).as_posix()
    src = RAW_BASE + quote(rel, safe="/")
    return f'<img class="cover-thumb" src="{src}" alt="CCAG #{num:02d} cover">'


def album_cell(en_title: str, num: int, album_dir: Path | None) -> str:
    if album_dir is None:
        return html.escape(en_title)
    slug = album_dir.name.split("_", 1)[1] if "_" in album_dir.name else album_dir.name
    html_path = ROOT / "site" / "CCAG" / f"{num:02d}_{slug}.html"
    if html_path.exists():
        return f'<a href="CCAG/{num:02d}_{slug}.html">{html.escape(en_title)}</a>'
    return html.escape(en_title)


def status_and_notes(mp3_count: int, planned: int) -> tuple[str, str]:
    if mp3_count == 0:
        return '<span class="badge pending">現在制作中</span>', "未掲載"
    if planned > 0:
        if mp3_count < planned:
            return "公開中", f"{mp3_count}/{planned} tracks (未掲載あり)"
        return "公開中", f"{mp3_count}/{planned} tracks"
    return "公開中", f"{mp3_count} tracks"


def generate_rows(titles: dict[int, tuple[str, str]]) -> str:
    rows: list[str] = []
    for num in range(1, 41):
        en, jp = titles.get(num, (f"Title {num:02d}", f"未設定 {num:02d}"))
        album_dir = find_album_dir(num)
        mp3_count = count_mp3(album_dir) if album_dir else 0
        planned = 0
        if album_dir and (album_dir / "jobs.toml").exists():
            planned = planned_tracks_from_jobs(album_dir / "jobs.toml")
        if planned == 0 and mp3_count > 0:
            planned = mp3_count

        cover_html = cover_cell(first_cover_file(album_dir) if album_dir else None, num)
        album_html = album_cell(en, num, album_dir)
        status_html, notes = status_and_notes(mp3_count, planned)
        rows.append(
            f"        <tr><td>{num:02d}</td><td>{cover_html}</td><td>{album_html}</td>"
            f"<td>{html.escape(jp)}</td><td>{status_html}</td><td>{html.escape(notes)}</td></tr>"
        )
    return "      <tbody>\n" + "\n".join(rows) + "\n      </tbody>"


def main() -> None:
    titles = parse_titles(SOURCE_DOC.read_text(encoding="utf-8"))
    if len(titles) < 40:
        raise RuntimeError("Failed to parse 40 track titles from source doc.")

    html_text = SITE_INDEX.read_text(encoding="utf-8")
    tbody = generate_rows(titles)
    updated = re.sub(r"<tbody>[\s\S]*?</tbody>", tbody, html_text, count=1)
    if updated == html_text:
        raise RuntimeError("No <tbody> block replaced in site/index.html.")
    SITE_INDEX.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
