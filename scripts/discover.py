#!/usr/bin/env python3
"""Job discovery script for job-hunter pipeline.

Runs 3 location passes per title:
  1. Abu Dhabi UAE
  2. Dubai UAE
  3. Remote (global)
"""

import json
import sqlite3
import re
import sys
import time
import random
import hashlib
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "jobs.db"
BLACKLIST_PATH = ROOT / "config" / "blacklist.json"
SEARCH_PATH = ROOT / "config" / "search.json"
SCORER_PATH = ROOT / "prompts" / "scorer.md"

OLLAMA_BASE_URL = "http://100.110.228.115:11434"
OLLAMA_MODEL = "hermes3:latest"
OLLAMA_TIMEOUT = 300
_OLLAMA_AVAILABLE = None

LOCATION_PASSES = [
    {
        "label": "Abu Dhabi UAE",
        "location": "Abu Dhabi",
        "is_remote": False,
        "country_indeed": "united arab emirates",
    },
    {
        "label": "Dubai UAE",
        "location": "Dubai",
        "is_remote": False,
        "country_indeed": "united arab emirates",
    },
    {
        "label": "Remote",
        "location": "Remote",
        "is_remote": True,
        "country_indeed": None,
    },
]

# Sites that support non-US locations reliably
SUPPORTED_SITES = ["linkedin", "indeed"]


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    schema = (ROOT / "data" / "schema.sql").read_text()
    db.executescript(schema)
    db.commit()
    return db


def load_config():
    return json.loads(SEARCH_PATH.read_text())


def load_blacklist():
    return json.loads(BLACKLIST_PATH.read_text())


def is_blacklisted(title, company, description, blacklist):
    text = f"{title} {company} {description or ''}".lower()
    patterns = (
        blacklist["blacklisted_patterns"].get("title_patterns", [])
        + blacklist["blacklisted_patterns"].get("description_patterns", [])
        + blacklist["blacklisted_patterns"].get("company_type_patterns", [])
        + blacklist["blacklisted_patterns"].get("location_patterns", [])
    )
    for p in patterns:
        if p.lower() in text:
            return True, p
    for c in blacklist.get("blacklisted_companies", []):
        if c.lower() in company.lower():
            return True, f"blacklisted company: {c}"
    return False, None


def make_external_id(job_url, title, company):
    key = f"{job_url or ''}{title}{company}".encode()
    return hashlib.md5(key).hexdigest()


def _check_ollama() -> bool:
    global _OLLAMA_AVAILABLE
    if _OLLAMA_AVAILABLE is not None:
        return _OLLAMA_AVAILABLE
    try:
        import urllib.request
        with urllib.request.urlopen(f"{OLLAMA_BASE_URL}/api/tags", timeout=4) as r:
            _OLLAMA_AVAILABLE = r.status == 200
    except Exception:
        _OLLAMA_AVAILABLE = False
    label = "Ollama rig-2060" if _OLLAMA_AVAILABLE else "Claude CLI (fallback)"
    print(f"  [scorer] backend -> {label}", file=sys.stderr)
    return _OLLAMA_AVAILABLE


def _score_via_ollama(prompt: str) -> str:
    import urllib.request
    body = json.dumps({
        "model": OLLAMA_MODEL, "prompt": prompt,
        "stream": False, "options": {"temperature": 0.1, "num_predict": 300},
    }).encode()
    req = urllib.request.Request(
        f"{OLLAMA_BASE_URL}/api/generate", data=body,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT) as r:
        return json.loads(r.read()).get("response", "")


def salary_to_monthly_usd(min_amount, max_amount, currency, interval):
    import math
    amount = min_amount or max_amount
    if not amount:
        return None
    try:
        amount = float(amount)
    except Exception:
        return None
    if math.isnan(amount):
        return None
    interval = (interval or "").lower()
    if "year" in interval or "annual" in interval:
        amount /= 12
    elif "hour" in interval:
        amount *= 160
    elif "week" in interval:
        amount *= 4.33
    elif "day" in interval:
        amount *= 21
    rates = {"USD": 1, "EUR": 1.09, "GBP": 1.27, "CAD": 0.74, "AUD": 0.65,
             "AED": 0.272, "INR": 0.012, "SAR": 0.267}
    rate = rates.get((currency or "USD").upper(), 1.0)
    return int(amount * rate)


def search_jobs(title, pass_cfg, results_wanted):
    import jobspy
    import warnings
    warnings.filterwarnings("ignore")

    kwargs = dict(
        site_name=SUPPORTED_SITES,
        search_term=title,
        location=pass_cfg["location"],
        results_wanted=results_wanted,
        hours_old=336,  # 14 days
        is_remote=pass_cfg["is_remote"],
    )
    if pass_cfg["country_indeed"]:
        kwargs["country_indeed"] = pass_cfg["country_indeed"]

    try:
        return jobspy.scrape_jobs(**kwargs)
    except Exception as e:
        print(f"  [WARN] scrape error: {e}", file=sys.stderr)
        return None


def score_job(job_data, scorer_prompt):
    'Score a job via Ollama on rig-2060 (Tailscale); fall back to Claude CLI.'
    import subprocess
    parts = [
        f"Title: {job_data.get('title', '')}",
        f"Company: {job_data.get('company', '')}",
        f"Location: {job_data.get('location', '')}",
        f"Salary: {job_data.get('salary_raw') or 'Not stated'}",
        f"Remote: {job_data.get('remote', 'Unknown')}",
        f"Source: {job_data.get('source', '')}",
        "Description:",
        str(job_data.get('description', ''))[:3000],
    ]
    job_block = "\n".join(parts).strip()
    prompt = (
        scorer_prompt + "\n\n---\n## Job to Score\n" + job_block +
        "\n\nReturn ONLY the JSON object described above. No markdown fences, no explanation."
    )

    if _check_ollama():
        try:
            out = _score_via_ollama(prompt)
            m = re.search(r'\{[\s\S]*\}', out)
            if m:
                return json.loads(m.group())
            print("    [scorer] Ollama no JSON - falling back", file=sys.stderr)
        except Exception as e:
            print(f"    [scorer] Ollama error: {e} - falling back", file=sys.stderr)
            global _OLLAMA_AVAILABLE
            _OLLAMA_AVAILABLE = False

    try:
        r = subprocess.run(
            ["claude", "-p", "-", "--model", "claude-haiku-4-5-20251001"],
            input=prompt, capture_output=True, text=True, timeout=60,
        )
        out = r.stdout.strip()
        m = re.search(r'\{[\s\S]*\}', out)
        if m:
            return json.loads(m.group())
    except Exception as e:
        print(f"    [scorer error] {e}", file=sys.stderr)

    return basic_score(job_data)


def basic_score(job_data):
    """Fallback heuristic scorer."""
    title = (job_data.get("title") or "").lower()
    desc = (job_data.get("description") or "").lower()
    location = (job_data.get("location") or "").lower()
    text = title + " " + desc

    bd = {}

    # Role match
    if any(x in title for x in ["senior full stack", "lead full stack", "senior angular", "senior .net"]):
        bd["role_match"] = 20
    elif any(x in title for x in ["full stack", "angular", ".net", "senior software"]):
        bd["role_match"] = 14
    elif any(x in title for x in ["software engineer", "developer"]):
        bd["role_match"] = 8
    else:
        bd["role_match"] = 3

    # Tech stack
    skills = ["angular", ".net", "typescript", "node", "sql server", "entity framework",
              "react", "azure", "aws", "cqrs", "rxjs", "signalr", "web api", "microservices"]
    matches = sum(1 for s in skills if s in text)
    if matches >= 8: bd["tech_stack_overlap"] = 19
    elif matches >= 5: bd["tech_stack_overlap"] = 15
    elif matches >= 3: bd["tech_stack_overlap"] = 11
    elif matches >= 1: bd["tech_stack_overlap"] = 7
    else: bd["tech_stack_overlap"] = 2

    # Location fit — UAE = 15
    is_uae = any(x in location for x in ["abu dhabi", "dubai", "sharjah", "uae", "united arab"])
    if is_uae:
        bd["location_fit"] = 15
    elif any(x in text for x in ["fully remote", "remote-first", "work from anywhere", "async-first"]):
        bd["location_fit"] = 15
    elif any(x in text for x in ["remote ok", "remote friendly", "distributed team"]):
        bd["location_fit"] = 10
    elif "hybrid" in text:
        bd["location_fit"] = 5
    elif job_data.get("remote"):
        bd["location_fit"] = 10
    else:
        bd["location_fit"] = 3

    # Seniority
    if any(x in title for x in ["senior", "lead", "principal", "staff"]):
        bd["seniority_alignment"] = 10
    elif any(x in title for x in ["mid", "iii"]):
        bd["seniority_alignment"] = 5
    else:
        bd["seniority_alignment"] = 2

    # Salary
    salary_min = job_data.get("salary_min_usd")
    if salary_min and salary_min >= 4000:
        bd["salary_signal"] = 10
    elif salary_min and salary_min >= 2000:
        bd["salary_signal"] = 3
    else:
        bd["salary_signal"] = 6

    bd["company_quality"] = 5
    bd["growth_opportunity"] = 5 if any(x in text for x in ["architecture", "tech lead", "mentorship", "system design"]) else 3
    bd["application_complexity"] = 5 if "linkedin" in (job_data.get("source") or "").lower() else 3
    bd["timezone_fit"] = 3 if (is_uae or "gulf" in text or "gst" in text or not any(x in text for x in ["us hours only", "est only"])) else 1
    bd["visa_clarity"] = 2 if any(x in text for x in ["visa sponsorship", "global candidates", "international"]) else (0 if any(x in text for x in ["us citizens only", "no sponsorship"]) else 1)

    score = sum(bd.values())
    if score >= 80: rec = "APPLY"
    elif score >= 60: rec = "REVIEW"
    elif score >= 35: rec = "SKIP"
    else: rec = "AUTO_SKIP"

    uae_role = is_uae
    if uae_role and score >= 50 and rec == "SKIP":
        rec = "REVIEW"

    return {
        "score": score, "uae_role": uae_role, "breakdown": bd,
        "summary": f"Heuristic score ({matches} core skills matched). {'UAE role.' if uae_role else ''}",
        "green_flags": (["UAE-based role"] if uae_role else []),
        "red_flags": [],
        "recommendation": rec,
        "confidence": "low",
    }


def upsert_daily_stats(db, discovered=0, scored=0):
    today = datetime.now().strftime("%Y-%m-%d")
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
    scorer_prompt = SCORER_PATH.read_text()

    titles = config["titles"]
    results_per_title = config["results_per_title"]
    threshold_review = config["score_threshold_for_review"]
    threshold_auto_skip = config["score_threshold_for_auto_skip"]

    # Track seen URLs across all passes to deduplicate
    seen_urls: set[str] = set()
    existing_ids: set[str] = {
        row[0] for row in db.execute("SELECT external_id FROM jobs").fetchall()
    }

    total_found = 0
    total_new = 0
    total_scored = 0
    total_bl_skipped = 0
    above_threshold = 0

    for idx, title in enumerate(titles, 1):
        print(f"\n[{idx}/{len(titles)}] '{title}'")

        for pass_cfg in LOCATION_PASSES:
            print(f"  Pass: {pass_cfg['label']} ...", end=" ", flush=True)
            df = search_jobs(title, pass_cfg, results_per_title)

            if df is None or df.empty:
                print("0 results")
                time.sleep(random.uniform(2, 4))
                continue

            pass_new = 0
            total_found += len(df)

            for _, row in df.iterrows():
                job_url = str(row.get("job_url") or row.get("job_url_direct") or "")
                if not job_url or job_url in seen_urls:
                    continue
                seen_urls.add(job_url)

                job_title = str(row.get("title") or "")
                company = str(row.get("company") or "")
                if company.lower() in ("nan", "none", ""):
                    company = "Unknown"
                location = str(row.get("location") or "")
                description = str(row.get("description") or "")
                source = str(row.get("site") or "")
                is_remote = bool(row.get("is_remote") or pass_cfg["is_remote"])

                min_amt = row.get("min_amount")
                max_amt = row.get("max_amount")
                currency = str(row.get("currency") or "USD")
                interval = str(row.get("interval") or "yearly")
                salary_raw = f"{currency} {min_amt or '?'}–{max_amt or '?'} {interval}" if (min_amt or max_amt) else ""
                salary_min_usd = salary_to_monthly_usd(
                    float(min_amt) if min_amt else None,
                    float(max_amt) if max_amt else None,
                    currency, interval
                )

                external_id = make_external_id(job_url, job_title, company)
                if external_id in existing_ids:
                    continue
                existing_ids.add(external_id)

                bl, bl_reason = is_blacklisted(job_title, company, description, blacklist)
                if bl:
                    total_bl_skipped += 1
                    continue

                total_new += 1
                pass_new += 1

                job_data = {
                    "title": job_title, "company": company, "location": location,
                    "salary_raw": salary_raw, "salary_min_usd": salary_min_usd,
                    "remote": is_remote, "description": description, "source": source,
                }

                print(f"\n    Scoring: {job_title[:50]} @ {company[:30]}...", end=" ", flush=True)
                scoring = score_job(job_data, scorer_prompt)
                score = scoring.get("score", 0)
                recommendation = scoring.get("recommendation", "SKIP")
                uae_role = scoring.get("uae_role", False)
                total_scored += 1

                # UAE override: surface 50+ UAE roles for review
                if uae_role and score >= 50 and recommendation == "SKIP":
                    recommendation = "REVIEW"

                status = "pending"
                if recommendation == "AUTO_SKIP" or score < threshold_auto_skip:
                    status = "skipped"

                if score >= threshold_review:
                    above_threshold += 1

                notes = "UAE PRIORITY" if uae_role else None

                db.execute("""
                    INSERT OR IGNORE INTO jobs
                    (external_id, title, company, location, salary_raw, salary_min_usd,
                     remote, url, description, source, score, score_breakdown,
                     score_summary, red_flags, green_flags, recommendation, status, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    external_id, job_title, company, location, salary_raw, salary_min_usd,
                    is_remote, job_url, description[:10000], source, score,
                    json.dumps(scoring.get("breakdown", {})),
                    scoring.get("summary", ""),
                    json.dumps(scoring.get("red_flags", [])),
                    json.dumps(scoring.get("green_flags", [])),
                    recommendation, status, notes,
                ))
                db.commit()
                print(f"score={score} → {recommendation}{'  [UAE]' if uae_role else ''}")

            print(f"  Pass done: {pass_new} new jobs.")
            upsert_daily_stats(db, discovered=len(df))
            time.sleep(random.uniform(3, 6))

    upsert_daily_stats(db, scored=total_scored)
    db.close()

    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISCOVERY COMPLETE
  Total scraped:        {total_found}
  New (not duplicate):  {total_new}
  Blacklist-skipped:    {total_bl_skipped}
  Scored:               {total_scored}
  Above threshold(≥{threshold_review}):  {above_threshold}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run /job-hunter:review to see pending jobs.
""")


if __name__ == "__main__":
    main()
