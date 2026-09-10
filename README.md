# DentalOS

> AI-Powered Dental Clinic SaaS Platform

A multi-tenant SaaS platform that gives dental clinics an AI receptionist powered by Google Gemini that books appointments, answers patient questions, sends reminders, and manages recall campaigns.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/next.js-15-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Database Schema](#database-schema)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [AI Agent Design](#ai-agent-design)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

DentalOS solves three core problems for dental clinics:

1. **Missed calls** - AI receptionist handles patient inquiries 24/7 via WhatsApp and web chat
2. **No-shows** - Automated reminders and recall campaigns keep patients engaged
3. **Front-desk overhead** - Automated booking, rescheduling, and cancellation reduces staff workload

### Target Market

- **Pakistan-first** - WhatsApp-native, PKR billing, Urdu/English bilingual
- **Global-ready** - Stripe international, SMS/email channels, English-only mode

### Core Value Proposition

| For Clinics | For Patients |
|-------------|--------------|
| Fewer missed calls | Instant booking via chat |
| Fewer no-shows | 24/7 availability |
| Automated recall campaigns | No phone calls needed |
| More recurring revenue | Quick responses |
| Less front-desk overhead | Multi-language support |

---

## Key Features

### AI Receptionist (Gemini)
- Natural language conversation via WhatsApp and web chat
- Book, reschedule, or cancel appointments
- Answer questions about services, pricing, and hours
- Collect patient intake information
- Escalate to human staff for medical advice or emergencies
- Sentiment analysis on patient messages
- Multi-turn conversation context

### Appointment Management
- Real-time availability checking
- Conflict detection and prevention
- Calendar view with daily/weekly/monthly layouts
- Staff schedule management
- Waiting list for cancelled slots
- Automated 24-hour reminders via SMS/WhatsApp

### Patient Portal
- Self-service appointment booking
- View appointment history
- Update personal information
- Receive automated reminders

### Analytics & Insights
- Revenue tracking and trends
- Appointment statistics by service
- No-show rate analysis
- Peak hours identification
- Patient retention metrics

### Billing & Payments
- Stripe subscription billing (Solo/Growth/Clinic Group tiers)
- Invoice generation with PDF export
- Usage-based AI conversation pricing
- JazzCash/EasyPaisa integration (Pakistan)

### Recall & Reminders
- Automated recall campaigns (e.g., 6-month checkup nudges)
- Personalized messaging via Gemini
- Multi-channel delivery (WhatsApp, SMS, Email)
- Campaign performance tracking

### Multi-Tenancy
- Clinic isolation via `clinic_id` scoping
- Role-based access (Owner, Receptionist, Dentist)
- Custom branding per clinic
- White-label custom domains

### Integrations
- **WhatsApp Business API** - Patient communication
- **Twilio** - SMS reminders
- **SendGrid** - Email notifications
- **Daily.co** - Telemedicine video calls
- **Google Calendar** - Bidirectional sync
- **Stripe** - Subscription payments
- **Google Gemini** - AI agent

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 15 (App Router) | Web dashboard and patient portal |
| **Styling** | Tailwind CSS | UI components and responsive design |
| **Auth** | Clerk | Multi-tenant authentication |
| **Backend** | Python FastAPI | REST API and AI agent |
| **Database** | NeonDB (PostgreSQL) | Persistent data storage |
| **Cache** | Redis (Upstash) | Session caching, rate limiting |
| **AI** | Google Gemini | Conversational AI agent |
| **Payments** | Stripe | Subscription billing |
| **Messaging** | WhatsApp Business API | Patient communication |
| **SMS** | Twilio | Appointment reminders |
| **Email** | SendGrid | Email notifications |
| **Video** | Daily.co | Telemedicine consultations |
| **Hosting** | Vercel (FE) + Railway (BE) | Production deployment |
| **Mobile** | React Native (Expo) | Staff mobile app (optional) |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        PATIENTS                             │
│  WhatsApp Chat │ Web Chat Widget │ Patient Portal │ Mobile  │
└────────┬───────────────┬──────────────┬─────────────┬───────┘
         │               │              │             │
         ▼               ▼              ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                     NGINX / LOAD BALANCER                    │
└────────────────────────────┬────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   NEXT.JS FE    │ │   FASTAPI BE    │ │   WEBHOOKS      │
│   (Vercel)      │ │   (Railway)     │ │   (WhatsApp)    │
│                 │ │                 │ │                 │
│  - Dashboard    │ │  - REST API     │ │  - Meta Cloud   │
│  - Chat Widget  │ │  - AI Agent     │ │  - Stripe       │
│  - Patient UI   │ │  - Reminders    │ │  - Twilio       │
└─────────────────┘ └────────┬────────┘ └─────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   NEONDB        │ │   REDIS         │ │   EXTERNAL      │
│   (PostgreSQL)  │ │   (Upstash)     │ │   SERVICES      │
│                 │ │                 │ │                 │
│  - Clinics      │ │  - Cache        │ │  - Gemini AI    │
│  - Patients     │ │  - Rate Limit   │ │  - Stripe       │
│  - Appointments │ │  - Sessions     │ │  - Twilio       │
│  - Messages     │ │                 │ │  - SendGrid     │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

### Request Flow

```
Patient Message (WhatsApp/Web)
    │
    ▼
Webhook/API Endpoint
    │
    ▼
Load Conversation Context + Clinic Config
    │
    ▼
Call Gemini with System Prompt + Tool Definitions
    │
    ├──► Gemini returns text ──► Send to patient
    │
    └──► Gemini returns tool_call
            │
            ▼
        Execute tool against DB
            │
            ▼
        Send result back to Gemini
            │
            ▼
        Gemini produces natural-language reply
            │
            ▼
        Send to patient (WhatsApp/Web)
```

---

## Database Schema

### Core Tables

```sql
-- Clinic (multi-tenant root)
clinics (id, name, slug, phone, address, timezone, whatsapp_number, branding_json, subscription_tier)

-- Staff management
staff_users (id, clerk_user_id, clinic_id, role, full_name, phone)

-- Patient records
patients (id, clinic_id, full_name, phone, email, dob, medical_notes, insurance_info)

-- Services offered
services (id, clinic_id, name, duration_minutes, price, category)

-- Dentist profiles
dentists (id, clinic_id, staff_user_id, specialty, working_hours_json)

-- Appointments
appointments (id, clinic_id, patient_id, dentist_id, service_id, start_time, end_time, status, booked_via)

-- AI conversations
conversations (id, clinic_id, patient_id, channel, status, sentiment_score)
messages (id, conversation_id, role, content, tool_calls_json)

-- Billing
invoices (id, clinic_id, patient_id, appointment_id, amount, currency, status, payment_method)
subscriptions (id, clinic_id, stripe_customer_id, stripe_subscription_id, plan, status)

-- Engagement
recall_campaigns (id, clinic_id, name, trigger_rule, message_template, active)
waiting_list (id, clinic_id, patient_id, service_id, preferred_date, status)
referrals (id, clinic_id, referrer_patient_id, referred_patient_id, referral_code, reward_applied)

-- Operations
audit_logs (id, clinic_id, user_id, action, resource_type, resource_id, details)
```

### Entity Relationship

```
clinics ──┬── staff_users
          ├── patients ──────┬── appointments
          ├── services ──────┤
          ├── dentists ──────┘
          ├── conversations ──── messages
          ├── invoices
          ├── subscriptions
          ├── recall_campaigns
          ├── waiting_list
          ├── referrals
          └── audit_logs
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL (NeonDB)
- Redis (Upstash)
- Google Gemini API key
- Stripe account
- Clerk account
- WhatsApp Business account

### 1. Clone Repository

```bash
git clone https://github.com/yourusername/dentalos.git
cd dentalos
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run database migrations
alembic upgrade head

# Start development server
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your keys

# Start development server
npm run dev
```

### 4. Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### 5. Docker Setup (Optional)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

---

## Project Structure

```
dentalos/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── routers/           # API endpoints (14 routers)
│   │   │   ├── clinics.py     # Clinic CRUD
│   │   │   ├── patients.py    # Patient management
│   │   │   ├── services.py    # Service offerings
│   │   │   ├── dentists.py    # Dentist profiles
│   │   │   ├── appointments.py # Booking system
│   │   │   ├── conversations.py # AI chat logs
│   │   │   ├── staff.py       # Staff management
│   │   │   ├── chat.py        # AI chat endpoint
│   │   │   ├── webhooks.py    # WhatsApp webhook
│   │   │   ├── billing.py     # Stripe integration
│   │   │   ├── analytics.py   # Revenue & stats
│   │   │   ├── invoices.py    # Invoice management
│   │   │   ├── waiting_list.py # Waitlist feature
│   │   │   ├── referrals.py   # Referral program
│   │   │   ├── telemedicine.py # Video calls
│   │   │   ├── training.py    # AI training mode
│   │   │   ├── packages.py    # Bundle pricing
│   │   │   ├── insurance.py   # Insurance verification
│   │   │   ├── whitelabel.py  # Custom domains
│   │   │   ├── api_access.py  # Third-party API
│   │   │   ├── marketplace.py # Clinic directory
│   │   │   ├── multilang.py   # Urdu/English
│   │   │   └── whatsapp_catalog.py
│   │   ├── services/          # Business logic
│   │   │   ├── gemini_agent.py # AI agent
│   │   │   ├── chat_service.py # Conversation handler
│   │   │   ├── sentiment_service.py # Sentiment analysis
│   │   │   ├── reminder_service.py # SMS/Email
│   │   │   ├── audit_service.py # Audit logging
│   │   │   ├── rate_limiter.py # Rate limiting
│   │   │   ├── cache.py       # Redis caching
│   │   │   ├── websocket_manager.py # Real-time
│   │   │   ├── calendar_sync.py # Google Calendar
│   │   │   └── training_service.py # AI training
│   │   ├── models.py          # 14 database models
│   │   ├── database.py        # Async SQLAlchemy
│   │   └── config.py          # Pydantic settings
│   ├── migrations/            # Alembic migrations
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/                   # Next.js 15 frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── dashboard/     # Admin dashboard (11 pages)
│   │   │   │   ├── page.tsx   # Stats overview
│   │   │   │   ├── appointments/
│   │   │   │   ├── calendar/
│   │   │   │   ├── patients/
│   │   │   │   ├── services/
│   │   │   │   ├── staff-schedule/
│   │   │   │   ├── conversations/
│   │   │   │   ├── analytics/
│   │   │   │   ├── broadcast/
│   │   │   │   ├── training/
│   │   │   │   └── settings/
│   │   │   ├── c/[slug]/      # Public booking widget
│   │   │   ├── patient/       # Patient portal
│   │   │   ├── sign-in/       # Clerk auth
│   │   │   └── sign-up/
│   │   ├── components/
│   │   │   ├── dashboard-sidebar.tsx
│   │   │   ├── chat-widget.tsx
│   │   │   └── voice-input.tsx
│   │   ├── lib/
│   │   │   ├── api.ts         # API client
│   │   │   └── utils.ts       # Utilities
│   │   └── middleware.ts      # Clerk auth middleware
│   ├── package.json
│   ├── Dockerfile
│   └── .env
│
├── docker-compose.yml
├── .env.example
├── .gitignore
├── opencode_mcp_setup.md      # MCP server guide
├── opencode_skills.md         # Skills guide
├── opencode_agents.md         # Agents guide
└── dentalos-project-prompt.md # Original spec
```

---

## API Documentation

### Base URLs

| Environment | URL |
|-------------|-----|
| Development | `http://localhost:8000` |
| Production | `https://api.dentalos.app` |

### Endpoints

#### Clinics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/clinics/` | List all clinics |
| GET | `/api/clinics/{id}` | Get clinic details |
| POST | `/api/clinics/` | Create clinic |

#### Patients
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/patients/?clinic_id={id}` | List patients |
| GET | `/api/patients/{id}` | Get patient |
| POST | `/api/patients/` | Create patient |

#### Appointments
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/appointments/?clinic_id={id}` | List appointments |
| GET | `/api/appointments/{id}` | Get appointment |
| POST | `/api/appointments/` | Create appointment |
| PUT | `/api/appointments/{id}/status` | Update status |

#### Services
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/services/?clinic_id={id}` | List services |
| POST | `/api/services/` | Create service |

#### AI Chat
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat` | Send message to AI |

#### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/analytics/summary` | Dashboard stats |
| GET | `/api/analytics/revenue` | Revenue chart |
| GET | `/api/analytics/appointments-by-service` | Service stats |
| GET | `/api/analytics/no-show-rate` | No-show analysis |

#### Billing
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/billing/checkout` | Create Stripe checkout |
| POST | `/webhooks/stripe` | Stripe webhook |

---

## AI Agent Design

### System Prompt

```
You are the AI front-desk assistant for {clinic_name}, a dental clinic.

Your job:
- Help patients book, reschedule, or cancel appointments
- Answer questions about services, pricing, and hours
- Collect basic intake info (name, phone, reason for visit)
- Escalate to human staff for medical advice or emergencies
- Be warm, concise, and professional
- Respond in the language the patient uses (English or Urdu)

Never diagnose, recommend treatment, or discuss clinical judgment.
```

### Tool Definitions

| Tool | Description |
|------|-------------|
| `check_availability` | Get open appointment slots |
| `book_appointment` | Create a confirmed appointment |
| `reschedule_appointment` | Move appointment to new time |
| `cancel_appointment` | Cancel an existing appointment |
| `get_clinic_info` | Fetch hours, services, pricing |
| `escalate_to_staff` | Flag for human attention |

### Guardrails

1. **No medical advice** - Hard-coded refusal + escalation
2. **No invented data** - Every claim from tool results, not free generation
3. **Data encryption** - PHI encrypted at rest
4. **Emergency detection** - Urgency keywords trigger immediate handoff

---

## Deployment

### Frontend (Vercel)

```bash
cd frontend
vercel --prod
```

### Backend (Railway)

```bash
cd backend
railway up
```

### Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `REDIS_URL` | Redis connection string |
| `GEMINI_API_KEY` | Google Gemini API key |
| `STRIPE_SECRET_KEY` | Stripe secret key |
| `CLERK_SECRET_KEY` | Clerk auth secret |
| `WHATSAPP_ACCESS_TOKEN` | WhatsApp API token |
| `TWILIO_ACCOUNT_SID` | Twilio account SID |
| `SENDGRID_API_KEY` | SendGrid API key |

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

- **Documentation:** https://dentalos.app/docs
- **Issues:** https://github.com/yourusername/dentalos/issues
- **Email:** support@dentalos.app

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Next.js](https://nextjs.org/) - React framework
- [Google Gemini](https://ai.google.dev/) - AI model
- [Clerk](https://clerk.com/) - Authentication
- [Stripe](https://stripe.com/) - Payments
- [NeonDB](https://neon.tech/) - Serverless PostgreSQL
