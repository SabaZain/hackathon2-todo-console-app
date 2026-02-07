---
id: PHR-0001
title: Update Frontend to Connect to Vercel Backend
stage: green
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: /sp.implement
labels: ["frontend", "backend", "vercel", "api", "configuration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - fullstackwebapp/frontend/.env.local
 - fullstackwebapp/frontend/lib/api.ts
tests:
 - none
---

## Prompt

Update the frontend code in the project to connect to the live backend deployed on Vercel at "https://hackathon2-todo-console-app-lazz-v2.vercel.app".

- Find all API calls in the frontend that currently use relative paths like "/tasks" or "/todos".
- Replace them with the full URL using a constant, e.g., BACKEND_URL.
- Use BACKEND_URL in all fetch or axios calls.
- Make the changes in all frontend files where API calls are made.

## Response snapshot

Updated the frontend to connect to the Vercel backend by modifying the API_BASE_URL constant in lib/api.ts and the NEXT_PUBLIC_API_BASE_URL environment variable in .env.local to use the provided Vercel deployment URL.

## Outcome

- ✅ Impact: Frontend now connects to Vercel-deployed backend instead of local server
- 🧪 Tests: Built successfully with npm run build
- 📁 Files: Updated .env.local and lib/api.ts with new backend URL
- 🔁 Next prompts: None needed - configuration complete
- 🧠 Reflection: Proper constant-based architecture made the URL update straightforward

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh was not found, had to manually create PHR file
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Use agent-native file creation when shell scripts are unavailable