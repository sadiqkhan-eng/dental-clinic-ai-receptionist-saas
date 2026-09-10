# OpenCode Skills Guide

Complete guide to creating and using Agent Skills in OpenCode.

---

## What are Skills?

Skills are reusable instruction files that agents can discover and load on-demand. They let you define custom behaviors, workflows, and domain-specific knowledge for your AI agents.

---

## 1. File Locations

OpenCode searches for skills in these locations:

| Location | Path |
|----------|------|
| Project (recommended) | `.opencode/skills/<name>/SKILL.md` |
| Global | `~/.config/opencode/skills/<name>/SKILL.md` |
| Claude-compatible (project) | `.claude/skills/<name>/SKILL.md` |
| Claude-compatible (global) | `~/.claude/skills/<name>/SKILL.md` |
| Agent-compatible (project) | `.agents/skills/<name>/SKILL.md` |
| Agent-compatible (global) | `~/.agents/skills/<name>/SKILL.md` |

---

## 2. Create Your First Skill

### Step 1: Create Directory

```bash
# Project-level skill
mkdir -p .opencode/skills/dental-booking

# Global skill (available everywhere)
mkdir -p ~/.config/opencode/skills/dental-booking
```

### Step 2: Create SKILL.md

Create `.opencode/skills/dental-booking/SKILL.md`:

```markdown
---
name: dental-booking
description: Handle dental appointment booking workflows
license: MIT
compatibility: opencode
metadata:
  audience: dental-clinic-staff
  workflow: appointments
---

## What I do

- Help patients book dental appointments
- Check dentist availability
- Send booking confirmations
- Handle rescheduling and cancellations

## When to use me

Use this skill when a patient wants to book, reschedule, or cancel a dental appointment.

## Booking workflow

1. Ask for patient name and phone number
2. Ask for preferred date and time
3. Check dentist availability using the booking API
4. Confirm the appointment details
5. Send confirmation via WhatsApp or SMS

## API endpoints

- `POST /api/appointments` - Create appointment
- `GET /api/appointments` - List appointments
- `PUT /api/appointments/{id}/status` - Update status

## Example conversation

Patient: "I want to book a cleaning appointment for tomorrow"
Agent: "I'd be happy to help! What time works best for you? We have slots at 10:00 AM, 2:00 PM, and 4:00 PM."
```

---

## 3. Skill File Rules

### Frontmatter (Required)

```yaml
---
name: my-skill              # Required: 1-64 chars, lowercase alphanumeric with hyphens
description: Do something   # Required: 1-1024 chars
license: MIT                # Optional
compatibility: opencode     # Optional
metadata:                   # Optional: string-to-string map
  audience: developers
  version: "1.0"
---
```

### Name Rules

- Must be 1-64 characters
- Lowercase alphanumeric with single hyphen separators
- Cannot start or end with `-`
- Cannot contain consecutive `--`
- Must match the directory name

Valid: `git-release`, `dental-booking`, `api-v2`
Invalid: `-git`, `git--release`, `Git-Release`

### Body Content

After the frontmatter, write your instructions in Markdown:

- Use headings to organize sections
- Include code examples when relevant
- Provide API references if applicable
- Add example conversations

---

## 4. Real-World Examples

### Example 1: Git Release Skill

`.opencode/skills/git-release/SKILL.md`:

```markdown
---
name: git-release
description: Create consistent releases and changelogs
license: MIT
compatibility: opencode
metadata:
  audience: maintainers
  workflow: github
---

## What I do

- Draft release notes from merged PRs
- Propose a version bump
- Provide a copy-pasteable `gh release create` command

## When to use me

Use this when you are preparing a tagged release.
Ask clarifying questions if the target versioning scheme is unclear.

## Steps

1. Run `git log --oneline` since last tag
2. Categorize commits (features, fixes, breaking)
3. Suggest version bump (patch/minor/major)
4. Generate changelog text
5. Provide `gh release create` command
```

### Example 2: Code Review Skill

`.opencode/skills/code-review/SKILL.md`:

```markdown
---
name: code-review
description: Perform thorough code reviews with security checks
metadata:
  audience: developers
  workflow: pull-requests
---

## What I do

- Review code for bugs, security issues, and style violations
- Suggest improvements and optimizations
- Check for proper error handling
- Verify test coverage

## When to use me

Use this when reviewing pull requests or checking code quality.

## Review checklist

1. **Security**: SQL injection, XSS, auth bypass
2. **Performance**: N+1 queries, unnecessary loops, memory leaks
3. **Error handling**: Try/catch blocks, meaningful error messages
4. **Testing**: Unit tests, integration tests, edge cases
5. **Documentation**: Comments, README updates, API docs

## Output format

Provide feedback in this format:
- Line number or file reference
- Issue description
- Suggested fix
- Severity (critical/warning/info)
```

### Example 3: DentalOS API Skill

`.opencode/skills/dentalos-api/SKILL.md`:

```markdown
---
name: dentalos-api
description: Build and maintain DentalOS FastAPI backend endpoints
metadata:
  audience: backend-developers
  framework: fastapi
---

## What I do

- Create new API endpoints following project conventions
- Use async SQLAlchemy with proper error handling
- Add Pydantic models for request/response validation
- Follow multi-tenant patterns with clinic_id scoping

## Project conventions

- All routers go in `backend/app/routers/`
- Use `APIRouter()` from FastAPI
- Always use `HTTPException` for errors, never return tuples
- Use Pydantic `BaseModel` for request bodies
- Use `Depends(get_db)` for database sessions

## Example endpoint

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Patient

router = APIRouter()

class PatientCreate(BaseModel):
    clinic_id: str
    full_name: str
    phone: str

@router.post("/")
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_db)):
    patient = Patient(clinic_id=data.clinic_id, full_name=data.full_name, phone=data.phone)
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return {"id": str(patient.id), "full_name": patient.full_name}
```

## Database models

- Use `UUID` primary keys with `default=uuid.uuid4`
- Scope all tables by `clinic_id` for multi-tenancy
- Use `relationship()` for foreign key relationships
```

---

## 5. Use Skills in Prompts

Once created, skills appear in the `skill` tool description. Agents can load them:

```
Load the dental-booking skill and help me book an appointment
```

Or explicitly:

```
use the dentalos-api skill to create a new endpoint for invoices
```

---

## 6. Skill Permissions

Control which skills agents can access in `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "pr-review": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

| Permission | Behavior |
|------------|----------|
| `allow` | Skill loads immediately |
| `deny` | Skill hidden from agent, access rejected |
| `ask` | User prompted for approval before loading |

---

## 7. Per-Agent Permissions

Give specific agents different permissions:

### Custom Agents (in SKILL.md frontmatter)

```yaml
---
name: my-skill
description: My skill
permission:
  skill:
    "documents-*": "allow"
---
```

### Built-in Agents (in opencode.json)

```json
{
  "agent": {
    "plan": {
      "permission": {
        "skill": {
          "internal-*": "allow"
        }
      }
    }
  }
}
```

---

## 8. Disable Skills

### For Specific Agents

```json
{
  "agent": {
    "plan": {
      "tools": {
        "skill": false
      }
    }
  }
}
```

### Globally

```json
{
  "tools": {
    "skill": false
  }
}
```

---

## 9. DentalOS Project Skills

Here are skills you can create for this project:

### `.opencode/skills/dentalos-backend/SKILL.md`

```markdown
---
name: dentalos-backend
description: Build FastAPI backend endpoints for DentalOS
metadata:
  framework: fastapi
  database: postgresql
---

## Backend conventions

- Python FastAPI with async/await
- SQLAlchemy async with asyncpg
- Pydantic models for validation
- UUID primary keys
- Multi-tenant via clinic_id
- Always use HTTPException for errors

## File structure

- `backend/app/routers/` - API endpoints
- `backend/app/services/` - Business logic
- `backend/app/models.py` - Database models
- `backend/app/config.py` - Settings
```

### `.opencode/skills/dentalos-frontend/SKILL.md`

```markdown
---
name: dentalos-frontend
description: Build Next.js frontend components for DentalOS
metadata:
  framework: next.js
  styling: tailwind
---

## Frontend conventions

- Next.js 15 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- Clerk for authentication
- API calls via `apiRequest()` from `lib/api.ts`

## File structure

- `frontend/src/app/` - Pages and layouts
- `frontend/src/components/` - Reusable components
- `frontend/src/lib/` - Utilities and API client
```

### `.opencode/skills/dentalos-deploy/SKILL.md`

```markdown
---
name: dentalos-deploy
description: Deploy DentalOS to production
metadata:
  hosting: vercel+railway
---

## Deployment steps

1. Frontend: `cd frontend && npm run build`
2. Backend: `cd backend && pip install -r requirements.txt`
3. Database: `cd backend && alembic upgrade head`

## Environment variables

Ensure all env vars are set in production:
- DATABASE_URL
- REDIS_URL
- GEMINI_API_KEY
- STRIPE_SECRET_KEY
- CLERK_SECRET_KEY
```

---

## 10. Troubleshooting

| Issue | Solution |
|-------|----------|
| Skill not showing | Verify `SKILL.md` is all caps, frontmatter has `name` and `description` |
| Name error | Check name matches directory, is lowercase with hyphens only |
| Permission denied | Check `permission.skill` in `opencode.json` |
| Skill not loading | Ensure name is unique across all locations |

---

## Quick Reference

```
.opencode/
  skills/
    my-skill/
      SKILL.md          # Skill definition with frontmatter

~/.config/opencode/
  skills/
    global-skill/
      SKILL.md          # Available in all projects
```

```bash
# Test skill loading
opencode
# Then in chat:
# use the my-skill tool
```
