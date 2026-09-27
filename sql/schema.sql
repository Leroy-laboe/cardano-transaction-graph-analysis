CREATE TABLE IF NOT EXISTS transactions (
  tx_id TEXT PRIMARY KEY,
  timestamp TIMESTAMP,
  from_addr TEXT,
  to_addr TEXT,
  amount DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_from_addr ON transactions(from_addr);
CREATE INDEX IF NOT EXISTS idx_to_addr ON transactions(to_addr);
CREATE INDEX IF NOT EXISTS idx_timestamp ON transactions(timestamp);
