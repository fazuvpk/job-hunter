#!/usr/bin/env python3
"""Job review server — serves the validation UI at http://localhost:7749"""

import json, sqlite3, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from pathlib import Path

ROOT        = Path(__file__).parent.parent
DB_PATH     = ROOT / "data" / "jobs.db"
BLACKLIST   = ROOT / "config" / "blacklist.json"
HTML_PATH   = Path(__file__).parent / "review_ui.html"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._raw(200, "text/html; charset=utf-8", HTML_PATH.read_bytes())
        elif path == "/api/jobs":
            self._json(get_jobs())
        else:
            self._raw(404, "text/plain", b"Not found")

    def do_POST(self):
        parts = [p for p in urlparse(self.path).path.split("/") if p]
        # /api/jobs/{id}/approve|skip|blacklist
        if len(parts) == 4 and parts[:2] == ["api", "jobs"]:
            try:
                self._json(handle_action(int(parts[2]), parts[3]))
            except Exception as e:
                self._json({"error": str(e)})
        else:
            self._raw(404, "text/plain", b"Not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.end_headers()

    def _raw(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, data):
        body = json.dumps(data, ensure_ascii=False).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_):
        pass  # quiet server


def db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def get_jobs():
    con = db()
    rows = con.execute("""
        SELECT id, title, company, location, salary_raw, url, score,
               score_breakdown, score_summary, green_flags, red_flags,
               recommendation, source, discovered_at
        FROM jobs
        WHERE status = 'pending' AND score >= 60
        ORDER BY score DESC
    """).fetchall()
    con.close()
    result = []
    for row in rows:
        j = dict(row)
        for f in ("score_breakdown", "green_flags", "red_flags"):
            try:
                j[f] = json.loads(j[f]) if j.get(f) else ({} if f == "score_breakdown" else [])
            except Exception:
                j[f] = {} if f == "score_breakdown" else []
        result.append(j)
    return result


def handle_action(job_id: int, action: str) -> dict:
    con = db()
    if action == "approve":
        con.execute("UPDATE jobs SET status='approved', reviewed_at=datetime('now') WHERE id=?", (job_id,))
    elif action == "skip":
        con.execute("UPDATE jobs SET status='skipped', reviewed_at=datetime('now') WHERE id=?", (job_id,))
    elif action == "blacklist":
        row = con.execute("SELECT company FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row:
            company = row["company"]
            con.execute(
                "UPDATE jobs SET status='skipped', reviewed_at=datetime('now') WHERE company=? AND status='pending'",
                (company,),
            )
            _blacklist_company(company)
    else:
        con.close()
        return {"error": f"unknown action: {action}"}
    con.commit()
    con.close()
    return {"ok": True}


def _blacklist_company(company: str):
    try:
        with open(BLACKLIST) as f:
            bl = json.load(f)
        lst = bl.setdefault("blacklisted_companies", [])
        if company not in lst:
            lst.append(company)
            with open(BLACKLIST, "w") as f:
                json.dump(bl, f, indent=2)
    except Exception:
        pass


if __name__ == "__main__":
    import sys
    no_browser = "--no-browser" in sys.argv
    port = 7749
    local_url  = f"http://localhost:{port}"
    tail_url   = f"http://m1.bombay-newton.ts.net:{port}"
    print(f"Job Review UI")
    print(f"  Local   → {local_url}")
    print(f"  Tailnet → {tail_url}")
    print("Press Ctrl+C to stop.\n")
    if not no_browser:
        webbrowser.open(local_url)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
