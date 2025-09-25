CREATE TABLE IF NOT EXISTS applications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT,
  position TEXT NOT NULL,
  location TEXT,
  cover TEXT,
  auth_to_work TEXT,
  cv_filename TEXT,
  created_at TIMESTAMP
);