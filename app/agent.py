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

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

from app.course_tools import (
    check_deployment_readiness,
    get_course_status,
    list_allowed_course_files,
    list_official_links,
    prepare_capstone_summary,
    read_course_file,
    search_course_notes,
)

root_agent = Agent(
    name="course_ops_agent",
    model=Gemini(
        model="gemini-flash-latest",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=(
        "You are Course Materials Ops Agent, a local-first assistant for the "
        "Kaggle 5-Day AI Agents course workspace. Answer in the user's language. "
        "Ground every course-status, source, capstone, or deployment answer in "
        "tool output from the local workspace. Prefer official links already "
        "recorded in notes/link-log.md.\n\n"
        "Safety rules:\n"
        "- Never read, reveal, summarize, or search .env or other secret files.\n"
        "- Never claim cloud deployment, cleanup, CI/CD, billing, or publishing "
        "has happened unless local notes explicitly prove it.\n"
        "- If the user asks whether deployment can proceed, call "
        "check_deployment_readiness and explain blockers plainly.\n"
        "- If an official link is not confirmed in local notes, say it is "
        "pending confirmation rather than inventing URLs.\n"
        "- Keep answers concise, practical, and clear about completed vs pending "
        "human actions."
    ),
    tools=[
        list_allowed_course_files,
        read_course_file,
        list_official_links,
        get_course_status,
        search_course_notes,
        check_deployment_readiness,
        prepare_capstone_summary,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
