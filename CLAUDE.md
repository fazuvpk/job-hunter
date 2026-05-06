# Job Hunter — Claude Code Skill File

## Candidate Profile (Source of Truth)

**Name:** Mohammed Afsal V P
**Email:** YOUR_EMAIL@gmail.com
**Phone:** +971XXXXXXXXX
**Location:** Abu Dhabi, UAE
**LinkedIn:** https://www.linkedin.com/in/mohammed-afsal-v-p-2bb9b7249/
**Portfolio:** https://portfolio-plum-pi-62.vercel.app
**GitHub:** https://github.com/mohammadafsalvp
**Years of Experience:** 2
**Education:** B.Tech AI & Data Science, Anna University, CGPA 7.56
**Availability:** Immediate
**Work Authorization:** UAE Resident Visa — no sponsorship needed for UAE roles
**Travel:** Open to UAE; remote preferred
**Remote:** Open to UAE on-site, hybrid, or fully remote (global)
**Salary Floor:** AED 10,000/month (~USD 2,500/month); target AED 10,000–15,000/month

### Tech Stack
- **Automation:** n8n, UiPath, Power Automate, Make, Zapier
- **AI/LLM:** LLM APIs (OpenAI, Azure OpenAI), Prompt Engineering, RAG
- **Programming:** Python, SQL
- **Databases:** Supabase (PostgreSQL), Firebase
- **Cloud:** AWS (S3, Redshift, Lambda), Azure (Fundamentals, OpenAI)
- **APIs:** REST, JSON, OAuth, Webhooks
- **BI:** Power BI, Tableau, Excel
- **Data:** ETL/ELT pipelines, data ingestion & transformation
- **RPA:** UiPath (48.5hr Udemy cert + UiPath Academy Foundation cert)

### Notable Achievements
- **AI Lead Qualification System:** n8n + Telegram + LLM + Supabase → 100% automated lead classification (Hot/Warm/Cold) + CRM entry + follow-up
- **Data Intelligence Pipeline:** 14,000+ records processed end-to-end; 40% reduction in manual reporting effort
- **Customer Analytics (AWS):** 100% automated S3 → Lambda → Redshift for 14,000+ telecom records; zero manual intervention
- **UiPath RPA:** OCR-based extraction from unstructured documents; eliminated human data entry errors
- **Skill Tenet Conversation Engine:** LLM-driven multilingual recruitment automation + candidate repository
- **Idempotent Order Processing:** Python stdlib only, air-gapped RHEL 9.4, SHA-256 audit trail, exponential backoff
- **Research Publication:** "AutoStream: Your All-in-One Data Science Assistant Using LLM" — IJSREM Vol.09 Issue 04, April 2025

### Dream Companies
- n8n GmbH (priority — core tool expert)
- UiPath (certified developer)
- Automation Anywhere (UAE/MENA market leader)

### Blacklist
- Pure body-shopping / staff augmentation agencies
- Roles requiring 7+ years experience
- Salary below AED 5,000/month
- US citizens only / clearance required

---

## Slash Commands

### `/job-hunter:discover`

**Purpose:** Run job discovery, score all results, save to SQLite.

**Steps:**
1. Read `config/search.json` for search parameters
2. For each title in `titles` array, call JobSpy MCP with:
   - `site_name`: all sites from `sites` array
   - `search_term`: current title
   - `results_wanted`: `results_per_title`
   - `is_remote`: false (search both UAE-located and remote)
   - `location`: search "Abu Dhabi UAE" AND "Remote" for each title
3. For each job returned:
   - Check `data/jobs.db` for duplicate `external_id` — skip if exists
   - Check `config/blacklist.json` patterns against title + company + description
   - If not blacklisted, score using `prompts/scorer.md` rubric
   - Insert into `jobs` table with score, breakdown, recommendation
   - Update `daily_stats` for today
4. Report: "Discovered X jobs, Y new, Z scored above threshold, W auto-skipped"

**MCP Tools Used:** `jobspy`, `sqlite`

**Anti-detection:** No pacing needed for discovery (read-only scraping).

---

### `/job-hunter:review`

**Purpose:** Show pending jobs scoring >= 60 one by one for human approval.

**Steps:**
1. Query SQLite: `SELECT * FROM jobs WHERE status = 'pending' AND score >= 60 ORDER BY score DESC`
2. For each job, display a formatted card:
   ```
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   [SCORE: 87/100] AI Automation Engineer
   Company:  TechFlow UAE (SaaS product)
   Location: Abu Dhabi, UAE (hybrid)
   Salary:   AED 12,000–16,000/month
   Source:   LinkedIn
   URL:      https://...

   GREEN FLAGS: n8n required, UAE role (no visa friction), Python + Supabase
   RED FLAGS:   None

   SUMMARY: Strong n8n + Python automation role at UAE SaaS startup.
            Hybrid Abu Dhabi — Afsal's resident visa means zero friction.

   BREAKDOWN:
     Role match:            18/20
     Tech stack:            17/20
     Location/remote fit:   15/15
     Seniority alignment:   10/10
     Salary signal:         10/10
     Company quality:        9/10
     Growth opportunity:     4/5
     Application ease:       3/5
     Timezone fit:           3/3
     Visa clarity:           2/2

   ─────────────────────────────────────────
   [A] Approve   [S] Skip   [B] Blacklist company
   ```
3. Wait for keypress:
   - `A` → set `status = 'approved'`, set `reviewed_at`, proceed to next
   - `S` → set `status = 'skipped'`, set `reviewed_at`, proceed to next
   - `B` → set `status = 'skipped'`, add company to `config/blacklist.json`, proceed to next
4. After all reviewed, report summary counts.

**MCP Tools Used:** `sqlite`

---

### `/job-hunter:apply [id]`

**Purpose:** For an approved job: tailor resume, generate cover letter, submit application.

**Steps:**
1. Fetch job record from SQLite by `id`
2. Verify `status = 'approved'` — abort if not
3. Check daily application count: `SELECT COUNT(*) FROM applications WHERE DATE(submitted_at) = DATE('now')` — abort if >= 8
4. **Tailor Resume:**
   - Read `prompts/resume_tailor.md`
   - Generate tailored resume JSON mapped to job description keywords
   - Save to `output/resumes/resume_{id}_{company_slug}.md`
   - Update `jobs.resume_path`
5. **Generate Cover Letter:**
   - Read `prompts/cover_letter.md`
   - Generate 3-paragraph cover letter (see prompt for rules)
   - Save to `output/covers/cover_{id}_{company_slug}.md`
   - Update `jobs.cover_path`
6. **Submit via Playwright:**
   - Navigate to job URL
   - Detect ATS platform (Greenhouse, Lever, Workday, LinkedIn Easy Apply, direct)
   - Fill fields using `config/screening.json` for standard answers
   - Upload tailored resume file
   - Paste cover letter text
   - **Pace each action:** wait 3–8 seconds between field fills (random within range)
   - Submit and capture confirmation number/text
7. **Record in DB:**
   - Set `jobs.status = 'applied'`, `jobs.applied_at = NOW()`
   - Insert into `applications` table with `method`, `ats_platform`, `confirmation`
   - Update `daily_stats` for today

**MCP Tools Used:** `playwright`, `sqlite`, `filesystem`

**Anti-detection Rules:**
- Hard cap: 8 applications per calendar day — refuse if limit reached
- Random delay 3–8 seconds between each Playwright action
- Do not submit identical cover letters — always job-specific
- Do not use autofill keyboard shortcuts that trigger bot detection

---

### `/job-hunter:status`

**Purpose:** Show dashboard of all pipeline metrics.

**Output Format:**
```
━━━━━━━━━━━━━━━━ JOB HUNTER DASHBOARD ━━━━━━━━━━━━━━━━

TODAY (2026-05-06)
  Discovered:   12    Applied:  3 / 8 limit
  Scored:       12    Responses: 0

ALL TIME PIPELINE
  Total Found:  247   ████████████████████
  Pending:       18   ████
  Approved:       9   ██
  Applied:       43   █████████
  Responses:      7   █
  Interviews:     2

RECENT APPLICATIONS (last 7 days)
  2026-05-05  n8n GmbH — Automation Engineer          ✓ Submitted
  2026-05-04  TechFlow UAE — AI Automation Engineer   ✓ Submitted
  2026-05-03  UiPath — RPA Developer                  ⏳ Pending response

TOP PENDING (ready to review)
  Score 91 — AI Automation Engineer @ n8n GmbH (HIGH PRIORITY — n8n expert override)
  Score 84 — RPA Developer @ UiPath
  Score 78 — Workflow Automation Dev @ CloudCo UAE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**MCP Tools Used:** `sqlite`

---

### `/job-hunter:watchlist`

**Purpose:** Check n8n GmbH, UiPath, Automation Anywhere and other priority companies for new job openings.

**Steps:**
1. Read `config/watchlist.json` for company list and URLs
2. **Always check n8n GmbH first** before any other company
3. For each company, use Playwright to:
   - Navigate to careers page URL
   - Extract all open roles with titles, locations, links
   - Pace: 3–8 seconds between companies
4. For each role found:
   - Check if already in `jobs` table by URL or title+company
   - If new: score it, insert as `status = 'pending'`
5. **Special n8n GmbH rule:** Any n8n GmbH role scoring >= 45 → flag as HIGH PRIORITY, add `notes = 'n8n expert override — priority flag'`
6. Report: "n8n GmbH: 2 new roles found. [titles]"

**Special handling for n8n GmbH:**
- Always check first
- Flag any role scoring >= 45 as high priority (score override note in `notes`)
- Display n8n GmbH results prominently regardless of score

**MCP Tools Used:** `playwright`, `sqlite`

---

### `/job-hunter:follow-up`

**Purpose:** List applications older than 7 days with no response and draft follow-up emails.

**Steps:**
1. Query: `SELECT j.*, a.* FROM jobs j JOIN applications a ON a.job_id = j.id WHERE j.status = 'applied' AND j.response_at IS NULL AND a.submitted_at < datetime('now', '-7 days') AND a.follow_up_sent = 0`
2. For each result, draft a follow-up email:
   - Subject: `Following up: [Role Title] Application`
   - Body: 3–4 sentences, professional, reference original application date, restate interest, offer to provide additional info
   - Use specific company name and role title
3. Display drafts for review
4. If approved: send via Gmail MCP
5. Update `applications.follow_up_sent = 1`, `applications.follow_up_at = NOW()`

**MCP Tools Used:** `sqlite`, Gmail MCP (if configured)

---

## Scoring Rubric Summary

See `prompts/scorer.md` for the full prompt. Dimensions:

| Dimension | Max Points |
|-----------|-----------|
| Role match | 20 |
| Tech stack overlap | 20 |
| Location / remote fit | 15 |
| Seniority alignment | 10 |
| Salary signal | 10 |
| Company quality | 10 |
| Growth opportunity | 5 |
| Application complexity | 5 |
| Timezone fit | 3 |
| Visa clarity | 2 |
| **Total** | **100** |

- **>= 80:** Auto-recommend APPLY
- **60–79:** REVIEW (show to Afsal)
- **35–59:** Flag as borderline SKIP
- **< 35:** Auto-skip, never show

---

## MCP Tool Usage Instructions

### JobSpy MCP (`jobspy`)
- Use for initial job discovery across LinkedIn, Indeed, Glassdoor, Google Jobs
- Pass `is_remote: false` and search both "Abu Dhabi UAE" and "Remote" for each title
- Deduplicate by `job_url` before inserting

### Playwright MCP (`playwright`)
- Use for watchlist scraping and application submission
- Always add 3–8 second random delays between actions
- On CAPTCHA detection: pause, notify user, do not attempt to bypass
- Screenshot on errors for debugging

### SQLite MCP (`sqlite`)
- Database path: `./data/jobs.db`
- Always use parameterized queries
- Run schema.sql on first setup if tables don't exist

### Filesystem MCP (`filesystem`)
- Root: `./` (job-hunter directory)
- Use for reading/writing resumes and cover letters

---

## Safety & Anti-Detection Rules

1. **Daily cap:** Maximum 8 applications per calendar day — hard stop
2. **Pacing:** 3–8 second random delay between each Playwright action
3. **No bulk apply:** Never use LinkedIn "Easy Apply All" or similar bulk features
4. **Unique content:** Every cover letter must be job-specific — no templates
5. **CAPTCHA:** If detected, stop and notify user immediately
6. **Rate limiting:** If a job board returns 429, wait 60 seconds before retry (max 2 retries)
7. **Blacklist enforcement:** Check blacklist before every application, not just discovery

---

## File Structure Reference

```
~/job-hunter/
├── CLAUDE.md              ← This file
├── .mcp.json              ← MCP server configuration
├── setup.sh               ← One-time setup script
├── README.md              ← Full documentation
├── config/
│   ├── profile.json       ← Candidate profile data
│   ├── search.json        ← Search parameters
│   ├── screening.json     ← Standard ATS answers
│   ├── watchlist.json     ← Priority companies to monitor
│   └── blacklist.json     ← Companies/patterns to skip
├── prompts/
│   ├── scorer.md          ← Job scoring prompt (0–100)
│   ├── cover_letter.md    ← Cover letter generation prompt
│   └── resume_tailor.md   ← Resume tailoring instructions
├── data/
│   ├── schema.sql         ← SQLite schema
│   └── jobs.db            ← Generated database (gitignored)
└── output/
    ├── resumes/           ← Tailored resume outputs
    └── covers/            ← Cover letter outputs
```
