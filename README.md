# Job Hunter — AI-Powered Job Application Automation

Automated job discovery, scoring, tailoring, and application system for Fazil Kunhamed. Powered by Claude Code with MCP servers for job scraping, browser automation, and database management.

---

## Prerequisites

| Tool | Purpose | Install |
|------|---------|---------|
| Claude Code | AI engine + slash commands | `npm install -g @anthropic-ai/claude-code` |
| Python + uv | JobSpy and SQLite MCP servers | `pip install uv` |
| Node.js 18+ | Playwright and filesystem MCP | https://nodejs.org |
| sqlite3 CLI | Database initialization | `brew install sqlite` |

---

## Setup

```bash
cd ~/job-hunter
bash setup.sh
```

This will:
1. Check all prerequisites
2. Create `data/`, `output/resumes/`, `output/covers/` directories
3. Initialize `data/jobs.db` with the full schema
4. Verify `.mcp.json` is in place
5. Pre-fetch MCP server binaries

---

## Starting Claude Code

```bash
cd ~/job-hunter
claude
```

Claude Code will automatically load `CLAUDE.md` and connect the MCP servers defined in `.mcp.json`.

---

## Slash Commands

### `/job-hunter:discover`
Runs job discovery across LinkedIn, Indeed, Glassdoor, ZipRecruiter, and Google Jobs. Scores every result 0–100 and saves to SQLite. Skips duplicates and blacklisted patterns.

```
/job-hunter:discover
```

**What it does:**
- Searches for all titles in `config/search.json`
- Filters to remote-only roles
- Scores each job across 10 dimensions (see Scoring section)
- Saves all results to `data/jobs.db`
- Auto-skips jobs scoring < 35

**Typical output:**
```
Discovered 47 jobs, 31 new, 18 scored >= 60, 13 auto-skipped
```

---

### `/job-hunter:review`
Interactive review of pending jobs scoring >= 60. Shows one job at a time as a card with full score breakdown.

```
/job-hunter:review
```

**Controls:**
- `A` — Approve (queue for application)
- `S` — Skip (not interested)
- `B` — Blacklist company (skip + add to blacklist)

**Card example:**
```
[SCORE: 87/100] Senior Angular Developer
Company:  TechCorp (Series B SaaS)
Location: Remote (Global)
Salary:   $5,000–$7,000/month
Source:   LinkedIn

GREEN FLAGS: Angular 19, async-first, equity offered
RED FLAGS:   No salary in posting (estimated from funding)

BREAKDOWN:
  Role match:           18/20
  Tech stack:           17/20
  Remote:               15/15
  ...
```

---

### `/job-hunter:apply [id]`
Applies to an approved job: tailors resume, generates cover letter, submits via Playwright.

```
/job-hunter:apply 42
```

**What it does:**
1. Verifies job is approved and daily limit not reached (max 8/day)
2. Generates a tailored resume (saved to `output/resumes/`)
3. Generates a job-specific cover letter (saved to `output/covers/`)
4. Navigates to job URL with Playwright
5. Detects ATS platform and fills all fields
6. Uses `config/screening.json` for standard answers
7. Submits and records confirmation

**Safety limits:** Hard cap of 8 applications per day. Random 3–8 second delays between Playwright actions.

---

### `/job-hunter:status`
Shows full pipeline dashboard.

```
/job-hunter:status
```

**Output includes:**
- Today's stats vs daily limit
- All-time pipeline counts
- Recent applications with status
- Top pending jobs ready to review

---

### `/job-hunter:watchlist`
Checks priority companies (especially AXI) for new openings.

```
/job-hunter:watchlist
```

**What it does:**
- Visits careers pages in `config/watchlist.json`
- Extracts open roles and checks for new ones
- Scores new roles and adds to database
- Always shows AXI results prominently

---

### `/job-hunter:follow-up`
Drafts follow-up emails for applications older than 7 days with no response.

```
/job-hunter:follow-up
```

**What it does:**
- Queries applications where: status=applied, no response, > 7 days old, no follow-up sent
- Drafts professional follow-up emails
- Shows drafts for approval
- Sends via Gmail MCP (if configured)
- Marks `follow_up_sent = 1` in database

---

## Scoring System (0–100)

| Dimension | Max | Notes |
|-----------|-----|-------|
| Role match | 20 | Exact title match vs senior vs stretch |
| Tech stack overlap | 20 | Count of Fazil's skills in JD |
| Remote compatibility | 15 | Fully remote=15, hybrid=5, onsite=0 |
| Seniority alignment | 10 | Senior/lead=10, mid=5, junior=0 |
| Salary signal | 10 | Above $4K=10, unclear likely ok=6, below=0 |
| Company quality | 10 | Product startup=10, agency=2 |
| Growth opportunity | 5 | Architecture/leadership mentioned=5 |
| Application complexity | 5 | Easy Apply=5, complex ATS=2 |
| Timezone fit | 3 | Async/global=3, India overlap=2, US only=0 |
| Visa clarity | 2 | Explicitly open=2, unclear=1, local only=0 |

**Thresholds:**
- **>= 80:** Auto-recommend APPLY
- **60–79:** Show in review queue (Fazil decides)
- **35–59:** Auto-skip (not shown)
- **< 35:** Discarded immediately

---

## Configuration Files

### `config/search.json`
Controls what to search for, how many results, and what thresholds to use.

### `config/profile.json`
Complete candidate profile used by all prompts.

### `config/screening.json`
Standard answers to ATS screening questions. Edit `expected_salary` if your target changes.

### `config/watchlist.json`
Priority companies to monitor. Add new companies with `careers_url` and `priority`.

### `config/blacklist.json`
Patterns that trigger automatic skip. Add company names to `blacklisted_companies` during review with `B` key.

---

## Database Schema

### `jobs` table
All discovered jobs with scores, status, and file paths.

**Status flow:** `pending` → `approved` or `skipped` → `applied` → (response received updates `response_at`)

### `applications` table
One row per submitted application. Tracks ATS platform, confirmation, and follow-up status.

### `daily_stats` table
Aggregated daily counts for dashboard display.

---

## File Structure

```
~/job-hunter/
├── CLAUDE.md                  ← Slash command definitions + candidate profile
├── .mcp.json                  ← MCP server configuration
├── setup.sh                   ← One-time setup script
├── README.md                  ← This file
├── config/
│   ├── profile.json           ← Candidate profile (structured)
│   ├── search.json            ← Search parameters and thresholds
│   ├── screening.json         ← ATS question answers
│   ├── watchlist.json         ← Priority companies
│   └── blacklist.json         ← Skip patterns
├── prompts/
│   ├── scorer.md              ← Scoring rubric (10 dimensions)
│   ├── cover_letter.md        ← Cover letter generation rules
│   └── resume_tailor.md      ← Resume tailoring instructions
├── data/
│   ├── schema.sql             ← Database schema
│   └── jobs.db               ← SQLite database (generated)
└── output/
    ├── resumes/               ← Tailored resume outputs (Markdown)
    └── covers/                ← Cover letter outputs (Markdown)
```

---

## Daily Workflow

### Morning (15–20 minutes)
```
/job-hunter:discover     ← Find new jobs
/job-hunter:watchlist    ← Check AXI + priority companies
/job-hunter:review       ← Approve/skip pending jobs
```

### Midday (30–45 minutes)
```
/job-hunter:apply [id]   ← Apply to approved jobs (up to 8/day)
/job-hunter:status       ← Check pipeline
```

### Weekly
```
/job-hunter:follow-up    ← Send follow-ups on aging applications
```

---

## Safety & Anti-Detection

- **Daily cap:** Maximum 8 applications per day — hard enforced
- **Pacing:** 3–8 second random delay between every Playwright action
- **Unique content:** Every cover letter is job-specific
- **CAPTCHA:** System stops and notifies if CAPTCHA is detected — never auto-bypasses
- **Rate limiting:** Backs off 60 seconds on 429 errors, max 2 retries
- **Blacklist enforcement:** Checked at every stage, not just discovery

---

## Troubleshooting

**MCP servers not connecting:**
```bash
# Test jobspy
uvx jobspy-mcp-server --help

# Test sqlite
uvx mcp-server-sqlite --help

# Test playwright
npx @playwright/mcp@latest --help
```

**Database issues:**
```bash
# Reinitialize (WARNING: deletes all data)
rm ./data/jobs.db
sqlite3 ./data/jobs.db < ./data/schema.sql
```

**Check today's applications:**
```bash
sqlite3 ./data/jobs.db "SELECT j.title, j.company, a.submitted_at FROM applications a JOIN jobs j ON j.id = a.job_id WHERE DATE(a.submitted_at) = DATE('now');"
```

**View top pending jobs:**
```bash
sqlite3 ./data/jobs.db "SELECT id, score, title, company FROM jobs WHERE status='pending' AND score >= 60 ORDER BY score DESC LIMIT 10;"
```
