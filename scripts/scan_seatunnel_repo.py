#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function

import argparse
import os
import sys
from pathlib import Path


KNOWN_MODULES = [
    ("seatunnel-api", "API"),
    ("seatunnel-core", "Core"),
    ("seatunnel-engine", "Zeta"),
    ("seatunnel-connectors-v2", "Connector-V2"),
    ("seatunnel-transforms-v2", "Transform-V2"),
    ("seatunnel-formats", "Format"),
    ("seatunnel-translation", "Translation"),
    ("seatunnel-e2e", "E2E"),
    ("docs", "Docs"),
    ("config", "Config"),
]


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def _detect_source_sink(connector_dir):
    java_root = connector_dir / "src" / "main" / "java"
    if not java_root.is_dir():
        return False, False, 0

    has_source = False
    has_sink = False
    option_hits = 0

    for java_file in java_root.rglob("*.java"):
        text = _read_text(java_file)
        if not has_source and "SeaTunnelSource" in text:
            has_source = True
        if not has_sink and "SeaTunnelSink" in text:
            has_sink = True
        option_hits += text.count("Option")
        if has_source and has_sink and option_hits >= 50:
            # Enough signal; stop early to keep scan fast on large connectors.
            break

    return has_source, has_sink, option_hits


def scan(repo):
    repo = Path(repo)
    result = {
        "repo": str(repo),
        "modules": [],
        "connectors": [],
    }

    for module_dir, module_name in KNOWN_MODULES:
        result["modules"].append(
            {
                "dir": module_dir,
                "name": module_name,
                "exists": (repo / module_dir).is_dir(),
            }
        )

    connectors_root = repo / "seatunnel-connectors-v2"
    if connectors_root.is_dir():
        for child in sorted(connectors_root.iterdir()):
            if not child.is_dir():
                continue
            if not (child.name.startswith("connector-") or child.name.startswith("seatunnel-connector-")):
                continue
            has_source, has_sink, option_hits = _detect_source_sink(child)
            result["connectors"].append(
                {
                    "name": child.name,
                    "path": str(child),
                    "has_source": has_source,
                    "has_sink": has_sink,
                    "option_hits": option_hits,
                }
            )

    return result


def render_markdown(result):
    lines = []
    lines.append("# SeaTunnel Repo Scan")
    lines.append("")
    lines.append("- repo: `%s`" % result["repo"])
    lines.append("")

    lines.append("## 1. Modules")
    lines.append("")
    for m in result["modules"]:
        lines.append("- %s (`%s`): %s" % (m["name"], m["dir"], "OK" if m["exists"] else "MISSING"))
    lines.append("")

    lines.append("## 2. Connector-V2 summary (heuristic)")
    lines.append("")
    if not result["connectors"]:
        lines.append("- no connector modules found under `seatunnel-connectors-v2/`")
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    lines.append("- total connector modules: `%d`" % len(result["connectors"]))
    lines.append("")
    lines.append("| connector module | source | sink | Option hits (rough) |")
    lines.append("|---|---:|---:|---:|")
    for c in result["connectors"]:
        lines.append(
            "| %s | %s | %s | %d |"
            % (
                c["name"],
                "Y" if c["has_source"] else "",
                "Y" if c["has_sink"] else "",
                int(c["option_hits"]),
            )
        )
    lines.append("")
    lines.append("> `Option hits` 仅为粗略信号（基于字符串计数），用于快速定位“配置密集型”connector。")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv):
    p = argparse.ArgumentParser(description="Scan a local apache/seatunnel repo for modules and connectors.")
    p.add_argument("--repo", required=True, help="Local path to apache/seatunnel repo")
    p.add_argument("--out", default="", help="Write markdown report to a file")
    return p.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print("[ERROR] repo not found: %s" % repo)
        return 2

    result = scan(repo)
    md = render_markdown(result)

    if args.out:
        out_path = os.path.abspath(args.out)
        out_dir = os.path.dirname(out_path)
        if out_dir and not os.path.isdir(out_dir):
            os.makedirs(out_dir)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md)
        print("[OK] wrote: %s" % out_path)
        return 0

    try:
        sys.stdout.write(md)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(md.encode("utf-8", errors="replace"))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
