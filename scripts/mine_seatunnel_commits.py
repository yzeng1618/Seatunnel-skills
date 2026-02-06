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
import collections
import datetime as _dt
import os
import re
import subprocess
import sys


COMMIT_SUBJECT_RE = re.compile(r"^\[(?P<type>[^\]]+)\]\[(?P<module>[^\]]+)\]\s+(?P<desc>.+)$")

PATH_MODULE_RULES = [
    ("Connector-V2", "seatunnel-connectors-v2/"),
    ("Zeta", "seatunnel-engine/"),
    ("Core", "seatunnel-core/"),
    ("API", "seatunnel-api/"),
    ("Transform-V2", "seatunnel-transforms-v2/"),
    ("Format", "seatunnel-formats/"),
    ("Translation", "seatunnel-translation/"),
    ("E2E", "seatunnel-e2e/"),
    ("Docs", "docs/"),
    ("Config", "config/"),
]


def _run_git(repo, args):
    cmd = ["git", "-C", repo] + args
    return subprocess.check_output(cmd).decode("utf-8", errors="replace")


def _since_date(args):
    if args.since:
        return args.since
    if args.months <= 0:
        raise ValueError("--months must be > 0 if --since is not set")
    days = int(args.months) * 30
    dt = _dt.datetime.utcnow() - _dt.timedelta(days=days)
    return dt.strftime("%Y-%m-%d")


def _infer_module_from_paths(paths):
    for module, prefix in PATH_MODULE_RULES:
        for p in paths:
            if p.startswith(prefix):
                return module
    return "Other"


def _path_prefix(path, depth):
    parts = [p for p in path.split("/") if p]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return "/".join(parts[:depth]) + "/"


def _categorize_dimension(subject, paths):
    s = subject.lower()
    dims = set()
    if "fix" in s or "bug" in s:
        dims.add("Bugfix")
    if "option" in s or "config" in s or "parameter" in s or "param" in s:
        dims.add("Options")
    if "connector" in s or "source" in s or "sink" in s:
        dims.add("Connector")
    for p in paths:
        lp = p.lower()
        if "/source/" in lp:
            dims.add("Source")
        if "/sink/" in lp:
            dims.add("Sink")
    if not dims:
        dims.add("Other")
    return sorted(dims)


def mine(repo, since, paths=None, max_commits=0):
    args = [
        "log",
        "--since=%s" % since,
        "--name-only",
        "--date=short",
        "--pretty=format:%H\t%ad\t%s",
    ]
    if max_commits and int(max_commits) > 0:
        args.insert(1, "-n")
        args.insert(2, str(int(max_commits)))
    if paths:
        args.append("--")
        args.extend(paths)

    raw = _run_git(repo, args)

    commits = []
    current = None
    for line in raw.splitlines():
        if not line.strip():
            continue
        if "\t" in line and re.match(r"^[0-9a-f]{7,40}\t", line):
            if current:
                commits.append(current)
            parts = line.split("\t", 2)
            commit_hash = parts[0]
            commit_date = parts[1] if len(parts) > 1 else ""
            subject = parts[2] if len(parts) > 2 else ""
            current = {
                "hash": commit_hash,
                "date": commit_date,
                "subject": subject,
                "paths": [],
            }
        else:
            if current is None:
                continue
            current["paths"].append(line.strip())
    if current:
        commits.append(current)

    stats = {
        "total_commits": len(commits),
        "since": since,
        "paths_filter": list(paths or []),
        "type_counts": collections.Counter(),
        "module_counts_msg": collections.Counter(),
        "module_counts_path": collections.Counter(),
        "dimension_counts": collections.Counter(),
        "top_paths": collections.Counter(),
        "samples_by_dimension": collections.defaultdict(list),
        "recent_commits": [],
    }

    for c in commits:
        subject = c["subject"]
        paths = c["paths"]
        for p in paths:
            pref = _path_prefix(p, depth=2)
            if pref:
                stats["top_paths"][pref] += 1

        msg_type = "Other"
        msg_module = "Other"
        m = COMMIT_SUBJECT_RE.match(subject)
        if m:
            msg_type = m.group("type").strip()
            msg_module = m.group("module").strip()
        stats["type_counts"][msg_type] += 1
        stats["module_counts_msg"][msg_module] += 1

        modules_touched = set()
        for module, prefix in PATH_MODULE_RULES:
            for p in paths:
                if p.startswith(prefix):
                    modules_touched.add(module)
                    break
        if not modules_touched:
            modules_touched.add("Other")
        for mod in sorted(modules_touched):
            stats["module_counts_path"][mod] += 1

        dims = _categorize_dimension(subject, paths)
        for d in dims:
            stats["dimension_counts"][d] += 1
            if len(stats["samples_by_dimension"][d]) < 10:
                stats["samples_by_dimension"][d].append((c["hash"], subject))

        if len(stats["recent_commits"]) < 50:
            stats["recent_commits"].append((c.get("date", ""), c["hash"], subject))

    return stats


def _render_markdown(stats):
    def _top(counter, n=15):
        return counter.most_common(n)

    lines = []
    lines.append("# SeaTunnel Commit Insights")
    lines.append("")
    lines.append("- since: `%s`" % stats["since"])
    lines.append("- total commits: `%d`" % stats["total_commits"])
    if stats.get("paths_filter"):
        lines.append("- paths filter: `%s`" % ", ".join(stats["paths_filter"]))
    lines.append("")

    lines.append("## 1. Types (from commit subject)")
    lines.append("")
    for k, v in _top(stats["type_counts"], 20):
        lines.append("- %s: %d" % (k, v))
    lines.append("")

    lines.append("## 2. Modules (from commit subject)")
    lines.append("")
    for k, v in _top(stats["module_counts_msg"], 20):
        lines.append("- %s: %d" % (k, v))
    lines.append("")

    lines.append("## 3. Modules (from touched paths)")
    lines.append("")
    for k, v in _top(stats["module_counts_path"], 20):
        lines.append("- %s: %d" % (k, v))
    lines.append("")

    lines.append("## 4. Dimensions (heuristic)")
    lines.append("")
    for k, v in _top(stats["dimension_counts"], 20):
        lines.append("- %s: %d" % (k, v))
    lines.append("")

    lines.append("## 5. Top touched path prefixes (depth=2)")
    lines.append("")
    for k, v in _top(stats["top_paths"], 30):
        lines.append("- %s: %d" % (k, v))
    lines.append("")

    lines.append("## 6. Sample commits by dimension")
    lines.append("")
    for dim, samples in sorted(stats["samples_by_dimension"].items()):
        lines.append("### %s" % dim)
        lines.append("")
        for h, s in samples:
            lines.append("- `%s` %s" % (h[:10], s))
        lines.append("")

    lines.append("## 7. Recent commits (up to 50)")
    lines.append("")
    for d, h, s in stats.get("recent_commits", []):
        lines.append("- `%s` `%s` %s" % (d, h[:10], s))
    lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv):
    p = argparse.ArgumentParser(description="Mine Apache SeaTunnel commit history for insights.")
    p.add_argument("--repo", required=True, help="Local path to apache/seatunnel repo")
    p.add_argument("--since", default="", help="Since date (YYYY-MM-DD)")
    p.add_argument("--months", type=int, default=24, help="Months back if --since is not set (default: 24)")
    p.add_argument(
        "--path",
        action="append",
        default=[],
        help="Limit git log to a path (can be repeated), e.g. --path seatunnel-connectors-v2",
    )
    p.add_argument(
        "--max-commits",
        type=int,
        default=0,
        help="Limit commits processed (0 means no limit).",
    )
    p.add_argument("--out", default="", help="Write markdown report to a file")
    return p.parse_args(argv)


def main(argv):
    args = parse_args(argv)
    repo = os.path.abspath(args.repo)
    if not os.path.isdir(repo):
        print("[ERROR] repo not found: %s" % repo)
        return 2

    since = _since_date(args)
    stats = mine(repo, since, paths=args.path, max_commits=args.max_commits)
    md = _render_markdown(stats)

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
