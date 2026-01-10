# db.py
import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set")
    return psycopg2.connect(DATABASE_URL)


def get_students():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, full_name, course FROM students LIMIT 50;"
                )
                return cur.fetchall()
    except Exception as e:
        print("DB error in get_students:", e)
        return []


def get_risks():
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT student_id, risk_score FROM risk_scores;"
                )
                return cur.fetchall()
    except Exception as e:
        print("DB error in get_risks:", e)
        return []


def get_features(student_id):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT week, avg_session_time, videos_completed
                    FROM weekly_features
                    WHERE student_id = %s
                    ORDER BY week;
                """, (student_id,))
                return cur.fetchall()
    except Exception as e:
        print("DB error in get_features:", e)
        return []


def get_interventions(student_id):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT action, created_at
                    FROM interventions
                    WHERE student_id = %s
                    ORDER BY created_at DESC;
                """, (student_id,))
                return cur.fetchall()
    except Exception as e:
        print("DB error in get_interventions:", e)
        return []


def add_intervention(student_id, action, note):
    try:
        with get_conn() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO interventions (student_id, action, note)
                    VALUES (%s, %s, %s);
                """, (student_id, action, note))
                conn.commit()
    except Exception as e:
        print("DB error in add_intervention:", e)
