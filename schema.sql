-- schema.sql
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Providers (
  Provider_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Name TEXT,
  Provider_Type TEXT,
  Contact TEXT,
  Address TEXT
);

CREATE TABLE IF NOT EXISTS Food_Listings (
  Food_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Food_Name TEXT NOT NULL,
  Quantity INTEGER NOT NULL CHECK (Quantity >= 0),
  Unit TEXT DEFAULT 'servings',
  Location TEXT,
  Lat REAL,
  Lon REAL,
  Expiry_Date DATE,
  Date_Added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  Provider_ID INTEGER,
  Provider_Type TEXT,
  Status TEXT DEFAULT 'Available',
  Claimed_By TEXT,
  Claimed_At TIMESTAMP,
  Contact TEXT,
  Notes TEXT,
  FOREIGN KEY (Provider_ID) REFERENCES Providers(Provider_ID)
);

CREATE TABLE IF NOT EXISTS Claims (
  Claim_ID INTEGER PRIMARY KEY AUTOINCREMENT,
  Food_ID INTEGER,
  Claimer_Name TEXT,
  Claimer_Contact TEXT,
  Claimed_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  Status TEXT DEFAULT 'Completed',
  FOREIGN KEY (Food_ID) REFERENCES Food_Listings(Food_ID)
);

CREATE INDEX IF NOT EXISTS idx_food_location ON Food_Listings(Location);
CREATE INDEX IF NOT EXISTS idx_food_status ON Food_Listings(Status);
CREATE INDEX IF NOT EXISTS idx_food_expiry ON Food_Listings(Expiry_Date);
