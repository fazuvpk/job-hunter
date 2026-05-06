# Job Hunter — AI-Powered Job Application Automation
### Hey Afsal 👋 This system was set up for you by Fazil.

This tool uses Claude Code + MCP servers to automate your entire job search pipeline: discover → score → review → apply → follow up. It's tailored to your profile as a Junior AI Automation Engineer based in Abu Dhabi.

---

## Before You Start — Fill These In

Before running anything, open these two files and fill in your details:

### 1. `config/profile.json`
Find and replace these placeholder values:
```json
"email": "YOUR_EMAIL@gmail.com"   → your actual Gmail address
"phone": "+971XXXXXXXXX"          → your UAE mobile number
```

### 2. `config/screening.json`
Find and replace these placeholder values:
```json
"email": "YOUR_EMAIL@gmail.com"   → your actual Gmail address
"phone": "+971XXXXXXXXX"          → your UAE mobile number
"linkedin": "..."                  → verify URL is correct
"portfolio": "..."                 → verify URL is correct
"github": "..."                    → verify URL is correct
```

### 3. Drop your resume PDF
Place your base resume as:
```
output/resumes/base_resume.pdf
```
This is used as the upload file for applications. The tailored content is generated per-application, but ATS systems often require a PDF upload.

---

## Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Claude Code CLI | Latest | `npm install -g @anthropic-ai/claude-code` |
| Python | 3.10+ | https://python.org |
| Node.js | 18+ | https://nodejs.org |
| Git | Any | https://git-scm.com |

---

## Setup

```bash
git clone https://github.com/fazilkunhamed/job-hunter.git
cd job-hunter
git checkout mohd-afsal
bash setup.sh
```

The setup script installs Python dependencies, initializes the SQLite database, and verifies MCP server configuration.

---

## Starting Claude Code

```bash
cd ~/job-hunter
claude
```

Then use the slash commands below.

---

## Slash Commands

### `/job-hunter:discover`
Searches LinkedIn, Indeed, Glassdoor, and Google Jobs for all your target roles (both UAE-based and remote), scores each one 0–100, and saves results to the database.

```
/job-hunter:discover
→ Discovered 47 jobs, 31 new, 12 scored above 60, 19 auto-skipped
```

Runs automatically for all 10 role titles in `config/search.json`. Checks both Abu Dhabi/UAE locations and remote.

---

### `/job-hunter:review`
Shows you every job scoring >= 60 one at a time with a full scorecard. You decide: Approve, Skip, or Blacklist the company.

```
/job-hunter:review
→ Shows job cards one by one, waits for [A] / [S] / [B] keypress
```

Typical session: 10–20 minutes to review a day's worth of discoveries.

---

### `/job-hunter:apply [id]`
Takes an approved job ID, tailors your resume to the JD, generates a job-specific cover letter, and submits the application via Playwright.

```
/job-hunter:apply 42
→ Tailoring resume for "AI Automation Engineer @ TechFlow UAE"...
→ Generating cover letter...
→ Submitting via LinkedIn Easy Apply...
→ Application submitted. Confirmation: APP-2026-94821
```

Hard limit: 8 applications per day. The system refuses if you've hit the cap.

---

### `/job-hunter:status`
Prints a full dashboard of your pipeline: today's stats, all-time pipeline counts, recent applications, and top pending jobs ready to review.

```
/job-hunter:status
```

---

### `/job-hunter:watchlist`
Checks n8n GmbH (first, always), UiPath, Automation Anywhere, and UAE AI startup searches for new openings. Any new role is scored and added to the pipeline.

```
/job-hunter:watchlist
→ n8n GmbH: 1 new role — "Automation Engineer (Remote)" — HIGH PRIORITY
→ UiPath: 0 new roles
→ Automation Anywhere: 2 new roles
```

n8n GmbH roles scoring >= 45 are always flagged as HIGH PRIORITY regardless of score.

---

### `/job-hunter:follow-up`
Finds applications older than 7 days with no response and drafts professional follow-up emails for your review.

```
/job-hunter:follow-up
→ 3 applications eligible for follow-up
→ Drafting emails... [review and approve each]
```

Sends via Gmail MCP when you approve. Updates the database to prevent duplicate follow-ups.

---

## Scoring System

Each job is scored 0–100 across 10 dimensions:

| Dimension | Max | What it measures |
|-----------|-----|-----------------|
| Role match | 20 | Does the title/responsibilities match your target roles? |
| Tech stack overlap | 20 | How many of your tools (n8n, UiPath, Python, etc.) appear in the JD? |
| Location / remote fit | 15 | UAE role = 15 pts (no visa friction); remote/global = 15 pts |
| Seniority alignment | 10 | Junior/0–2yr = 10; mid/2–4yr = 8; 5yr+ = decreasing |
| Salary signal | 10 | >= AED 10,000/month = 10; unclear = 6; below floor = 0 |
| Company quality | 10 | Product company/SaaS/funded startup = 10; body shop = 0 |
| Growth opportunity | 5 | Ownership, architecture decisions, R&D signals |
| Application complexity | 5 | Easy Apply = 5; complex ATS = 3; broken = 0 |
| Timezone fit | 3 | Async/global/GST-compatible = 3 |
| Visa clarity | 2 | UAE role = 2; no restriction = 1; requires non-UAE work auth = 0 |

**Thresholds:**
- **>= 80:** Auto-recommend APPLY
- **60–79:** REVIEW (your decision)
- **35–59:** Auto-skip (borderline)
- **< 35:** Discarded, never shown

---

## Your Strongest Selling Points

The system is built to surface these in every cover letter and tailored resume:

1. **n8n production system** — AI Lead Qualification with 100% automated CRM entry + follow-up (most employers have never seen this built end-to-end)
2. **UiPath certified** — 48.5hr Udemy course + UiPath Academy Foundation cert — rare for someone 2 years in
3. **14,000+ record pipeline** — both AWS (S3→Lambda→Redshift) and n8n (Data Intelligence Pipeline) at scale
4. **AWS 100% automated** — real cloud production experience, not just tutorials
5. **Skill Tenet LLM engine** — multilingual, RAG-based, built in collaboration with a senior engineer
6. **IIT Madras Applied AI Mastery cert** — highest-tier Indian institution, differentiates you in AI roles
7. **UAE residency = zero friction** — for every UAE-based role, no sponsorship, no waiting, immediate start

---

## Configuration Files

| File | Purpose |
|------|---------|
| `config/profile.json` | Your full candidate profile — fill in email/phone |
| `config/search.json` | Job titles to search, sites, score thresholds |
| `config/screening.json` | Standard ATS answers — fill in email/phone |
| `config/watchlist.json` | n8n GmbH, UiPath, Automation Anywhere + UAE startup searches |
| `config/blacklist.json` | Patterns and companies to auto-skip |

---

## Daily Workflow

**Morning (~15 min):**
```
/job-hunter:watchlist    ← check dream companies for new roles
/job-hunter:discover     ← run broad job search
/job-hunter:review       ← approve/skip new results
```

**Midday (~10 min per application):**
```
/job-hunter:apply [id]   ← apply to each approved job (up to 8/day)
```

**Weekly (~5 min):**
```
/job-hunter:follow-up    ← send follow-ups for week-old applications
/job-hunter:status       ← check full pipeline health
```

---

## Safety & Anti-Detection

The system follows these rules automatically:

1. **8 applications/day hard cap** — refuses to apply if limit reached
2. **3–8 second random delays** between every Playwright action
3. **No bulk apply** — never uses LinkedIn "Easy Apply All"
4. **Unique cover letters** — every letter is generated fresh for the specific JD
5. **CAPTCHA detection** — stops and notifies you immediately; never attempts bypass
6. **Rate limiting** — waits 60 seconds on HTTP 429, max 2 retries
7. **Blacklist check** — runs before every application, not just discovery

---

## Troubleshooting

**Database issues:**
```bash
sqlite3 data/jobs.db ".tables"
sqlite3 data/jobs.db "SELECT COUNT(*) FROM jobs;"
```

**Reset and re-run schema:**
```bash
sqlite3 data/jobs.db < data/schema.sql
```

**MCP server status:**
```bash
cat .mcp.json
```

**Check today's applications:**
```bash
sqlite3 data/jobs.db "SELECT * FROM applications WHERE DATE(submitted_at) = DATE('now');"
```

---

## File Structure

```
~/job-hunter/
├── CLAUDE.md              ← System instructions for Claude Code
├── .mcp.json              ← MCP server configuration
├── setup.sh               ← One-time setup script
├── README.md              ← This file
├── config/
│   ├── profile.json       ← Your candidate profile (fill in email/phone)
│   ├── search.json        ← Job titles and search parameters
│   ├── screening.json     ← Standard ATS answers (fill in email/phone)
│   ├── watchlist.json     ← n8n GmbH, UiPath, Automation Anywhere + UAE startups
│   └── blacklist.json     ← Auto-skip patterns
├── prompts/
│   ├── scorer.md          ← Job scoring rubric (0–100) tailored for Afsal
│   ├── cover_letter.md    ← Cover letter generation (n8n/UiPath/data/AI/general)
│   └── resume_tailor.md   ← Resume tailoring instructions
├── data/
│   ├── schema.sql         ← SQLite database schema
│   └── jobs.db            ← Generated database (gitignored — not committed)
└── output/
    ├── resumes/
    │   ├── base_resume.pdf          ← DROP YOUR RESUME HERE
    │   └── resume_{id}_{slug}.md    ← Tailored resumes (auto-generated)
    └── covers/
        └── cover_{id}_{slug}.md     ← Cover letters (auto-generated)
```
