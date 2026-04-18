# Sentinel
### AI-Powered Network Security Audit SaaS for Indian SMEs

> Automatically scan a business network and generate a professional security audit report
> in under 10 minutes — the kind consultants charge ₹50,000–₹2,00,000 for.

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-009688)
![React](https://img.shields.io/badge/React-frontend-61DAFB)
![Status](https://img.shields.io/badge/status-building-orange)

---

## What Is Sentinel?

Sentinel is a SaaS product that:

1. Runs a lightweight Python agent on a customer's local network
2. Captures live traffic, extracts flow features, detects threats using ML
3. Scores risk per device and maps threats to MITRE ATT&CK
4. Generates a professional PDF security audit report automatically
5. Emails the report to the customer — monthly, on autopilot

**Target customer:** Indian SMEs with 20–200 employees — pharma, manufacturing,
clinics, logistics, CA firms — who have no dedicated security team and cannot
afford enterprise tools like Darktrace or Fortinet.

**Price:**
- ₹9,999 — one-time report
- ₹14,999/month — monthly automated reports
- ₹1,29,999/year — annual plan (28% saving)

---

## Product Vision

```
Customer installs Sentinel agent (one command)
          ↓
Agent scans network silently for 30 minutes
          ↓
Raw data sent to Sentinel cloud API
          ↓
AI engine detects threats, scores risk, maps MITRE
          ↓
PDF report generated automatically
          ↓
Report emailed to customer + available in dashboard
          ↓
Repeat every 30 days automatically
```

---

## Full Tech Stack

### Backend
| Tool | Version | Purpose |
|---|---|---|
| Python | 3.11+ | Core language |
| FastAPI | 0.115+ | REST API framework |
| Uvicorn | 0.30+ | ASGI server |
| SQLAlchemy | 2.0+ | ORM / database queries |
| SQLite | — | Database (Phase 1) |
| PostgreSQL | 15+ | Database (Phase 3+) |
| Celery | 5.4+ | Background task queue |
| Redis | 7+ | Celery broker + cache |
| WeasyPrint | 62+ | HTML → PDF generation |
| Jinja2 | 3.1+ | PDF report templates |
| Pydantic | 2.7+ | Data validation |
| Python-Jose | 3.3+ | JWT authentication |
| Passlib | 1.7+ | Password hashing |
| Razorpay | 1.4+ | Indian payments |
| Resend | 0.7+ | Transactional email |
| Python-dotenv | 1.0+ | Environment variables |
| Pytest | 8.2+ | Testing |
| Httpx | 0.27+ | Async HTTP client |

### Network Detection Engine (Agent)
| Tool | Version | Purpose |
|---|---|---|
| Scapy | 2.5+ | Packet capture |
| Pandas | 2.2+ | Flow data processing |
| NumPy | 1.26+ | Numerical operations |
| Scikit-learn | 1.5+ | Isolation Forest anomaly detection |
| PyYAML | 6.0+ | Config management |
| Psutil | 5.9+ | System health metrics |

### Frontend
| Tool | Version | Purpose |
|---|---|---|
| React | 18.3+ | UI framework |
| Vite | 5.2+ | Build tool / dev server |
| Tailwind CSS | 3.4+ | Utility-first styling |
| shadcn/ui | latest | Pre-built components |
| React Router | 6.23+ | Client-side routing |
| TanStack Query | 5.40+ | Server state + data fetching |
| Axios | 1.7+ | HTTP requests |
| Recharts | 2.12+ | Charts and visualisations |
| Lucide React | 0.383+ | Icons |

### Infrastructure & DevOps
| Tool | Purpose |
|---|---|
| Docker + Docker Compose | Containerisation |
| GitHub Actions | CI/CD pipeline |
| Railway | Backend hosting (start free) |
| Vercel | Frontend hosting (free) |
| Supabase | Auth + managed Postgres (Phase 3) |
| Cloudflare | DNS + domain |

### Dev Tools (Vibe Coding Setup)
| Tool | Purpose |
|---|---|
| Cursor | AI-powered code editor — primary IDE |
| Claude | Code generation, architecture help |
| Postman | API endpoint testing |
| TablePlus | Database GUI |
| ESLint + Prettier | Code formatting |

---

## Repository Structure

```
sentinel/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── reports.py             # Report CRUD + download
│   │   │   ├── scans.py               # Scan upload + processing
│   │   │   ├── payments.py            # Razorpay integration
│   │   │   ├── auth.py                # Login, register, JWT
│   │   │   └── customers.py           # Customer management
│   │   ├── core/
│   │   │   ├── config.py              # Settings via pydantic-settings
│   │   │   ├── database.py            # SQLAlchemy engine + session
│   │   │   ├── security.py            # JWT helpers, password hashing
│   │   │   └── deps.py                # FastAPI dependencies
│   │   ├── models/
│   │   │   ├── customer.py            # Customer table
│   │   │   ├── report.py              # Report table
│   │   │   └── scan.py                # Scan job table
│   │   ├── schemas/
│   │   │   ├── customer.py            # Pydantic request/response schemas
│   │   │   ├── report.py
│   │   │   └── scan.py
│   │   ├── services/
│   │   │   ├── report_generator.py    # Core: scan data → PDF bytes
│   │   │   ├── email_service.py       # Send report PDF via email
│   │   │   └── scan_processor.py      # Validate + parse uploaded data
│   │   └── templates/
│   │       ├── report.html            # Jinja2 PDF report template
│   │       └── report.css             # PDF styling
│   │
│   ├── detection/                     # Network detection engine
│   │   ├── __init__.py
│   │   ├── sniffer.py                 # Packet capture (Scapy)
│   │   ├── flow_table.py              # Flow tracking + timeout
│   │   ├── feature_extractor.py       # 24 statistical features per flow
│   │   ├── anomaly_engine.py          # Z-score + Isolation Forest
│   │   ├── behavioral_fingerprint.py  # Per-device baseline + drift
│   │   ├── risk_engine.py             # Unified risk scoring
│   │   ├── mitre_mapper.py            # Map threats to ATT&CK
│   │   └── alert_logger.py            # Write alerts.json
│   │
│   ├── agent/
│   │   ├── sentinel_agent.py          # Agent customers install + run
│   │   └── agent_config.yaml          # Agent config (API key, endpoint)
│   │
│   ├── tasks/
│   │   └── celery_tasks.py            # Background: generate report async
│   │
│   ├── tests/
│   │   ├── test_detection.py
│   │   ├── test_reports.py
│   │   └── fixtures/
│   │       ├── sample_alerts.json
│   │       ├── sample_device_profiles.json
│   │       └── sample_risk_timeline.json
│   │
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── celeryconfig.py
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing.jsx            # Marketing homepage
│   │   │   ├── Login.jsx              # Auth page
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx          # Customer home
│   │   │   ├── Reports.jsx            # Report history list
│   │   │   ├── ReportDetail.jsx       # Single report view
│   │   │   └── Payment.jsx            # Checkout + Razorpay
│   │   ├── components/
│   │   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── ReportCard.jsx         # Report preview card
│   │   │   ├── RiskScoreCircle.jsx    # Animated risk score
│   │   │   ├── ThreatTable.jsx        # Threats with MITRE tags
│   │   │   ├── DeviceRiskBar.jsx      # Device risk progress bar
│   │   │   └── Navbar.jsx
│   │   ├── hooks/
│   │   │   ├── useAuth.js
│   │   │   └── useReports.js
│   │   ├── lib/
│   │   │   ├── api.js                 # Axios instance + interceptors
│   │   │   └── utils.js
│   │   └── App.jsx
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.js
│
├── docker-compose.yml
├── .github/
│   └── workflows/
│       └── ci.yml
└── README.md
```

---

## Roadmap — Build Order

> Rule: finish each phase completely before starting the next.
> Each phase = one focused build session.

---

### Phase 0 — Validate First (Week 1, No Code)

**Goal: Prove a real person will pay before writing a single line.**

This is the most important phase. Do not skip it.

- [ ] Write a sample audit report manually in Google Docs
  - Pretend you scanned a company network
  - Include: risk score, 5 fake threats, device list, recommendations
  - Make it look professional — this is your sales tool
- [ ] Post on LinkedIn: "I'm building a tool that auto-generates network
      security audit reports for SMEs. Looking for 3 businesses in
      Hyderabad to get a free report. Comment or DM me."
- [ ] Send direct messages to 20 people:
  - Search: "IT Manager Hyderabad", "CTO Hyderabad", "Operations Head"
  - Target: pharma, manufacturing, clinics, CA firms, logistics
  - Message template (see Customer Acquisition section below)
- [ ] Get 1 person to agree to a free trial
- [ ] Visit them, interview them for 20 minutes:
  - "How do you currently handle network security?"
  - "Have you ever had a security audit done? What did it cost?"
  - "Would you pay ₹9,999/month for this report automatically?"
- [ ] Show them the Google Docs sample report
- [ ] Note their exact reaction and words

**Exit criteria:** At least 1 person says "yes I'd pay for this" OR
you learn something specific that changes the product direction.

---

### Phase 1 — Detection Engine (Weekend 1, ~8 hours)

**Goal: Python script that captures network traffic and outputs
structured threat data as JSON files.**

This is the core of the whole product. Everything else depends on this.

#### Step 1 — Project setup (30 min)
```bash
mkdir sentinel && cd sentinel
python -m venv .venv
source .venv/bin/activate
pip install scapy pandas numpy scikit-learn pyyaml psutil
mkdir -p detection tests/fixtures
```

#### Step 2 — Packet capture + flow table (2 hours)

Build `detection/sniffer.py`:
- Capture packets using Scapy `sniff()`
- Group packets into flows (src IP + dst IP + port + protocol)
- Expire flows after 30 seconds of inactivity
- Output: list of flow dicts

Build `detection/flow_table.py`:
- `FlowTable` class — stores active flows in memory
- `add_packet(packet)` — adds packet to matching flow
- `get_expired_flows()` — returns flows idle > 30s
- Flow keys: `(src_ip, dst_ip, dst_port, protocol)`

#### Step 3 — Feature extraction (1 hour)

Build `detection/feature_extractor.py`:
- Takes a completed flow, returns 24 features:
  - `packet_count`, `byte_count`, `duration_seconds`
  - `avg_packet_size`, `std_packet_size`
  - `packets_per_second`, `bytes_per_second`
  - `src_port`, `dst_port`, `protocol`
  - `syn_count`, `ack_count`, `fin_count`
  - `unique_dst_ports` (from same src in last 60s)
  - `dns_query_count` (per device per minute)
  - `is_internal_src`, `is_internal_dst`
  - `hour_of_day`, `day_of_week`
  - `tcp_flag_ratio`, `payload_ratio`

#### Step 4 — Anomaly detection (2 hours)

Build `detection/anomaly_engine.py`:
- `AnomalyEngine` class
- Warmup: collect 50 flows to build baseline
- Z-score detection: flag features > 3 standard deviations from mean
- Isolation Forest: fit on baseline, score new flows
- Returns: `(is_anomalous: bool, anomaly_score: float, reason: str)`

Build `detection/behavioral_fingerprint.py`:
- `BehavioralFingerprint` class — one profile per device IP
- Track per-device rolling averages: ports used, IPs talked to,
  traffic volume, active hours
- `check_drift(ip, current_features)` — compare to baseline
- Returns: `(has_drift: bool, drift_reason: str, deviation_pct: float)`

#### Step 5 — Risk scoring (1 hour)

Build `detection/risk_engine.py`:
- `RiskEngine` class
- Inputs: anomaly score + drift detection + threat indicators
- Formula: `risk_score = (anomaly_weight * 0.4) + (drift_weight * 0.3)
  + (threat_indicators * 0.3)`
- Severity levels:
  - Critical: score >= 75
  - High: score >= 50
  - Medium: score >= 25
  - Low: score < 25
- Returns: `(risk_score: int, severity: str)`

#### Step 6 — MITRE mapping (30 min)

Build `detection/mitre_mapper.py`:
- Dictionary mapping threat patterns to MITRE ATT&CK:
  - Port scanning → T1046 Network Service Discovery
  - DNS anomaly → T1071 Application Layer Protocol
  - Unusual outbound → T1041 Exfiltration Over C2 Channel
  - Rogue device → T1200 Hardware Additions
  - Brute force → T1110 Brute Force
  - Data staging → T1074 Data Staged
- `map_threat(threat_type)` → returns tactic + technique_id + technique_name

#### Step 7 — Alert logger (30 min)

Build `detection/alert_logger.py`:
- Writes HIGH+ severity alerts to `alerts.json`
- Writes device profiles to `device_profiles.json`
- Writes risk timeline to `risk_timeline.json`
- Appends — does not overwrite

#### Step 8 — Wire it all together (1 hour)

Build `detection/engine.py`:
- `SentinelEngine` class — orchestrates all modules
- `process_flow(flow)` → runs all detectors → returns alert or None
- Build `run_detection.py` — main script:
  ```bash
  sudo python run_detection.py --duration 30 --interface eth0
  ```
  Runs for 30 minutes, outputs 3 JSON files

**Test it:** Run on your home network. Check the JSON files.
Verify alerts are being generated. Fix anything broken.

**Vibe coding prompt for Phase 1:**
> "Build a Python network detection engine with these modules:
> sniffer.py using Scapy to capture packets and group into flows,
> feature_extractor.py to extract 24 statistical features per flow,
> anomaly_engine.py using Z-score + Isolation Forest to detect anomalies,
> behavioral_fingerprint.py to track per-device baselines and detect drift,
> risk_engine.py to calculate a 0-100 risk score, mitre_mapper.py to map
> threat types to MITRE ATT&CK technique IDs, and alert_logger.py to write
> alerts.json and device_profiles.json. Wire everything together in engine.py."

---

### Phase 2 — PDF Report Generator (Weekend 2, ~6 hours)

**Goal: Python function that takes the 3 JSON files and outputs
a professional PDF report.**

#### Step 1 — Install dependencies
```bash
pip install weasyprint jinja2
```

#### Step 2 — Build report template

Create `backend/app/templates/report.html`:
- Full HTML page styled for PDF output
- Five sections (see Report Template Spec below)
- Professional design: navy header, clear typography, risk colour coding
- Inline CSS only (WeasyPrint does not support external stylesheets well)

#### Step 3 — Build report generator

Create `backend/app/services/report_generator.py`:

```python
def generate_pdf_report(
    company_name: str,
    alerts: list,
    device_profiles: dict,
    risk_timeline: list
) -> bytes:
    # 1. Calculate overall risk score (average of top device scores)
    # 2. Count critical/high/medium alerts
    # 3. Get top 5 threats sorted by risk score
    # 4. Get top 10 devices sorted by risk score
    # 5. Generate plain-English recommendations
    # 6. Render Jinja2 template with all data
    # 7. Convert HTML to PDF using WeasyPrint
    # 8. Return PDF as bytes
```

#### Step 4 — Build standalone test script

Create `generate_report.py` in project root:
```bash
python generate_report.py \
  --company "Test Company Pvt Ltd" \
  --alerts tests/fixtures/sample_alerts.json \
  --devices tests/fixtures/sample_device_profiles.json \
  --output report_output.pdf
```

Run it. Open the PDF. Read it as a non-technical business owner.
Ask: "Does this make sense? Is it clear? Would I pay for this?"
Iterate until the answer is yes.

**Vibe coding prompt for Phase 2:**
> "Write a Python function generate_pdf_report() that takes company_name,
> alerts list, device_profiles dict, and risk_timeline list as inputs.
> Use Jinja2 to render an HTML template and WeasyPrint to convert to PDF.
> The report must have: a header with company name + overall risk score circle
> coloured red/amber/green, an overview grid with 4 stat boxes, a top threats
> table with severity pills and MITRE ATT&CK IDs, a device risk leaderboard
> with coloured progress bars, and numbered plain-English recommended actions
> with estimated fix times. Return the PDF as bytes."

---

### Phase 3 — Backend API (Weekend 3, ~8 hours)

**Goal: FastAPI server that accepts scan data, generates reports,
handles payments, and serves PDFs.**

#### Step 1 — Project setup
```bash
cd backend
pip install fastapi uvicorn sqlalchemy python-jose passlib razorpay
          resend celery redis python-multipart python-dotenv
```

#### Step 2 — Database models

`app/models/customer.py`:
- id, email, hashed_password, company_name, phone
- created_at, subscription_plan, is_active

`app/models/report.py`:
- id, customer_id (FK), created_at, status
- company_name, overall_risk_score, pdf_path
- critical_count, high_count, medium_count, device_count

`app/models/scan.py`:
- id, customer_id (FK), created_at, status
- alerts_path, devices_path, timeline_path
- report_id (FK, nullable until generated)

#### Step 3 — Core API endpoints

`POST /api/auth/register` — create customer account
`POST /api/auth/login` — returns JWT token
`GET  /api/auth/me` — current user info

`POST /api/scans/upload` — upload 3 JSON files, returns scan_id
`GET  /api/scans/{id}/status` — check processing status

`GET  /api/reports` — list customer's reports
`GET  /api/reports/{id}` — report metadata
`GET  /api/reports/{id}/download` — returns PDF file

`POST /api/payments/create-order` — creates Razorpay order (₹9999)
`POST /api/payments/verify` — verifies signature, unlocks report
`POST /api/payments/webhook` — Razorpay webhook handler

#### Step 4 — Background task

`tasks/celery_tasks.py`:
```python
@celery.task
def generate_report_task(scan_id: int):
    # Load scan JSON files from disk
    # Run report_generator.generate_pdf_report()
    # Save PDF to disk
    # Update report record in DB (status = ready)
    # Send email with PDF attachment
```

#### Step 5 — Wire everything

`app/main.py`:
- Include all routers
- CORS middleware (allow frontend origin)
- Startup: create DB tables if not exist

Test every endpoint with Postman before moving on.

**Vibe coding prompt for Phase 3:**
> "Build a FastAPI backend for a SaaS product called Sentinel. Include:
> JWT auth (register/login), scan file upload endpoint that accepts 3 JSON files
> and triggers an async Celery task, Razorpay payment integration with order
> creation and signature verification, report endpoints that return PDF files,
> SQLAlchemy models for Customer/Report/Scan with SQLite, and a Celery task
> that generates a PDF report and emails it using Resend. Use pydantic-settings
> for config management."

---

### Phase 4 — Frontend (Weekend 4, ~8 hours)

**Goal: Clean web interface for customers to upload scans,
pay, and download reports.**

#### Step 1 — Setup
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install tailwindcss @tailwindcss/vite
npm install @tanstack/react-query react-router-dom axios
npm install lucide-react recharts
npx shadcn@latest init
```

#### Step 2 — Pages to build

**Landing page** (`/`):
- Hero: "Know your network. Before attackers do."
- 3 feature blocks: Scan → Report → Action
- Pricing cards (₹9,999 / ₹14,999/mo / ₹1,29,999/yr)
- CTA: "Get your free sample report"

**Auth pages** (`/login`, `/register`):
- Clean form, email + password
- JWT stored in localStorage
- Redirect to dashboard on success

**Dashboard** (`/dashboard`):
- Welcome message + company name
- "Upload New Scan" button (prominent)
- Recent reports list (last 5)
- Quick stats: total scans, avg risk score

**Upload page** (`/upload`):
- 3 file upload zones (drag and drop)
  - alerts.json
  - device_profiles.json
  - risk_timeline.json
- Company name input
- "Generate Report" button → triggers payment

**Payment page** (`/pay`):
- Order summary: "1x Network Security Report — ₹9,999"
- Razorpay checkout button
- On success → redirect to report

**Report page** (`/reports/:id`):
- Risk score circle (big, coloured)
- 4 stat cards: devices, critical, high, medium
- Threat table with MITRE tags
- Device risk leaderboard with bars
- "Download PDF" button

**Reports list** (`/reports`):
- All past reports as cards
- Each shows: date, risk score, company, download button

#### Step 3 — Connect to backend

`lib/api.js`:
- Axios instance with base URL
- Request interceptor: attach JWT from localStorage
- Response interceptor: redirect to /login on 401

**Vibe coding prompt for Phase 4:**
> "Build a React frontend using Vite, Tailwind CSS, and shadcn/ui for a SaaS
> called Sentinel. Pages: landing page with pricing, login/register with JWT auth,
> dashboard with report history, file upload page for 3 JSON files with drag-drop,
> Razorpay payment integration, and a report detail page showing risk score circle,
> threat table with MITRE ATT&CK tags, device risk leaderboard, and PDF download.
> Use TanStack Query for data fetching and React Router for navigation."

---

### Phase 5 — Agent (Weekend 5, ~4 hours)

**Goal: One script the customer downloads and runs once.
It scans their network and uploads results automatically.**

Build `agent/sentinel_agent.py`:
- Imports all detection modules from Phase 1
- Runs scan for configurable duration (default: 30 min)
- Reads API key and customer ID from `agent_config.yaml`
- Uploads results directly to your API
- Prints friendly progress to terminal:
  ```
  Sentinel Agent v1.0
  Scanning network... (this will take ~30 minutes)
  [=====>        ] 45% — 234 flows processed
  Uploading results...
  Report generation started. You'll receive an email shortly.
  ```

Package as single executable:
```bash
pip install pyinstaller
pyinstaller --onefile agent/sentinel_agent.py
```

Output: `sentinel_agent.exe` (Windows) / `sentinel_agent` (Linux/Mac)

Customer install instructions (entire README for them):
```
1. Download sentinel_agent.exe
2. Double-click to run (run as Administrator on Windows)
3. Enter your API key when prompted
4. Wait 30 minutes
5. Check your email for the report
```

**Vibe coding prompt for Phase 5:**
> "Build a Python script sentinel_agent.py that runs a 30-minute network scan
> using the detection engine modules (sniffer, feature_extractor, anomaly_engine,
> behavioral_fingerprint, risk_engine, mitre_mapper), saves results to temp JSON
> files, then POSTs them to https://api.sentinelaudit.in/api/scans/upload with
> an API key header read from agent_config.yaml. Show a friendly CLI progress bar
> during the scan. Package it with PyInstaller as a single executable."

---

### Phase 6 — Deploy (Weekend 6, ~3 hours)

**Goal: Live product accessible on the internet.**

#### Backend (Railway)
```bash
# Install Railway CLI
npm install -g @railway/cli
railway login
railway new
railway up
railway domain   # get your API URL
```

Add environment variables in Railway dashboard (see .env.example).

#### Frontend (Vercel)
```bash
npm install -g vercel
cd frontend
vercel
# Follow prompts — auto-detects Vite
```

Set `VITE_API_URL` to your Railway backend URL.

#### Domain (Cloudflare)
- Buy `sentinelaudit.in` on GoDaddy or Namecheap (~₹800/year)
- Point to Vercel (frontend) and Railway (API)
- Enable Cloudflare proxy for free SSL + DDoS protection

#### Redis (Railway)
- Add Redis plugin in Railway dashboard
- `REDIS_URL` auto-injected into environment

---

### Phase 7 — First 10 Customers (Month 2–3)

- [ ] Get free trial customer from Phase 0 to pay
- [ ] Ask every paying customer for 1 referral
- [ ] Post on LinkedIn weekly: share anonymised findings
      ("We found a rogue device on a Hyderabad pharma company's
      network last week. Here's what it was doing...")
- [ ] List on IndiaMART: "Network Security Audit Service Hyderabad"
- [ ] Reach out to 5 IT consultants in Hyderabad —
      offer white-label reseller deal (they charge ₹25,000,
      you give them the report for ₹9,999, they keep ₹15,001)
- [ ] Apply to NASSCOM 10,000 Startups programme

---

### Phase 8 — EdgeAI Hardware (Month 6+)

Once you have 10+ paying SaaS customers and ₹1,50,000+/month revenue:

- Build the SentinelEdgeAI hardware box (Pi 5 + Jetson Orin Nano)
- The detection engine from Phase 1 runs on the box
- The box replaces the manual agent install
- Existing SaaS customers are your first hardware buyers
- Price: ₹83,000 box + ₹9,999/month SaaS
- Apply for iCreate / MEITY Startup India hardware grant

---

## Environment Variables

Create `backend/.env` (copy from `.env.example`):

```env
# App
APP_NAME=Sentinel
APP_ENV=development
SECRET_KEY=change-this-to-a-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database
DATABASE_URL=sqlite:///./sentinel.db

# Razorpay (get from razorpay.com/dashboard)
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your_razorpay_secret

# Email via Resend (get from resend.com)
RESEND_API_KEY=re_xxxxxxxxxxxx
FROM_EMAIL=reports@sentinelaudit.in
FROM_NAME=Sentinel Security

# Redis
REDIS_URL=redis://localhost:6379/0

# File storage
UPLOAD_DIR=./uploads
REPORTS_DIR=./reports

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:5173
```

---

## Installation & Local Dev

```bash
# Clone
git clone https://github.com/yourusername/sentinel
cd sentinel

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # fill in values
uvicorn app.main:app --reload    # runs on http://localhost:8000

# Redis (required for Celery)
docker run -d -p 6379:6379 redis:7

# Celery worker (new terminal)
cd backend
celery -A tasks.celery_tasks worker --loglevel=info

# Frontend (new terminal)
cd frontend
npm install
npm run dev                      # runs on http://localhost:5173

# Test detection engine (requires admin/root)
cd backend
sudo python run_detection.py --duration 5 --interface eth0
```

---

## Report Template — 5 Sections

Your `report.html` must render exactly these sections in order:

### Section 1 — Header
- Sentinel logo + "Network Security Audit Report" title
- Company name (large)
- Scan date, report number, scan duration
- Overall risk score circle (large, right side):
  - Red fill if score >= 70
  - Amber fill if score >= 40
  - Green fill if score < 40

### Section 2 — Overview Grid (4 stat boxes)
- Total devices discovered
- Critical alerts (red)
- High risk alerts (amber)
- Total network flows analysed

### Section 3 — Top Threats Detected (table)
Columns: Severity | Description | Affected Device | MITRE ID
- Severity as colour pill: CRITICAL / HIGH / MEDIUM / LOW
- Description in plain English (no jargon)
- MITRE ATT&CK technique ID + name

### Section 4 — Device Risk Leaderboard (table)
Columns: Device Name | IP Address | Risk Score | Bar
- Sorted by risk score descending
- Bar coloured by score: red/amber/green
- Show top 10 devices

### Section 5 — Recommended Actions (numbered list)
- 5–8 specific actions in plain English
- Each has: action title, explanation, estimated fix time
- Priority order: most critical first
- Example:
  1. **Isolate DESKTOP-HR-04 immediately** — This device is scanning
     your internal network, which is a sign of compromise or malware.
     Disconnect it from the network and run an antivirus scan.
     Estimated time: 30 minutes.

### Footer
"Generated by Sentinel · Confidential — for internal use only ·
Next scan recommended in 30 days · sentinelaudit.in"

---

## requirements.txt

```txt
fastapi==0.115.0
uvicorn[standard]==0.30.0
python-multipart==0.0.9
sqlalchemy==2.0.30
alembic==1.13.1
weasyprint==62.3
jinja2==3.1.4
pydantic==2.7.0
pydantic-settings==2.3.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
razorpay==1.4.1
resend==0.7.2
celery==5.4.0
redis==5.0.4
scapy==2.5.0
scikit-learn==1.5.0
pandas==2.2.2
numpy==1.26.4
pyyaml==6.0.1
psutil==5.9.8
python-dotenv==1.0.1
httpx==0.27.0
pytest==8.2.0
pytest-asyncio==0.23.0
pyinstaller==6.7.0
```

---

## package.json (frontend)

```json
{
  "name": "sentinel-frontend",
  "version": "0.1.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint src"
  },
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.23.0",
    "@tanstack/react-query": "^5.40.0",
    "axios": "^1.7.0",
    "recharts": "^2.12.0",
    "lucide-react": "^0.383.0",
    "clsx": "^2.1.1",
    "tailwind-merge": "^2.3.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.3.0",
    "vite": "^5.2.0",
    "tailwindcss": "^3.4.0",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "eslint": "^9.0.0",
    "@eslint/js": "^9.0.0"
  }
}
```

---

## Customer Acquisition Script

**LinkedIn DM (copy-paste this):**

> Hi [Name], I built a tool that scans a company's network and generates
> a security audit report in 10 minutes — the kind consultants charge
> ₹50,000–₹2,00,000 for. I'm looking for 3 businesses in Hyderabad to
> try it completely free and give me feedback. Would you be open to a
> quick 15-minute call this week?

**After free trial — closing script:**

> "The report found [X] on your network. If that became a ransomware
> attack, the average recovery cost for an Indian SME is ₹40–80 lakhs
> in downtime alone. I can send you this report automatically every
> month for ₹14,999. Want to set it up today?"

**LinkedIn profiles to target:**
- "IT Manager Hyderabad"
- "Network Administrator Hyderabad"
- "CTO Hyderabad startup"
- "Operations Manager Hyderabad pharma"
- "Admin Head Hyderabad manufacturing"

---

## Success Milestones

| Milestone | Target date |
|---|---|
| Phase 0 complete — 1 person wants it | End of Week 1 |
| Phase 1 complete — detection engine working | End of Week 2 |
| Phase 2 complete — PDF report generating | End of Week 3 |
| First free report delivered to real customer | Week 4 |
| First paying customer | Week 5–6 |
| Phase 3+4 complete — web app live | Week 7–8 |
| Phase 5 complete — agent working | Week 9–10 |
| 5 paying customers | Month 3 |
| 10 paying customers — ₹1,50,000/month | Month 4–5 |
| Begin EdgeAI hardware build | Month 6 |

---

## What NOT to Build Yet

Do not touch these until you have 10 paying customers:

- Mobile app
- Real-time monitoring dashboard
- Slack / Teams integrations
- SIEM streaming
- Multi-tenant enterprise features
- Custom branding per customer
- Agent auto-update system
- 3D network visualisation
- Anything that takes more than one weekend

Ship the simplest thing that makes someone pay.
Everything else comes after.

---

## Pricing

| Plan | Price | What's included |
|---|---|---|
| One-time report | ₹9,999 | Single scan + PDF report emailed |
| Monthly | ₹14,999/month | Automated monthly reports |
| Annual | ₹1,29,999/year | Monthly reports, 28% saving |
| Consultant | ₹29,999/month | Up to 10 client reports, white-label |

---

## Branding

- **Name:** Sentinel
- **Tagline:** Know your network. Before attackers do.
- **Domain:** sentinelaudit.in
- **Colours:** #0F172A (navy) + #F59E0B (amber) + #EF4444 (red alerts)
- **Font:** Inter (web), same for PDF reports

---

## License

Proprietary — Sentinel © 2026. All rights reserved.

---

## Built By

Vishwa · Hyderabad, India
Building affordable cybersecurity for Indian SMEs.

---

*Start with Phase 0. Talk to customers before writing code.
The detection engine is Phase 1 — that's where you begin building.*
