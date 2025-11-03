import sqlite3, json
from pathlib import Path

DB_PATH = Path("leads.db")

class Storage:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.init_db()

    def init_db(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            value_props TEXT,
            ideal_use_cases TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            company TEXT,
            industry TEXT,
            location TEXT,
            linkedin_bio TEXT,
            rule_score INTEGER,
            ai_points INTEGER,
            total_score INTEGER,
            intent TEXT,
            reasoning TEXT
        )
        """)
        self.conn.commit()

    def insert_offer(self, offer):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO offers (name,value_props,ideal_use_cases) VALUES (?,?,?)",
                    (offer.name, json.dumps(offer.value_props), json.dumps(offer.ideal_use_cases)))
        self.conn.commit()

    def insert_lead(self, lead):
        cur = self.conn.cursor()
        cur.execute("""INSERT INTO leads (name,role,company,industry,location,linkedin_bio)
                    VALUES (?,?,?,?,?,?)""",
                    (lead.get("name"), lead.get("role"), lead.get("company"),
                     lead.get("industry"), lead.get("location"), lead.get("linkedin_bio")))
        self.conn.commit()

    def get_latest_offer(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM offers ORDER BY id DESC LIMIT 1")
        row = cur.fetchone()
        if not row: return None
        return {
            "id": row[0],
            "name": row[1],
            "value_props": json.loads(row[2]),
            "ideal_use_cases": json.loads(row[3])
        }

    def get_all_leads(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM leads")
        rows = cur.fetchall()
        return [dict(zip([c[0] for c in cur.description], row)) for row in rows]

    def update_lead_result(self, id, rule_score, ai_points, total, ai_data):
        cur = self.conn.cursor()
        cur.execute("""UPDATE leads SET rule_score=?, ai_points=?, total_score=?, intent=?, reasoning=? WHERE id=?""",
                    (rule_score, ai_points, total, ai_data["intent"], ai_data["explanation"], id))
        self.conn.commit()

    def get_scored_leads(self):
        cur = self.conn.cursor()
        cur.execute("SELECT name,role,company,industry,location,intent,total_score as score,reasoning FROM leads WHERE intent IS NOT NULL")
        rows = cur.fetchall()
        return [dict(zip([c[0] for c in cur.description], row)) for row in rows]

DB = Storage()
