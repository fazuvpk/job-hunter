# Job Hunter - Claude Code Skill File

## Candidate Profile (Source of Truth)

**Name:** Fazil Kunhamed  
**Email:** fazil.kunhamed@gmail.com  
**Phone:** +917356634634  
**Location:** Kerala, India  
**LinkedIn:** https://www.linkedin.com/in/fazilkunhamed  
**Years of Experience:** 10  
**Availability:** Immediate  
**Work Authorization:** Indian citizen, open to visa sponsorship  
**Travel:** Weekly within India OK; abroad depends on offer; **avoid UAE**  
**Remote:** Fully remote, global preferred  
**Salary Floor:** $4,000 USD/month minimum (target $4,000–$6,000/month)

### Tech Stack
- **Backend:** .NET Core, ASP.NET MVC, Web API, Entity Framework, Node.js, SQL Server
- **Frontend:** Angular 14–19, React, Vue, TypeScript, RxJS, JavaScript ES2022
- **Mobile:** Android (Kotlin, Java)
- **AI/Automation:** Claude Code, OpenAI API, n8n
- **Cloud:** AWS (SES, S3, Kinesis), Azure (App Services, Web Jobs, Storage, Event Grid)
- **Architecture:** Clean Architecture, CQRS, SOLID, Microservices, SignalR

### Notable Achievements
- **Oops AppLock** (Android): 7.7M+ downloads, featured on LifeHacker
- **Samsung SDS:** $45K revenue in 6 months, 20% cloud cost reduction, PII encryption of 20M+ records in 3 minutes
- **ADNOC:** Angular 14→19 migration, 55% bundle reduction, 33% API performance improvement
- **Skill Tenet:** Three.js 3D globe hero section, GSAP animations, Vite build pipeline

### Dream Companies
- AXI (priority)
- Funded startups seeking senior technical consultation

### Blacklist
- Pure body-shopping / staff augmentation agencies
- UAE-relocation required roles
- Roles below $4,000/month

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
   - `is_remote`: true
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
   [SCORE: 87/100] Senior Full Stack Developer
   Company:  Acme Corp (Product startup)
   Location: Remote (Global)
   Salary:   $5,000–$7,000/month
   Source:   LinkedIn
   URL:      https://...

   GREEN FLAGS: Angular 19, remote-first, equity
   RED FLAGS:   None

   SUMMARY: Strong Angular + .NET role at product startup.
            Fully async team, no relocation required.

   BREAKDOWN:
     Role match:          18/20
     Tech stack:          17/20
     Remote:              15/15
     Seniority:           10/10
     Salary signal:       10/10
     Company quality:      9/10
     Growth opportunity:   4/5
     Application ease:     3/5
     Timezone fit:         3/3
     Visa clarity:         1/2

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

TODAY (2026-04-08)
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
  2026-04-07  Acme Corp — Senior Full Stack Dev      ✓ Submitted
  2026-04-06  TechStartup — Angular Developer        ✓ Submitted
  2026-04-05  GlobalSoft — .NET Architect            ⏳ Pending response

TOP PENDING (ready to review)
  Score 91 — Lead Full Stack Engineer @ NovaTech
  Score 84 — Senior Angular Dev @ ProductHouse
  Score 78 — .NET Solutions Architect @ CloudCo
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**MCP Tools Used:** `sqlite`

---

### `/job-hunter:watchlist`

**Purpose:** Check AXI and priority companies for new job openings.

**Steps:**
1. Read `config/watchlist.json` for company list and URLs
2. For each company, use Playwright to:
   - Navigate to careers page URL
   - Extract all open roles with titles, locations, links
   - Pace: 3–8 seconds between companies
3. For each role found:
   - Check if already in `jobs` table by URL or title+company
   - If new: score it, insert as `status = 'pending'`
4. Report: "AXI: 2 new roles found. [titles]"

**Special handling for AXI:**
- Always check AXI first
- Flag any AXI role scoring >= 50 as high priority (score override note in `notes`)
- Display AXI results prominently regardless of score

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
| Remote compatibility | 15 |
| Seniority alignment | 10 |
| Salary signal | 10 |
| Company quality | 10 |
| Growth opportunity | 5 |
| Application complexity | 5 |
| Timezone fit | 3 |
| Visa clarity | 2 |
| **Total** | **100** |

- **>= 80:** Auto-recommend APPLY
- **60–79:** REVIEW (show to Fazil)
- **35–59:** Flag as borderline SKIP
- **< 35:** Auto-skip, never show

---

## MCP Tool Usage Instructions

### JobSpy MCP (`jobspy`)
- Use for initial job discovery across LinkedIn, Indeed, Glassdoor, ZipRecruiter, Google Jobs
- Always pass `is_remote: true`
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
