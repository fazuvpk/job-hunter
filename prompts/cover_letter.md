# Cover Letter Generation Prompt

You are writing a cover letter for Fazil Kunhamed, a senior software developer with 10 years of experience.

## Candidate Profile (for reference)
- **Name:** Fazil Kunhamed
- **Email:** fazil.kunhamed@gmail.com
- **Stack:** Angular 14–19, .NET Core, Web API, Entity Framework, TypeScript, Node.js, SQL Server, Azure, AWS
- **Key achievements:**
  - Oops AppLock Android: 7.7M+ downloads, featured on LifeHacker
  - Samsung SDS: $45K revenue in 6 months, 20% cloud cost cut, PII encryption of 20M+ records in 3 min
  - ADNOC: Angular 14→19 migration, 55% bundle reduction, 33% API improvement
  - Skill Tenet: Three.js 3D globe, GSAP animations, Vite build pipeline

---

## Inputs You Will Receive

- `job_title`: The role title
- `company_name`: The company name
- `job_description`: Full job description text
- `role_type`: One of: angular_frontend, dotnet_backend, full_stack, mobile, enterprise, startup, uae_onsite
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

---

## Structure

### Paragraph 1: The Hook (3–4 sentences)

**For `uae_onsite` roles (UAE on-site / hybrid):** Lead with the personal UAE connection before pivoting to technical fit.
- Open with: Fazil is actively relocating to UAE — wife is already UAE-based, strong personal motivation, can begin immediately upon visa processing.
- Then pivot to the most relevant technical project for their JD.
- Example hook: "I'm actively relocating to the UAE — my wife is already based there, and I have every personal reason to make this move quickly. I require employer visa sponsorship, and I'm ready to start the process as soon as an offer is in place. When [Company] was looking for someone who could [solve their specific problem], my work at [relevant project]..."

**For all other role types:** Open with a specific connection between one of Fazil's most relevant projects and a problem the company is clearly trying to solve.
- Reference the company by name and what they're building
- Do not summarize Fazil's career — get straight to the point of relevance
- Examples by role type:
  - **Angular frontend role:** Reference the ADNOC migration (Angular 14→19, 55% bundle reduction) if they're dealing with legacy Angular or performance
  - **Enterprise/backend:** Reference Samsung SDS ($45K revenue, 20M+ PII records encrypted)
  - **Startup/consumer:** Reference Oops AppLock (7.7M downloads) to show product sense and scale
  - **Creative/marketing frontend:** Reference Skill Tenet (Three.js globe, GSAP)
  - **Full-stack:** Reference the combination most relevant to their JD

### Paragraph 2: Specific Achievements (4–5 sentences)
- List 2–3 achievements with exact numbers pulled from the profile
- Map each achievement directly to a requirement or problem stated in the JD
- Use active voice: "I reduced...", "I built...", "I led..."
- Include tech stack terms naturally — not as a list, but woven into sentences
- Do not repeat what's already on the resume — add context and business impact

### Paragraph 3: Fit + Call to Action (2–3 sentences)

**For `uae_onsite` roles:** Acknowledge relocation readiness, visa sponsorship requirement, and personal connection to UAE.
- State that relocation to UAE is the active goal, wife is UAE-based, and visa sponsorship is required
- Reference why this specific company/role is a fit (use something specific from their JD or about pages)
- Close with a clear next step: "I'd welcome a conversation to discuss how I can contribute — and to outline a realistic visa timeline."

**For remote roles:** Keep existing structure.
- State remote availability and immediate start
- Reference why this specific company/role is a fit
- Close: "I'd welcome a conversation to discuss how I can contribute."

---

## Achievement Selection Guide

Choose achievements based on `role_type`:

| role_type | Primary Achievement | Secondary Achievement |
|-----------|--------------------|-----------------------|
| angular_frontend | ADNOC (Angular 19 migration, 55% bundle) | Skill Tenet (Three.js, GSAP, Vite) |
| dotnet_backend | Samsung SDS (PII encryption, 20M records, cloud cost) | Any .NET architecture work |
| full_stack | Samsung SDS + ADNOC combo | Oops AppLock for product sense |
| mobile | Oops AppLock (7.7M downloads, LifeHacker feature) | Samsung SDS for enterprise credibility |
| enterprise | Samsung SDS ($45K revenue, 20% cost reduction) | ADNOC for large-scale migration |
| startup | Oops AppLock (7.7M downloads, scrappy indie success) | Skill Tenet (modern stack, rapid build) |
| uae_onsite | ADNOC (UAE enterprise client — direct relevance) | Samsung SDS for enterprise credibility |

---

## JD Keyword Integration

Scan the job description for:
- Specific frameworks/versions (e.g., "Angular 17", "EF Core 8") → use exact version in letter
- Business outcomes they care about (e.g., "performance", "scalability") → reference matching achievement
- Team/culture signals (e.g., "async", "remote-first") → acknowledge briefly
- Technical challenges (e.g., "legacy migration", "high-traffic") → reference matching experience
- UAE-specific signals (e.g., "visa sponsorship provided", "relocation package") → acknowledge and confirm readiness

---

## Output Format

Return the cover letter as plain text, followed by a JSON metadata block:

```
[COVER LETTER TEXT]

---
METADATA
{
  "word_count": 187,
  "achievements_used": ["ADNOC migration", "Samsung SDS PII"],
  "jd_keywords_used": ["Angular 19", "performance optimization", "remote-first"],
  "tone": "confident",
  "hook_type": "uae_personal_connection",
  "role_type": "uae_onsite"
}
```

---

## Example Output — UAE On-Site Role (for reference — do not copy verbatim)

I'm actively relocating to the UAE — my wife is already based there, and I have every personal reason to make this move as quickly as possible. I require employer visa sponsorship, and I'm ready to begin that process immediately upon an offer. When Acme UAE needed to modernize their Angular frontend while keeping a live enterprise user base intact, that's precisely the problem I solved at ADNOC: a full Angular 14 to 19 migration delivering a 55% bundle size reduction and 33% API performance improvement.

At Samsung SDS, I delivered $45,000 in new revenue within 6 months while simultaneously reducing cloud infrastructure costs by 20% — the kind of dual outcome that requires both technical depth and commercial awareness. The PII encryption pipeline I built there processed 20 million+ records in under 3 minutes using Azure Service Bus and parallel processing. Earlier, building Oops AppLock from scratch to 7.7 million downloads taught me how code-level performance decisions translate directly into user retention at scale.

The Senior Full Stack Developer role at Acme UAE aligns directly with the scale of work I'm targeting next. I'd welcome a conversation about how I can contribute — and to walk through a realistic visa and onboarding timeline.

---

## Example Output — Remote Role (for reference — do not copy verbatim)

When [Company Name] decided to modernize their Angular frontend, the challenge wasn't just upgrading versions — it was doing it without disrupting an active user base or bloating the bundle further. At ADNOC, I led exactly that migration: Angular 14 to 19, resulting in a 55% bundle size reduction and a 33% improvement in API response times across a complex enterprise codebase.

In that project, I implemented lazy loading across 40+ feature modules using standalone components and replaced legacy RxJS patterns with signals-based state management. At Samsung SDS, I delivered $45,000 in new revenue within 6 months while simultaneously reducing cloud infrastructure costs by 20% — the kind of dual outcome that requires both technical depth and commercial awareness. Earlier, building Oops AppLock from scratch to 7.7 million downloads taught me how performance and UX decisions at the code level translate directly into retention and store rankings.

I'm available immediately and fully remote from India. The [Role Title] at [Company Name] aligns directly with the scale and ambition I'm looking for next. I'd welcome a conversation to explore how I can contribute.
