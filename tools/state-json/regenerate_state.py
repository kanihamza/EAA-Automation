#!/usr/bin/env python3
"""
regenerate_state.py — rebuild a complete package from an embedded state.json,
verifying every file's sha256. Proves the JSON is self-contained.

Usage:
    python3 tools/state-json/regenerate_state.py <in.state.json> <out_dir> [--verify-only]
"""
import sys, os, json, hashlib, base64, argparse

def sha256(b): return hashlib.sha256(b).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("state_json")
    ap.add_argument("out_dir")
    ap.add_argument("--verify-only", action="store_true",
                    help="reconstruct in memory and check hashes without writing files")
    a = ap.parse_args()

    doc = json.load(open(a.state_json, encoding="utf-8"))
    files = doc["files"]
    ok = bad = 0
    bad_list = []
    for rel, e in files.items():
        if e.get("contentEncoding") == "base64" or e.get("binary"):
            data = base64.b64decode(e["content"])
        else:
            data = e["content"].encode("utf-8")
        if e.get("sha256") and sha256(data) != e["sha256"]:
            bad += 1; bad_list.append(rel); continue
        ok += 1
        if not a.verify_only:
            dst = os.path.join(a.out_dir, rel)
            os.makedirs(os.path.dirname(dst) or ".", exist_ok=True)
            open(dst, "wb").write(data)
    print(f"files={len(files)} sha256_ok={ok} sha256_bad={bad} "
          f"{'(verify-only)' if a.verify_only else 'written to '+a.out_dir}")
    if bad:
        print("MISMATCH:", *bad_list[:20], sep="\n  "); sys.exit(1)

if __name__ == "__main__":
    main()
