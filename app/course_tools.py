# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _find_workspace_root() -> Path:
    env_root = os.environ.get("COURSE_WORKSPACE_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()

    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "notes" / "link-log.md").exists() and (
            parent / "capstone" / "spec.md"
        ).exists():
            return parent

    demo_workspace = PROJECT_ROOT / "demo_workspace"
    if demo_workspace.exists():
        return demo_workspace.resolve()

    return Path(__file__).resolve().parents[3]


WORKSPACE_ROOT = _find_workspace_root()

STATIC_ALLOWED_FILES = {
    "README.md",
    "docs/course-management.md",
    "docs/setup-checklist.md",
    "notes/course-log.md",
    "notes/link-log.md",
    "notes/official-email-summary.md",
    "work/day-04/README.md",
    "work/day-04/material-notes.md",
    "work/day-05/README.md",
    "work/day-05/material-notes.md",
    "work/day-05/production-checklist.md",
    "capstone/ideas.md",
    "capstone/spec.md",
    "capstone/submission-brief.md",
    "submissions/final-assignment-status.md",
}


def _is_secret_path(relative_path: str) -> bool:
    parts = Path(relative_path).parts
    return any(part in {".env", ".kaggle"} for part in parts) or relative_path.endswith(
        ".env"
    )


def _allowed_files() -> set[str]:
    allowed = set(STATIC_ALLOWED_FILES)
    work_dir = WORKSPACE_ROOT / "work"
    if work_dir.exists():
        allowed.update(
            path.relative_to(WORKSPACE_ROOT).as_posix()
            for path in work_dir.glob("day-*/material-notes.md")
        )
        allowed.update(
            path.relative_to(WORKSPACE_ROOT).as_posix()
            for path in work_dir.glob("day-*/README.md")
        )
    capstone_dir = WORKSPACE_ROOT / "capstone"
    if capstone_dir.exists():
        allowed.update(
            path.relative_to(WORKSPACE_ROOT).as_posix()
            for path in capstone_dir.glob("*.md")
        )
    submissions_dir = WORKSPACE_ROOT / "submissions"
    if submissions_dir.exists():
        allowed.update(
            path.relative_to(WORKSPACE_ROOT).as_posix()
            for path in submissions_dir.glob("*.md")
        )
    project_docs_dir = WORKSPACE_ROOT / "capstone" / "course-ops-agent" / "docs"
    if project_docs_dir.exists():
        allowed.update(
            path.relative_to(WORKSPACE_ROOT).as_posix()
            for path in project_docs_dir.glob("*.md")
        )
    return {path for path in allowed if not _is_secret_path(path)}


def list_allowed_course_files() -> dict[str, Any]:
    """List non-secret local files the agent is allowed to read."""
    return {
        "workspace_root": str(WORKSPACE_ROOT),
        "allowed_files": sorted(_allowed_files()),
        "secret_policy": "Secret files such as .env are never read or returned.",
    }


def _resolve_allowed_path(relative_path: str) -> Path:
    clean_path = Path(relative_path).as_posix().lstrip("/")
    if _is_secret_path(clean_path):
        raise ValueError("Secret paths such as .env are blocked.")
    if clean_path not in _allowed_files():
        raise ValueError(
            "Path is not in the course-agent allowlist. "
            f"Use list_allowed_course_files first. Requested: {clean_path}"
        )

    resolved = (WORKSPACE_ROOT / clean_path).resolve()
    try:
        resolved.relative_to(WORKSPACE_ROOT.resolve())
    except ValueError as exc:
        raise ValueError("Path traversal outside the workspace is blocked.") from exc
    return resolved


def read_course_file(relative_path: str, max_chars: int = 4000) -> dict[str, Any]:
    """Read a whitelisted, non-secret course workspace file.

    Args:
        relative_path: Workspace-relative path from list_allowed_course_files.
        max_chars: Maximum number of characters to return.

    Returns:
        File text, truncated if needed, plus source metadata.
    """
    try:
        path = _resolve_allowed_path(relative_path)
    except ValueError as exc:
        return {"ok": False, "error": str(exc)}

    text = path.read_text(encoding="utf-8")
    limit = max(500, min(max_chars, 12000))
    return {
        "ok": True,
        "source": path.relative_to(WORKSPACE_ROOT).as_posix(),
        "text": text[:limit],
        "truncated": len(text) > limit,
    }


def _parse_link_log_rows() -> list[dict[str, str]]:
    path = WORKSPACE_ROOT / "notes" / "link-log.md"
    if not path.exists():
        return []

    rows: list[dict[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| 20"):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != 5:
            continue
        date, day, link, link_type, notes = cells
        rows.append(
            {
                "date": date,
                "day": day,
                "link": link,
                "type": link_type,
                "notes": notes,
            }
        )
    return rows


def list_official_links(day: str = "") -> dict[str, Any]:
    """Return official course links recorded in notes/link-log.md.

    Args:
        day: Optional day filter, such as "Day 5", "5", or "Final".

    Returns:
        Matching links with their source type and notes.
    """
    normalized = day.strip().lower()
    rows = _parse_link_log_rows()
    if normalized:
        if normalized.isdigit():
            normalized = f"day {normalized}"
        rows = [
            row
            for row in rows
            if normalized in row["day"].lower()
            or normalized in row["notes"].lower()
            or normalized in row["type"].lower()
        ]
    return {
        "source": "notes/link-log.md",
        "query": day,
        "count": len(rows),
        "links": rows,
    }


def get_course_status(day: str = "Day 5") -> dict[str, Any]:
    """Get grounded status notes for a course day from local files.

    Args:
        day: Course day label, such as "Day 4" or "Day 5".

    Returns:
        Relevant local excerpts and official link rows.
    """
    normalized = day.strip().lower()
    if normalized.isdigit():
        normalized = f"day {normalized}"

    sources = [
        "notes/course-log.md",
        "submissions/final-assignment-status.md",
        "work/day-04/material-notes.md",
        "work/day-05/material-notes.md",
    ]
    excerpts: list[dict[str, str]] = []
    for source in sources:
        path = WORKSPACE_ROOT / source
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        matches = []
        for line in text.splitlines():
            lowered = line.lower()
            if normalized in lowered or "final assignment" in lowered:
                matches.append(line)
        if matches:
            excerpts.append({"source": source, "excerpt": "\n".join(matches[:12])})

    return {
        "day": day,
        "excerpts": excerpts,
        "links": list_official_links(day).get("links", []),
        "note": "Grounded only in local course notes and link log.",
    }


def search_course_notes(query: str, max_results: int = 8) -> dict[str, Any]:
    """Search whitelisted course notes for a user query.

    Args:
        query: Search text. Secret-file requests are refused.
        max_results: Maximum snippets to return.

    Returns:
        Matching snippets from whitelisted files.
    """
    if not query.strip():
        return {"ok": False, "error": "Query is empty."}
    if ".env" in query.lower() or "secret" in query.lower():
        return {
            "ok": False,
            "error": "Secret-related searches are blocked by policy.",
        }

    terms = [term for term in re.split(r"\W+", query.lower()) if len(term) >= 3]
    results: list[dict[str, str]] = []
    for relative_path in sorted(_allowed_files()):
        path = WORKSPACE_ROOT / relative_path
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        if not all(term in lowered for term in terms[:4]):
            continue
        for line in text.splitlines():
            line_lower = line.lower()
            if any(term in line_lower for term in terms):
                results.append({"source": relative_path, "snippet": line.strip()})
                break
        if len(results) >= max_results:
            break

    return {
        "ok": True,
        "query": query,
        "count": len(results),
        "results": results,
    }


def check_deployment_readiness() -> dict[str, Any]:
    """Check whether cloud deployment is allowed and locally ready.

    This function does not read secret values and never runs deployment commands.

    Returns:
        Readiness booleans and blockers.
    """
    gcloud_available = shutil.which("gcloud") is not None
    cloud_project_present = bool(os.environ.get("GOOGLE_CLOUD_PROJECT"))
    api_key_present = bool(os.environ.get("GOOGLE_API_KEY"))
    adc_present = bool(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

    blockers = []
    if not gcloud_available:
        blockers.append("gcloud is not installed or not on PATH.")
    if not cloud_project_present:
        blockers.append("GOOGLE_CLOUD_PROJECT is not set in the environment.")
    if not (api_key_present or adc_present):
        blockers.append("No API key or ADC credential presence is visible.")
    blockers.append("No explicit user approval for real cloud deployment is recorded.")
    blockers.append("No agents-cli deploy --dry-run review is recorded.")

    return {
        "ready": False,
        "checks": {
            "gcloud_available": gcloud_available,
            "google_cloud_project_present": cloud_project_present,
            "google_api_key_present": api_key_present,
            "google_application_credentials_present": adc_present,
            "explicit_deployment_approval_recorded": False,
            "dry_run_review_recorded": False,
        },
        "blockers": blockers,
        "policy": "Do not deploy until all blockers are cleared and the user explicitly approves.",
        "source": "work/day-05/production-checklist.md",
    }


def prepare_capstone_summary() -> dict[str, Any]:
    """Prepare a grounded capstone summary from local capstone notes."""
    brief = read_course_file("capstone/submission-brief.md", max_chars=5000)
    final_status = read_course_file("submissions/final-assignment-status.md")
    return {
        "project": "Course Materials Ops Agent",
        "brief": brief,
        "final_assignment_status": final_status,
        "deployment_claim": "No cloud deployment has been run or verified.",
    }
