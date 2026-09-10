# DentalOS — AI-Powered Dental Clinic SaaS
### Full Project Specification & Build Prompt

---

## 1. Product Overview

**Name:** DentalOS (working title — alt: DentaFlow, ClinicPilot, SmileStack)

**One-liner:** A multi-tenant SaaS platform that gives dental clinics an AI receptionist (powered by Gemini) that books appointments, answers patient questions, sends reminders, and manages recall campaigns — plus a full admin dashboard for staff.

**Target market:** Pakistan-first (WhatsApp-native, PKR billing, Urdu/English bilingual agent), architected to scale to global clinics (Stripe international, SMS/email channels, English-only mode).

**Core value proposition:**
- For clinics: fewer missed calls, fewer no-shows, automated recall = more recurring revenue, less front-desk overhead
- For patients: instant booking via chat instead of phone calls, 24/7 availability

---

## 2. Tech Stack

| Layer | Choice |
|---|---|
| Frontend | Next.js 15 (App Router), TypeScript, Tailwind CSS |
| Backend | Python FastAPI |
| Database | NeonDB (serverless Postgres) |
| Auth | Clerk (Organizations feature = clinic tenancy) |
| Payments | Stripe (subscription billing) |
| AI | Google Gemini (function calling / tool use) |
| Messaging | WhatsApp Business API (Meta Cloud API) + web chat widget |
| Hosting | Vercel (frontend) + Railway/Render or Fly.io (FastAPI backend) |
| Background jobs | FastAPI + APScheduler or a Postgres-based queue for reminders/recall |

---

## 3. Multi-Tenancy Model

- Clerk **Organizations** = clinics. Each staff user belongs to one clinic org.
- Every table scoped by `clinic_id` (Postgres row-level isolation, enforced at the query layer).
- Roles within a clinic: `owner` (dentist/admin), `receptionist`, `dentist` (view-only on non-clinical admin data).
- Subdomain or path-based routing per clinic for the public booking widget: `dentalos.app/c/{clinic-slug}`.

---

## 4. Database Schema (core tables)

```sql
clinics (
  id, name, slug, phone, address, timezone,
  whatsapp_number, branding_json, subscription_tier, created_at
)

staff_users (
  id, clerk_user_id, clinic_id, role, full_name, phone, created_at
)

patients (
  id, clinic_id, full_name, phone, email, dob,
  medical_notes, insurance_info, created_at
)

services (
  id, clinic_id, name, duration_minutes, price, category
)

dentists (
  id, clinic_id, staff_user_id, specialty, working_hours_json
)

appointments (
  id, clinic_id, patient_id, dentist_id, service_id,
  start_time, end_time, status, -- pending/confirmed/completed/cancelled/no_show
  booked_via, -- web/whatsapp/staff
  notes, created_at
)

conversations (
  id, clinic_id, patient_id, channel, -- whatsapp/web
  status, last_message_at, created_at
)

messages (
  id, conversation_id, role, -- user/agent/staff
  content, tool_calls_json, created_at
)

recall_campaigns (
  id, clinic_id, name, trigger_rule, -- e.g. "6 months since last cleaning"
  message_template, active
)

subscriptions (
  id, clinic_id, stripe_customer_id, stripe_subscription_id,
  plan, status, current_period_end
)
```

---

## 5. AI Agent Design (Gemini)

### Architecture pattern
Keep orchestration **inside FastAPI** — a simple loop, not a heavyweight framework:

```
Patient message → FastAPI receives (via WhatsApp webhook or web widget)
  → Load conversation context + clinic config
  → Call Gemini with system prompt + tool definitions
  → Gemini returns text OR a tool_call
  → If tool_call: FastAPI executes against real DB → sends result back to Gemini
  → Gemini produces final natural-language reply
  → Reply sent to patient (WhatsApp API / websocket to widget)
```

This avoids LangChain/CrewAI overhead for an MVP — you already have this instinct from your Vercel AI SDK agent template, and Gemini's native function calling is a direct fit for the same pattern.

### Agent system prompt (starting point)

```
You are the AI front-desk assistant for {clinic_name}, a dental clinic.

Your job:
- Help patients book, reschedule, or cancel appointments
- Answer questions about services, pricing, and hours using ONLY the
  clinic's provided data — never invent prices or availability
- Collect basic intake info (name, phone, reason for visit) before booking
- Escalate to a human staff member for: medical advice, emergencies,
  complaints, or anything outside scheduling/FAQ scope
- Be warm, concise, and professional. Respond in the language the
  patient uses (English or Urdu).

Never diagnose, recommend treatment, or discuss clinical judgment —
you handle scheduling and information only. For emergencies, immediately
provide the clinic's emergency contact and tell the patient to call directly.
```

### Tool definitions (function calling schema)

```json
[
  {
    "name": "check_availability",
    "description": "Get open appointment slots for a dentist/service in a date range",
    "parameters": {
      "dentist_id": "string, optional",
      "service_id": "string",
      "date_range_start": "string (ISO date)",
      "date_range_end": "string (ISO date)"
    }
  },
  {
    "name": "book_appointment",
    "description": "Create a confirmed appointment for a patient",
    "parameters": {
      "patient_phone": "string",
      "patient_name": "string",
      "service_id": "string",
      "dentist_id": "string",
      "start_time": "string (ISO datetime)"
    }
  },
  {
    "name": "reschedule_appointment",
    "description": "Move an existing appointment to a new time",
    "parameters": { "appointment_id": "string", "new_start_time": "string" }
  },
  {
    "name": "cancel_appointment",
    "description": "Cancel an existing appointment",
    "parameters": { "appointment_id": "string", "reason": "string, optional" }
  },
  {
    "name": "get_clinic_info",
    "description": "Fetch clinic hours, services, pricing, and location for FAQ answers",
    "parameters": {}
  },
  {
    "name": "escalate_to_staff",
    "description": "Flag conversation for human staff attention",
    "parameters": { "conversation_id": "string", "reason": "string" }
  }
]
```

### Recall Agent (separate, scheduled — not conversational)
A cron/background job runs daily: query patients whose last visit matches a clinic's `recall_campaigns` trigger rule → generate a personalized message via Gemini (using the template as grounding, not free generation) → send via WhatsApp → log to `conversations`.

---

## 6. MVP Build Phases

**Phase 1 — Foundation**
- Clerk org-based clinic onboarding + staff roles
- Clinic admin dashboard: services, dentists, working hours setup
- Manual appointment calendar (staff-created bookings)

**Phase 2 — AI Booking Agent**
- Web chat widget (embeddable) wired to Gemini + FastAPI tool-calling loop
- `check_availability` / `book_appointment` / `reschedule` / `cancel` tools live against real DB
- Conversation log visible in dashboard

**Phase 3 — WhatsApp Channel**
- Meta WhatsApp Business API webhook integration
- Same agent logic, different transport layer

**Phase 4 — Recall & Reminders**
- Scheduled reminder job (24hr-before appointment confirmations)
- Recall campaign engine (6-month checkup nudges, etc.)

**Phase 5 — Billing**
- Stripe subscription tiers (e.g. Solo / Multi-dentist / Multi-branch)
- Usage-based add-on: per-conversation AI cost pass-through if needed

---

## 7. Monetization (suggested tiers)

| Tier | Target | Price idea |
|---|---|---|
| Solo | 1 dentist, web widget only | Free or low PKR/month |
| Growth | Multi-dentist, WhatsApp included | Mid-tier monthly |
| Clinic Group | Multi-branch, recall campaigns, priority support | Higher monthly + per-branch add-on |

Pay-per-use fallback: charge per AI conversation beyond a free monthly quota (keeps Gemini API costs predictable for you).

---

## 8. Guardrails to build in from day one
- Agent never gives clinical/medical advice — hard-coded refusal + escalation path
- Agent never invents availability or pricing — every claim must come from a tool call result, not free generation
- All patient health data (`medical_notes`, `insurance_info`) encrypted at rest, access-scoped by role
- Clear emergency-escalation flow (agent detects urgency keywords → immediate human handoff + clinic emergency number)
