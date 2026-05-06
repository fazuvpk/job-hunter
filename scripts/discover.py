#!/usr/bin/env python3
"""Job discovery script for job-hunter pipeline."""

import json
import sqlite3
import re
import sys
import hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "jobs.db"
BLACKLIST_PATH = ROOT / "config" / "blacklist.json"
SEARCH_PATH = ROOT / "config" / "search.json"

def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    # Ensure schema exists
    schema = (ROOT / "data" / "schema.sql").read_text()
    db.executescript(schema)
    db.commit()
    return db

def load_config():
    with open(SEARCH_PATH) as f:
        return json.load(f)

def load_blacklist():
    with open(BLACKLIST_PATH) as f:
        return json.load(f)

def is_blacklisted(title, company, description, blacklist):
    text = f"{title} {company} {description or ''}".lower()
    all_patterns = (
        blacklist["blacklisted_patterns"].get("title_patterns", []) +
        blacklist["blacklisted_patterns"].get("description_patterns", []) +
        blacklist["blacklisted_patterns"].get("company_type_patterns", []) +
        blacklist["blacklisted_patterns"].get("location_patterns", [])
    )
    for pattern in all_patterns:
        if pattern.lower() in text:
            return True, pattern
    for company_name in blacklist.get("blacklisted_companies", []):
        if company_name.lower() in company.lower():
            return True, f"blacklisted company: {company_name}"
    return False, None

def make_external_id(job_url, title, company):
    key = f"{job_url or ''}{title}{company}".encode()
    return hashlib.md5(key).hexdigest()

def salary_to_monthly_usd(min_amount, max_amount, currency, interval):
    """Rough conversion to monthly USD."""
    if not min_amount and not max_amount:
        return None
    amount = min_amount or max_amount
    if not amount:
        return None
    # Normalize to monthly
    if interval == "yearly" or interval == "annual":
        amount = amount / 12
    elif interval == "hourly":
        amount = amount * 160  # ~40h/week * 4 weeks
    elif interval == "weekly":
        amount = amount * 4
    # Currency conversion (rough)
    rates = {"USD": 1, "EUR": 1.1, "GBP": 1.25, "CAD": 0.74, "AUD": 0.65, "INR": 0.012}
    rate = rates.get(currency or "USD", 1)
    return int(amount * rate)

def search_jobs(title, config):
    """Search jobs using python-jobspy."""
    import jobspy

    # Glassdoor doesn't support worldwide search — exclude it
    worldwide_supported = {"linkedin", "indeed", "zip_recruiter", "google"}
    site_map = {
        "linkedin": "linkedin",
        "indeed": "indeed",
        "zip_recruiter": "zip_recruiter",
        "google": "google",
    }
    sites = [site_map[s] for s in config["sites"] if s in site_map and s in worldwide_supported]

    print(f"  Searching: '{title}' on {', '.join(sites)}...")
    try:
        jobs_df = jobspy.scrape_jobs(
            site_name=sites,
            search_term=title,
            results_wanted=config["results_per_title"],
            is_remote=True,
            country_indeed="worldwide",
        )
        return jobs_df
    except Exception as e:
        print(f"  ERROR searching '{title}': {e}")
        return None

def score_job(job_data):
    """Score a job using Claude API via subprocess to avoid import issues."""
    import subprocess, json

    prompt = f"""You are scoring a job for Fazil Kunhamed using the rubric below. Return ONLY valid JSON, no markdown.

Job:
- Title: {job_data.get('title', '')}
- Company: {job_data.get('company', '')}
- Location: {job_data.get('location', '')}
- Salary: {job_data.get('salary_raw', 'Not stated')}
- Remote: {job_data.get('remote', 'Unknown')}
- Description: {str(job_data.get('description', ''))[:3000]}

Scoring dimensions (return JSON with these exact keys):
{{
  "score": <0-100>,
  "breakdown": {{
    "role_match": <0-20>,
    "tech_stack_overlap": <0-20>,
    "remote_compatibility": <0-15>,
    "seniority_alignment": <0-10>,
    "salary_signal": <0-10>,
    "company_quality": <0-10>,
    "growth_opportunity": <0-5>,
    "application_complexity": <0-5>,
    "timezone_fit": <0-3>,
    "visa_clarity": <0-2>
  }},
  "summary": "<2-3 sentence summary>",
  "green_flags": ["<flag1>", "<flag2>"],
  "red_flags": ["<flag1>"],
  "recommendation": "<APPLY|REVIEW|SKIP|AUTO_SKIP>",
  "confidence": "<high|medium|low>"
}}

Rules:
- APPLY if score >= 80, REVIEW if 60-79, SKIP if 35-59, AUTO_SKIP if < 35
- Score 0 + AUTO_SKIP for: UAE relocation, US citizens only, junior role, salary < $2000/month, security clearance
- Candidate stack: Angular 14-19, .NET Core, TypeScript, Node.js, SQL Server, React, Azure, AWS
- Must be fully remote (Kerala, India based)
- Salary floor: $4000/month USD"""

    try:
        result = subprocess.run(
            ["claude", "-p", prompt, "--model", "claude-haiku-4-5-20251001"],
            capture_output=True, text=True, timeout=30
        )
        output = result.stdout.strip()
        # Extract JSON from output
        json_match = re.search(r'\{[\s\S]*\}', output)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"    Score error: {e}")

    # Fallback: basic heuristic score
    return basic_score(job_data)

def basic_score(job_data):
    """Fallback heuristic scorer when Claude API unavailable."""
    title = (job_data.get('title') or '').lower()
    desc = (job_data.get('description') or '').lower()
    text = title + ' ' + desc

    score = 0
    breakdown = {}

    # Role match (0-20)
    if any(x in title for x in ['senior full stack', 'lead full stack', 'senior angular', 'senior .net']):
        breakdown['role_match'] = 20
    elif any(x in title for x in ['full stack', 'angular', '.net', 'senior software']):
        breakdown['role_match'] = 14
    elif any(x in title for x in ['software engineer', 'developer']):
        breakdown['role_match'] = 8
    else:
        breakdown['role_match'] = 3

    # Tech stack (0-20)
    skills = ['angular', '.net', 'typescript', 'node', 'sql server', 'entity framework', 'react', 'azure', 'aws', 'cqrs', 'rxjs', 'signalr', 'web api', 'microservices']
    matches = sum(1 for s in skills if s in text)
    if matches >= 8: breakdown['tech_stack_overlap'] = 19
    elif matches >= 5: breakdown['tech_stack_overlap'] = 15
    elif matches >= 3: breakdown['tech_stack_overlap'] = 11
    elif matches >= 1: breakdown['tech_stack_overlap'] = 7
    else: breakdown['tech_stack_overlap'] = 2

    # Remote (0-15)
    if any(x in text for x in ['fully remote', 'remote-first', 'work from anywhere', 'async-first', 'remote first']):
        breakdown['remote_compatibility'] = 15
    elif any(x in text for x in ['remote ok', 'remote friendly', 'remote possible', 'distributed team']):
        breakdown['remote_compatibility'] = 10
    elif 'hybrid' in text:
        breakdown['remote_compatibility'] = 5
    elif job_data.get('remote'):
        breakdown['remote_compatibility'] = 10
    else:
        breakdown['remote_compatibility'] = 3

    # Seniority (0-10)
    if any(x in title for x in ['senior', 'lead', 'principal', 'staff']):
        breakdown['seniority_alignment'] = 10
    elif any(x in title for x in ['mid', '5+', 'iii']):
        breakdown['seniority_alignment'] = 5
    else:
        breakdown['seniority_alignment'] = 2

    # Salary (0-10)
    salary_min = job_data.get('salary_min_usd')
    if salary_min and salary_min >= 4000:
        breakdown['salary_signal'] = 10
    elif salary_min and salary_min >= 2000:
        breakdown['salary_signal'] = 3
    else:
        breakdown['salary_signal'] = 6  # unknown, assume possible

    # Company quality (0-10) - default unknown
    breakdown['company_quality'] = 5

    # Growth (0-5)
    if any(x in text for x in ['architecture', 'tech lead', 'mentorship', 'ownership', 'system design']):
        breakdown['growth_opportunity'] = 5
    else:
        breakdown['growth_opportunity'] = 3

    # Application complexity (0-5)
    source = (job_data.get('source') or '').lower()
    if 'linkedin' in source:
        breakdown['application_complexity'] = 5
    else:
        breakdown['application_complexity'] = 3

    # Timezone (0-3)
    breakdown['timezone_fit'] = 3  # assume async/global

    # Visa (0-2)
    if any(x in text for x in ['visa sponsorship', 'global candidates', 'international']):
        breakdown['visa_clarity'] = 2
    elif any(x in text for x in ['us citizens only', 'authorized to work in us', 'no sponsorship']):
        breakdown['visa_clarity'] = 0
    else:
        breakdown['visa_clarity'] = 1

    score = sum(breakdown.values())

    if score >= 80:
        rec = 'APPLY'
    elif score >= 60:
        rec = 'REVIEW'
    elif score >= 35:
        rec = 'SKIP'
    else:
        rec = 'AUTO_SKIP'

    return {
        'score': score,
        'breakdown': breakdown,
        'summary': f"Heuristic score. Title: {job_data.get('title')}. {matches} core skills matched.",
        'green_flags': [],
        'red_flags': [],
        'recommendation': rec,
        'confidence': 'low'
    }

def upsert_daily_stats(db, discovered=0, scored=0):
    today = datetime.now().strftime('%Y-%m-%d')
    db.execute("""
        INSERT INTO daily_stats (date, discovered, scored) VALUES (?, ?, ?)
        ON CONFLICT(date) DO UPDATE SET
            discovered = discovered + excluded.discovered,
            scored = scored + excluded.scored
    """, (today, discovered, scored))
    db.commit()

def main():
    config = load_config()
    blacklist = load_blacklist()
    db = get_db()

    titles = config["titles"]
    threshold_review = config["score_threshold_for_review"]
    threshold_skip = config["score_threshold_for_auto_skip"]

    total_found = 0
    total_new = 0
    total_scored = 0
    total_skipped = 0
    above_threshold = 0

    for title in titles:
        print(f"\n[{titles.index(title)+1}/{len(titles)}] '{title}'")
        jobs_df = search_jobs(title, config)

        if jobs_df is None or jobs_df.empty:
            print(f"  No results.")
            continue

        batch_found = len(jobs_df)
        total_found += batch_found
        print(f"  Found {batch_found} listings")

        for _, row in jobs_df.iterrows():
            job_url = str(row.get('job_url', '') or '')
            job_title = str(row.get('title', '') or '')
            company = str(row.get('company', '') or '')
            location = str(row.get('location', '') or '')
            description = str(row.get('description', '') or '')
            source = str(row.get('site', '') or '')

            # Salary
            salary_min_raw = row.get('min_amount')
            salary_max_raw = row.get('max_amount')
            currency = str(row.get('currency', '') or 'USD')
            interval = str(row.get('interval', '') or 'yearly')
            salary_raw = ''
            if salary_min_raw or salary_max_raw:
                salary_raw = f"{currency} {salary_min_raw or '?'}-{salary_max_raw or '?'} {interval}"

            salary_min_usd = salary_to_monthly_usd(
                float(salary_min_raw) if salary_min_raw else None,
                float(salary_max_raw) if salary_max_raw else None,
                currency, interval
            )

            is_remote = bool(row.get('is_remote', False))

            external_id = make_external_id(job_url, job_title, company)

            # Skip duplicates
            existing = db.execute("SELECT id FROM jobs WHERE external_id = ?", (external_id,)).fetchone()
            if existing:
                continue

            # Blacklist check
            blacklisted, bl_reason = is_blacklisted(job_title, company, description, blacklist)
            if blacklisted:
                total_skipped += 1
                print(f"  SKIP (blacklisted: {bl_reason}): {job_title} @ {company}")
                continue

            total_new += 1

            # Score
            print(f"  Scoring: {job_title} @ {company}...", end=' ', flush=True)
            job_data = {
                'title': job_title,
                'company': company,
                'location': location,
                'salary_raw': salary_raw,
                'salary_min_usd': salary_min_usd,
                'remote': is_remote,
                'description': description,
                'source': source,
            }

            scoring = score_job(job_data)
            score = scoring.get('score', 0)
            recommendation = scoring.get('recommendation', 'SKIP')
            total_scored += 1

            if score >= threshold_review:
                above_threshold += 1

            status = 'pending'
            if recommendation == 'AUTO_SKIP' or score < threshold_skip:
                status = 'skipped'

            print(f"score={score} → {recommendation}")

            # Insert into DB
            db.execute("""
                INSERT OR IGNORE INTO jobs
                (external_id, title, company, location, salary_raw, salary_min_usd,
                 remote, url, description, source, score, score_breakdown,
                 score_summary, red_flags, green_flags, recommendation, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                external_id, job_title, company, location, salary_raw, salary_min_usd,
                is_remote, job_url, description[:10000], source, score,
                json.dumps(scoring.get('breakdown', {})),
                scoring.get('summary', ''),
                json.dumps(scoring.get('red_flags', [])),
                json.dumps(scoring.get('green_flags', [])),
                recommendation, status
            ))
            db.commit()

        # Update daily stats per title batch
        upsert_daily_stats(db, discovered=batch_found)

    upsert_daily_stats(db, scored=total_scored)

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISCOVERY COMPLETE
  Total found:         {total_found}
  New (not duplicate): {total_new}
  Scored:              {total_scored}
  Above threshold(≥{threshold_review}): {above_threshold}
  Auto-skipped:        {total_skipped + (total_scored - above_threshold - (total_new - total_scored))}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

if __name__ == "__main__":
    main()
