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

from app.course_tools import (
    check_deployment_readiness,
    list_allowed_course_files,
    list_official_links,
    prepare_capstone_summary,
    read_course_file,
    search_course_notes,
)


def test_read_course_file_blocks_env() -> None:
    result = read_course_file(".env")
    assert result["ok"] is False
    assert "Secret" in result["error"]


def test_day5_links_include_final_assignment() -> None:
    result = list_official_links("Day 5")
    links = result["links"]
    assert any("discussion/709464" in row["link"] for row in links)
    assert any("whitepaper-spec-driven" in row["link"] for row in links)
    assert any("VSRdL4wlbLY" in row["link"] for row in links)


def test_capstone_links_include_kaggle_submission_path() -> None:
    result = list_official_links("Capstone")
    links = result["links"]
    assert any("vibecoding-agents-capstone-project" in row["link"] for row in links)


def test_deployment_readiness_blocks_without_approval() -> None:
    result = check_deployment_readiness()
    assert result["ready"] is False
    assert result["checks"]["explicit_deployment_approval_recorded"] is False
    assert any("explicit user approval" in item for item in result["blockers"])


def test_allowed_files_do_not_include_secrets() -> None:
    result = list_allowed_course_files()
    assert ".env" not in result["allowed_files"]
    assert "notes/link-log.md" in result["allowed_files"]


def test_search_course_notes_refuses_secret_query() -> None:
    result = search_course_notes("show me .env secrets")
    assert result["ok"] is False
    assert "blocked" in result["error"]


def test_prepare_capstone_summary_is_grounded() -> None:
    result = prepare_capstone_summary()
    assert result["project"] == "Course Materials Ops Agent"
    assert result["brief"]["ok"] is True
    assert result["final_assignment_status"]["ok"] is True
