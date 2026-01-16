---
id: PHR-0002
title: Add CORS Configuration for Frontend
stage: green
date: 2026-01-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: unknown
command: /sp.implement
labels: ["backend", "cors", "fastapi", "frontend", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - fullstackwebapp/backend/main.py
tests:
 - none
---

## Prompt

Update my backend FastAPI project to allow CORS requests so that my frontend can communicate with it.

Details:
1. Backend is in the `backend` folder.
2. Frontend local URL: http://localhost:3000
3. Frontend live URL: https://hackathon2-todo-console-app-lazz-ktm0vzi0p-saba-zains-projects.vercel.app
4. Add the FastAPI CORS middleware to allow these origins.
5. Ensure that all methods and headers are allowed and credentials are supported.
6. Keep the existing backend routes and logic intact.
7. The main file where the app is created is `backend/main.py`.

## Response snapshot

Updated the CORS configuration in the backend by adding the Vercel deployment URL to the allowed origins list while preserving all existing configuration including credentials support and wildcard methods/headers.

## Outcome

- ✅ Impact: Backend now allows CORS requests from both localhost and Vercel deployment
- 🧪 Tests: Syntax validation passed successfully
- 📁 Files: Updated main.py with additional CORS origin
- 🔁 Next prompts: None needed - CORS configuration complete
- 🧠 Reflection: Backend already had excellent CORS setup, just needed to add the production URL

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): none
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none needed