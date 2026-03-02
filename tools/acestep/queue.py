"""
queue.py
ComfyUI AceStep 1.5 バッチキュー投入スクリプト

使い方 (repo root 基準):
    python tools/acestep/queue.py --workflow tools/acestep/AceStep1.5API.json --jobs series/CCAG/#07_neon_exploit/jobs.toml
    python tools/acestep/queue.py --workflow tools/acestep/AceStep1.5API.json --jobs series/CCAG/#07_neon_exploit/jobs.toml --host http://127.0.0.1:8188

必要ライブラリ: tomllib (Python 3.11+ 標準), requests
    C:\ComfyUIPortable\python_embeded\python.exe -m pip install requests
"""

import argparse
import copy
import json
import sys
import tomllib
import urllib.error
import urllib.request
import uuid
from pathlib import Path

# ── keyscale バリデーション ──────────────────────────────────────────────────
_NOTES = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F",
          "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
_MODES = ["major", "minor"]

def validate_keyscale(value: str) -> str:
    """'E major' / 'C# minor' 形式を検証して正規化して返す。"""
    parts = value.strip().split()
    if len(parts) != 2:
        raise ValueError(f"keyscale は '<音名> <major|minor>' 形式で指定してください: {value!r}")
    note, mode = parts[0], parts[1].lower()
    if note not in _NOTES:
        raise ValueError(f"無効な音名 {note!r}。使用可能: {_NOTES}")
    if mode not in _MODES:
        raise ValueError(f"無効なモード {mode!r}。使用可能: {_MODES}")
    return f"{note} {mode}"


# ── ワークフロー書き換え ──────────────────────────────────────────────────────
def apply_job(workflow: dict, job: dict) -> dict:
    """
    ワークフローのディープコピーに job の値を適用して返す。

    job キー:
        bpm       : int   (必須)
        duration  : int   (必須) ← seconds / duration 両方に反映
        keyscale  : str   (必須)
        tags      : str   (必須、改行可)
    """
    wf = copy.deepcopy(workflow)

    bpm      = int(job["bpm"])
    duration = int(job["duration"])
    keyscale = validate_keyscale(job["keyscale"])
    tags     = str(job["tags"])

    # ── TextEncodeAceStepAudio1.5 (ノード 94) ──
    enc = wf["94"]["inputs"]
    enc["bpm"]      = bpm
    enc["duration"] = duration
    enc["keyscale"] = keyscale
    enc["tags"]     = tags

    # ── EmptyAceStep1.5LatentAudio (ノード 98) ──
    wf["98"]["inputs"]["seconds"] = duration

    return wf


# ── ComfyUI API 投入 ──────────────────────────────────────────────────────────
def queue_prompt(host: str, workflow: dict, client_id: str) -> str:
    """
    POST /prompt にワークフローを投入し、prompt_id を返す。
    標準ライブラリ urllib だけで実行できるが、requests があれば使う。
    """
    payload = json.dumps({
        "prompt": workflow,
        "client_id": client_id,
    }).encode("utf-8")

    url = f"{host.rstrip('/')}/prompt"

    try:
        import requests  # type: ignore
        resp = requests.post(url, data=payload,
                             headers={"Content-Type": "application/json"}, timeout=30)
        resp.raise_for_status()
        return resp.json()["prompt_id"]
    except ImportError:
        pass

    # fallback: urllib
    req = urllib.request.Request(
        url, data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            return json.loads(res.read())["prompt_id"]
    except urllib.error.URLError as e:
        raise RuntimeError(f"ComfyUI への接続に失敗しました ({url}): {e}") from e


# ── メイン ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="AceStep 1.5 ワークフローを TOML ジョブリストで ComfyUI にバッチ投入する"
    )
    parser.add_argument(
        "--workflow", required=True,
        help="ベースとなるワークフロー JSON のパス (例: AceStep1_5API.json)"
    )
    parser.add_argument(
        "--jobs", required=True,
        help="ジョブリスト TOML のパス (例: jobs.toml)"
    )
    parser.add_argument(
        "--host", default="http://127.0.0.1:8188",
        help="ComfyUI の URL (デフォルト: http://127.0.0.1:8188)"
    )
    args = parser.parse_args()

    # ── ファイル読み込み ──
    workflow_path = Path(args.workflow)
    jobs_path     = Path(args.jobs)

    if not workflow_path.exists():
        sys.exit(f"[ERROR] ワークフローファイルが見つかりません: {workflow_path}")
    if not jobs_path.exists():
        sys.exit(f"[ERROR] ジョブファイルが見つかりません: {jobs_path}")

    with workflow_path.open(encoding="utf-8") as f:
        base_workflow = json.load(f)

    with jobs_path.open("rb") as f:
        toml_data = tomllib.load(f)

    jobs = toml_data.get("job")
    if not jobs:
        sys.exit("[ERROR] TOML に [[job]] エントリが見つかりません。")
    if not isinstance(jobs, list):
        sys.exit("[ERROR] TOML の [job] はリスト ([[job]] ...) で記述してください。")

    client_id = str(uuid.uuid4())
    print(f"ComfyUI: {args.host}")
    print(f"ワークフロー: {workflow_path}")
    print(f"ジョブ数: {len(jobs)}")
    print(f"クライアントID: {client_id}")
    print("─" * 60)

    # ── 各ジョブをキューに投入 ──
    for i, job in enumerate(jobs, start=1):
        label = job.get("label", f"job-{i}")
        print(f"[{i}/{len(jobs)}] {label}  "
              f"bpm={job.get('bpm')}  duration={job.get('duration')}s  "
              f"keyscale={job.get('keyscale')!r}")
        try:
            wf = apply_job(base_workflow, job)
            prompt_id = queue_prompt(args.host, wf, client_id)
            print(f"         → キュー登録完了  prompt_id={prompt_id}")
        except (ValueError, KeyError) as e:
            print(f"         [SKIP] パラメータエラー: {e}")
        except RuntimeError as e:
            print(f"         [ERROR] {e}")
            sys.exit(1)

    print("─" * 60)
    print(f"全 {len(jobs)} 件をキューに投入しました。")


if __name__ == "__main__":
    main()
