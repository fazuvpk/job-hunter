# Cover Letter Generation Prompt

You are writing a cover letter for Mohammed Afsal V P, a Junior AI Automation Engineer with 2 years of experience.

## Candidate Profile (for reference)
- **Name:** Mohammed Afsal V P
- **Location:** Abu Dhabi, UAE (UAE Resident Visa — no sponsorship needed)
- **Stack:** n8n, UiPath, Power Automate, Python, SQL, LLM APIs (OpenAI, Azure OpenAI), RAG, Supabase (PostgreSQL), Firebase, AWS (S3, Redshift, Lambda), Azure, Power BI, ETL/ELT pipelines
- **Education:** B.Tech AI & Data Science, Anna University, CGPA 7.56
- **Key achievements (use exact numbers):**
  - AI Lead Qualification System: n8n + Telegram + LLM (OpenAI/Gemini) + Supabase → auto-classifies leads Hot/Warm/Cold, **100% automated** CRM entry + follow-up
  - Automated Data Intelligence Pipeline: **14,000+ records** processed end-to-end; **40% reduction** in manual reporting effort; n8n + Supabase + Quadratic AI
  - Customer Analytics (AWS): **100% automated** data flow S3 → Lambda → Redshift; **14,000+ telecom records**; zero manual intervention
  - UiPath RPA: OCR-based extraction from unstructured documents; **eliminated human data entry errors**
  - Skill Tenet Conversation Engine: LLM-driven **multilingual** recruitment automation + candidate repository
  - Idempotent Order Processing: Python stdlib only, air-gapped RHEL 9.4, SHA-256 audit trail, exponential backoff
  - Research Publication: "AutoStream: Your All-in-One Data Science Assistant Using LLM" — IJSREM Vol.09 Issue 04, April 2025
- **Certifications:** Applied AI Mastery (IIT Madras), UiPath RPA Developer 48.5hr (Udemy + UiPath Academy Foundation), Prompt Engineering (Dubai Future Foundation)

---

## Inputs You Will Receive

- `job_title`: The role title
- `company_name`: The company name
- `job_description`: Full job description text
- `role_type`: One of: n8n_automation, rpa_uipath, data_engineering, ai_integration, general_automation
- `tailored_resume_summary`: The summary from the tailored resume for this job

---

## Rules — Follow Strictly

1. **Never open with "I am writing to apply..."** — This opener is banned.
2. **Maximum 3 paragraphs.** No longer.
3. **No filler phrases:** Avoid "I am passionate about", "I am excited to", "I have always been fascinated by", "team player", "hard worker", "detail-oriented."
4. **Always use the specific company name** — never "your company."
5. **Always use the specific role title** — never "this role" or "the position."
6. **Include exact numbers** — pull from achievements above.
7. **Mirror JD keywords** — use terms from the job description naturally.
8. **Confident tone, not arrogant** — state facts and outcomes, not self-assessments.
9. **Ending must include a clear call to action** — availability + next step.
10. **For UAE roles:** Always include this sentence naturally in paragraph 3: "I'm based in Abu Dhabi with an active UAE resident visa — no sponsorship or relocation needed."

---

## Structure

### Paragraph 1: The Hook (3–4 sentences)
- Open with a specific connection between one of Afsal's most relevant projects and a problem the company is clearly trying to solve
- Reference the company by name and what they're building
- Do not summarize Afsal's career — get straight to the point of relevance
- Examples by role type:
  - **n8n_automation:** Reference the AI Lead Qualification System (n8n + Telegram + LLM + Supabase, 100% automated CRM) — connect to their workflow automation problem
  - **rpa_uipath:** Reference the UiPath OCR extraction work (eliminated data entry errors) + certifications
  - **data_engineering:** Reference the AWS pipeline (S3→Lambda→Redshift, 14k+ records, 100% automated) or Data Intelligence Pipeline (40% effort reduction)
  - **ai_integration:** Reference the Skill Tenet Conversation Engine (LLM + RAG + multilingual) or research publication
  - **general_automation:** Reference Idempotent Order Processing (Python, air-gapped, production-grade reliability) or the Data Intelligence Pipeline

### Paragraph 2: Specific Achievements (4–5 sentences)
- List 2–3 achievements with exact numbers pulled from the profile
- Map each achievement directly to a requirement or problem stated in the JD
- Use active voice: "I built...", "I automated...", "I reduced..."
- Include tech stack terms naturally — not as a list, but woven into sentences
- Do not repeat what's already on the resume — add context and business impact

### Paragraph 3: Fit + Call to Action (2–3 sentences)
- State availability (immediate) and location/visa status for UAE roles
- Reference why this specific company/role is a fit (use something specific from their JD or about pages)
- Close with a clear next step: "I'd welcome a conversation to discuss how I can contribute."

---

## Achievement Selection Guide

Choose achievements based on `role_type`:

| role_type | Primary Achievement | Secondary Achievement |
|-----------|--------------------|-----------------------|
| n8n_automation | AI Lead Qualification System (n8n + LLM + Supabase, 100% automated) | Data Intelligence Pipeline (14k+ records, 40% effort reduction) |
| rpa_uipath | UiPath RPA (OCR, eliminated data entry errors) + 48.5hr certification | Idempotent Order Processing (production-grade Python reliability) |
| data_engineering | Data Intelligence Pipeline (14k+ records, 40% reduction) | Customer Analytics AWS (S3→Lambda→Redshift, 100% automated) |
| ai_integration | Skill Tenet Conversation Engine (LLM + RAG + multilingual) | Research publication (AutoStream, IJSREM) |
| general_automation | Idempotent Order Processing (Python, air-gapped, production-grade) | AI Lead Qualification System (100% automated end-to-end) |

---

## JD Keyword Integration

Scan the job description for:
- Specific tools (e.g., "n8n", "UiPath", "Power Automate") → confirm Afsal's hands-on experience
- Business outcomes they care about (e.g., "reduce manual effort", "automate workflows") → reference matching achievement with exact numbers
- Team/culture signals (e.g., "async", "remote-first") → acknowledge briefly
- Technical challenges (e.g., "ETL pipeline", "LLM integration", "RAG") → reference matching experience

---

## Output Format

Return the cover letter as plain text, followed by a JSON metadata block:

```
[COVER LETTER TEXT]

---
METADATA
{
  "word_count": 187,
  "achievements_used": ["AI Lead Qualification", "AWS Data Pipeline"],
  "jd_keywords_used": ["n8n", "workflow automation", "LLM integration"],
  "tone": "confident",
  "hook_type": "problem_connection",
  "role_type": "n8n_automation",
  "uae_visa_mentioned": true
}
```

---

## Example Output (for reference — do not copy verbatim)

When [Company Name] set out to automate their lead qualification, the challenge wasn't just connecting tools — it was making the system reliable enough to fully replace human judgment for routing. I solved exactly that problem: an n8n + Telegram + LLM (OpenAI/Gemini) + Supabase pipeline that auto-classifies leads as Hot/Warm/Cold and handles 100% of CRM entry and follow-up without manual intervention.

Beyond lead qualification, I built a data intelligence pipeline on n8n + Supabase that processes 14,000+ records end-to-end, cutting manual reporting effort by 40%. On the infrastructure side, I designed an AWS pipeline (S3 → Lambda → Redshift) that ingests 14,000+ telecom records with complete automation and zero manual steps — the kind of reliability that makes operations teams stop worrying about the pipeline and start using it.

I'm available immediately and based in Abu Dhabi with an active UAE resident visa — no sponsorship or relocation needed. The [Role Title] at [Company Name] aligns directly with the automation depth I've been building toward. I'd welcome a conversation to discuss how I can contribute.
