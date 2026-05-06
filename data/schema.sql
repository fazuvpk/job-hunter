CREATE TABLE IF NOT EXISTS jobs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  external_id TEXT UNIQUE,
  title TEXT NOT NULL,
  company TEXT NOT NULL,
  location TEXT,
  salary_raw TEXT,
  salary_min_usd INTEGER,
  remote BOOLEAN,
  url TEXT NOT NULL,
  description TEXT,
  source TEXT,
  score INTEGER,
  score_breakdown TEXT,
  score_summary TEXT,
  red_flags TEXT,
  green_flags TEXT,
  recommendation TEXT,
  status TEXT DEFAULT 'pending',
  discovered_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  reviewed_at DATETIME,
  applied_at DATETIME,
  response_at DATETIME,
  notes TEXT,
  resume_path TEXT,
  cover_path TEXT
);

CREATE TABLE IF NOT EXISTS applications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  job_id INTEGER REFERENCES jobs(id),
  submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  method TEXT,
  ats_platform TEXT,
  confirmation TEXT,
  follow_up_sent BOOLEAN DEFAULT 0,
  follow_up_at DATETIME,
  outcome TEXT
);

CREATE TABLE IF NOT EXISTS daily_stats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  date TEXT UNIQUE,
  discovered INTEGER DEFAULT 0,
  scored INTEGER DEFAULT 0,
  reviewed INTEGER DEFAULT 0,
  applied INTEGER DEFAULT 0,
  responses INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_jobs_score ON jobs(score);
CREATE INDEX IF NOT EXISTS idx_jobs_discovered_at ON jobs(discovered_at);
CREATE INDEX IF NOT EXISTS idx_jobs_company ON jobs(company);
CREATE INDEX IF NOT EXISTS idx_applications_job_id ON applications(job_id);
CREATE INDEX IF NOT EXISTS idx_applications_submitted_at ON applications(submitted_at);
CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(date);
