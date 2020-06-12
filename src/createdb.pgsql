CREATE TABLE IF NOT EXISTS budget(
  codename VARCHAR(255) PRIMARY KEY,
  daily_limit INTEGER
);

CREATE TABLE IF NOT EXISTS category(
  codename VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL UNIQUE,
  is_base_expense BOOLEAN,
  aliases TEXT
);

CREATE TABLE IF NOT EXISTS expense(
  id INTEGER PRIMARY KEY,
  amount INTEGER,
  created TIMESTAMP,
  category_codename VARCHAR(255),
  raw_text TEXT,
  FOREIGN KEY (category_codename) REFERENCES category(codename)
);
