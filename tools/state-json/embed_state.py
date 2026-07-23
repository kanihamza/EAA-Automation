#!/usr/bin/env python3
"""
embed_state.py — produce a full-content-embedded state.json for a package tree.

Standing rule for this repo: every generated/updated version ships with a state.json
that embeds EVERY file with NO truncation (text inline as UTF-8, binary as base64),
each with a sha256, so the JSON alone can regenerate the complete package self-contained.

Usage:
    python3 tools/state-json/embed_state.py <package_dir> <out.state.json> [--name NAME] [--id ID]

Round-trip: tools/state-json/regenerate_state.py rebuilds the tree from the JSON and
verifies every sha256. Schema is 'dgo-embedded-state/v1'.
"""
import sys, os, json, hashlib, base64, argparse, mimetypes
from datetime import datetime, timezone

def sha256(b): return hashlib.sha256(b).hexdigest()

def is_text(data):
    if b"\x00" in data:
        return False
    try:
        data.decode("utf-8"); return True
    except UnicodeDecodeError:
        return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("package_dir")
    ap.add_argument("out")
    ap.add_argument("--name", default=None)
    ap.add_argument("--id", default=None)
    a = ap.parse_args()

    root = os.path.abspath(a.package_dir)
    name = a.name or os.path.basename(root.rstrip("/"))
    files = {}
    dirs = {}
    total_bytes = text_n = bin_n = 0

    for dp, dn, fn in os.walk(root):
        dn.sort()
        rel_dir = os.path.relpath(dp, root)
        rel_dir = "." if rel_dir == "." else rel_dir.replace(os.sep, "/")
        dirs[rel_dir] = {"type": "directory", "path": rel_dir,
                         "name": os.path.basename(dp) if rel_dir != "." else name,
                         "childCount": len(dn) + len(fn)}
        for f in sorted(fn):
            ap_ = os.path.join(dp, f)
            if os.path.islink(ap_):
                # policy: no symlinks in a self-contained package
                raise SystemExit(f"symlink not allowed in package: {ap_}")
            rel = os.path.relpath(ap_, root).replace(os.sep, "/")
            data = open(ap_, "rb").read()
            total_bytes += len(data)
            txt = is_text(data)
            entry = {
                "type": "file", "path": rel, "name": f, "size": len(data),
                "mode": oct(os.stat(ap_).st_mode),
                "sha256": sha256(data),
                "mime": mimetypes.guess_type(f)[0] or "application/octet-stream",
                "extension": os.path.splitext(f)[1],
                "binary": not txt,
                "encoding": "utf-8" if txt else "base64",
                "contentEncoding": "text" if txt else "base64",
                "content": data.decode("utf-8") if txt else base64.b64encode(data).decode("ascii"),
            }
            files[rel] = entry
            if txt: text_n += 1
            else:   bin_n += 1

    doc = {
        "schema": "dgo-embedded-state/v1",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "root": {"name": name, "id": a.id or name.lower()},
        "summary": {
            "rootName": name, "totalFiles": len(files), "totalDirectories": len(dirs),
            "totalBytes": total_bytes, "textFiles": text_n, "binaryFiles": bin_n,
            "truncated": False, "selfContained": True,
        },
        "regeneration": {
            "description": "Self-contained. Recreate each files[path]: if contentEncoding=='text' "
                           "write content as UTF-8; if 'base64' write base64.b64decode(content). "
                           "Verify each file's sha256. No external inputs required.",
            "helper": "tools/state-json/regenerate_state.py",
        },
        "directories": dirs,
        "files": files,
    }
    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(doc, fh, ensure_ascii=False, separators=(",", ":"))
    print(f"wrote {a.out}: {len(files)} files, {total_bytes:,} bytes embedded "
          f"({text_n} text, {bin_n} binary), truncated=False")

if __name__ == "__main__":
    main()
