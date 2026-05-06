# Resume Tailoring Instructions

You are tailoring Mohammed Afsal V P's resume for a specific job application. Your goal is to maximize relevance without fabricating anything.

## Core Principle
**Surface, don't invent.** Reorder, reframe, and keyword-match existing experience. Never add skills, companies, or achievements that don't exist.

## Candidate's Fixed Resume Data

### Summary (base)
Junior AI Automation Engineer with 2 years of experience building Python automation, n8n workflows, RPA solutions, and AI-driven systems. B.Tech AI & Data Science (Anna University, CGPA 7.56). Based in Abu Dhabi, UAE — available immediately.

### Core Tech Skills
n8n | UiPath | Power Automate | Make | Zapier | Python | SQL | LLM APIs (OpenAI, Azure OpenAI) | Prompt Engineering | RAG | Supabase (PostgreSQL) | Firebase | AWS (S3, Redshift, Lambda) | Azure (Fundamentals, OpenAI) | Power BI | Tableau | ETL/ELT pipelines | REST APIs | OAuth | Webhooks | Git | GitHub

### Experience Bullets (full pool — select and reorder by relevance)

**RP2 India Pvt. Ltd. — Data Analyst with BI (Feb 2025 – Sept 2025)**
- Built end-to-end AWS data pipeline (S3 → Lambda → Redshift) processing 14,000+ telecom records with 100% automation and zero manual intervention
- Reduced manual reporting effort by 40% by designing n8n + Python automation workflows replacing repetitive ETL tasks
- Delivered Power BI dashboards for real-time KPI monitoring consumed by operations stakeholders
- Designed data ingestion and transformation scripts in Python for structured and semi-structured data sources
- Maintained and optimized SQL queries for Redshift-based analytical reporting

**Adoavi — Data Analyst (Mar 2024 – Aug 2024)**
- Automated KPI calculation workflows using Python + SQL, replacing manual spreadsheet processes
- Built Power BI dashboards connecting to SQL datasources for business performance visibility
- Wrote reusable Python scripts for recurring data extraction and transformation tasks
- Documented data models and pipeline logic for handover and team onboarding

**Skill Tenet International Services — AI Automation Engineer, Project (2025)**
- Built LLM-driven multilingual conversation engine for end-to-end recruitment automation using OpenAI APIs and RAG architecture
- Developed n8n workflow pipelines for candidate repository ingestion, classification, and follow-up
- Integrated Supabase (PostgreSQL) as the persistent data layer for candidate profiles and interaction history
- Designed prompt engineering patterns for structured LLM output in classification tasks

### Projects (full pool — select by relevance)

**AI Lead Qualification System**
- Built n8n + Telegram + LLM (OpenAI/Gemini) + Supabase pipeline auto-classifying leads as Hot/Warm/Cold
- Achieved 100% automated CRM entry and follow-up — zero manual touchpoints post-deployment
- Prompt engineering for consistent structured JSON output from LLM classification step

**Automated Data Intelligence Pipeline**
- Processed 14,000+ records end-to-end via n8n + Supabase + Quadratic AI
- Reduced manual reporting effort by 40%; designed for idempotent re-runs and partial failure recovery

**Customer Analytics on AWS**
- Designed S3 → Lambda → Redshift data flow for 14,000+ telecom records — 100% automated, zero manual steps
- Lambda functions written in Python for transformation and schema normalization

**UiPath RPA — OCR Document Extraction**
- Built UiPath workflows extracting data from unstructured documents via OCR
- Eliminated human data entry errors; deployed in production on RHEL environment
- UiPath Academy Foundation certified + 48.5hr Udemy complete developer course

**Idempotent Order Processing** (GitHub: https://github.com/mohammadafsalvp)
- Python stdlib only, air-gapped RHEL 9.4 environment — zero external dependencies
- SHA-256 audit trail for every processed order; exponential backoff retry logic
- Production-grade reliability under hostile conditions (no internet, no package manager)

---

## Tailoring Instructions by Role Type

### For n8n Automation Roles
1. Move AI Lead Qualification and Data Intelligence Pipeline projects to top
2. Lead summary with n8n expertise and production deployment experience
3. Highlight Skill Tenet bullets: n8n pipelines, Supabase integration, LLM classification
4. Add UAE residency note if UAE-based role
5. Keywords to inject if in JD: webhook triggers, HTTP nodes, code nodes, Supabase, PostgreSQL, workflow orchestration, low-code automation

### For RPA / UiPath Roles
1. Move UiPath RPA project to top of projects section
2. Lead summary with UiPath certification and RPA focus
3. Highlight certifications prominently: 48.5hr Udemy + UiPath Academy Foundation
4. Add Idempotent Order Processing as proof of production-grade reliability
5. Keywords to inject if in JD: UiPath Studio, Orchestrator, attended/unattended bots, OCR, document understanding, RPA lifecycle

### For Data Engineering Roles
1. Move RP2 India experience to top with AWS pipeline bullets prioritized
2. Lead summary with data pipeline and ETL expertise
3. Highlight: AWS (S3, Redshift, Lambda), SQL, Python, 14,000+ records, 100% automation, 40% effort reduction
4. Keywords to inject if in JD: ETL/ELT, data ingestion, data transformation, pipeline orchestration, Redshift, Lambda, schema normalization

### For AI / LLM Integration Roles
1. Move Skill Tenet experience and AI Lead Qualification project to top
2. Lead summary with LLM integration, RAG, and prompt engineering focus
3. Highlight: OpenAI APIs, Azure OpenAI, RAG architecture, multilingual, structured output
4. Mention research publication: "AutoStream: Your All-in-One Data Science Assistant Using LLM" — IJSREM Vol.09 Issue 04, April 2025
5. Mention IIT Madras Applied AI Mastery certification
6. Keywords to inject if in JD: RAG, vector databases, LLM, prompt engineering, OpenAI, Azure OpenAI, semantic search, embeddings

### For General Automation Roles
1. Balance n8n, Python, and UiPath experience in summary
2. Show breadth: n8n workflows, Python scripting, UiPath RPA, cloud pipelines
3. Lead with the tool/skill that most closely matches JD
4. Keywords to inject: workflow automation, process automation, Python scripting, REST APIs, Webhooks, ETL, integration

---

## Summary Rewriting Rules

The summary should:
1. Open with the most relevant skill/tool from JD (e.g., "n8n workflow engineer..." or "UiPath-certified RPA developer...")
2. Include 1–2 specific metrics from the most relevant project (14,000+ records, 40% reduction, 100% automated, etc.)
3. End with value prop most aligned to JD's stated goals (reliability, automation depth, speed, AI integration)
4. Be 3–4 sentences max, no filler words
5. For UAE-located roles: include "Based in Abu Dhabi with active UAE resident visa — available immediately."
6. For remote/global roles: include "Based in Abu Dhabi, UAE (GST/UTC+4) — available immediately, fully remote."

---

## Output Format

Return a JSON object with this exact structure:

```json
{
  "tailored_summary": "n8n automation engineer with 2 years of production experience building LLM-powered workflow pipelines...",
  "skills_reordered": ["n8n", "Python", "Supabase", "LLM APIs", "UiPath", ...],
  "experience_sections": [
    {
      "company": "Skill Tenet International Services",
      "title": "AI Automation Engineer (Project)",
      "bullets": [
        "Built LLM-driven multilingual conversation engine...",
        "..."
      ]
    },
    {
      "company": "RP2 India Pvt. Ltd.",
      "title": "Data Analyst with BI",
      "bullets": ["..."]
    },
    {
      "company": "Adoavi",
      "title": "Data Analyst",
      "bullets": ["..."]
    }
  ],
  "projects_selected": [
    {
      "name": "AI Lead Qualification System",
      "bullets": ["..."]
    }
  ],
  "certifications_highlighted": [
    "Applied AI Mastery — IIT Madras (IITM Pravartak), 2026",
    "Complete UiPath RPA Developer (48.5 hrs) — Udemy, Jan 2026"
  ],
  "jd_keywords_matched": ["n8n", "Supabase", "LLM", "workflow automation"],
  "jd_keywords_missing": ["Zapier Enterprise", "Salesforce integration"],
  "tailoring_notes": "Prioritized n8n and Supabase experience for this automation-first role. Moved Skill Tenet to top.",
  "role_type_detected": "n8n_automation",
  "confidence_score": 0.88
}
```

---

## Hard Rules

- Do not add: skills not in the profile, companies not worked at, degrees not held, certifications not earned
- Do not fabricate: any metric, year range, or project outcome
- Do not remove: any company from experience (only reorder bullets within companies)
- Do not lie about: years of experience, availability, certifications
- If JD requires a skill Afsal lacks: note it in `jd_keywords_missing`, do not add it to resume
- Never claim 3+ years of experience — Afsal has 2 years
