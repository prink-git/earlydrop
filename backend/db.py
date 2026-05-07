"""
This module handles database operations for the application.

Functions:
- get_students: Retrieves all students from the database.
- get_risks: Retrieves risk data from the database.
- get_features: Retrieves features for a specific student.
- get_interventions: Retrieves interventions for a specific student.
- add_intervention: Adds an intervention for a specific student.
"""

from dotenv import load_dotenv
load_dotenv()

import os
from supabase import create_client
import logging
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY") or os.getenv("SUPABASE_KEY")  # fallback for backward compat
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL env var not set")
if not SUPABASE_ANON_KEY:
    raise RuntimeError("SUPABASE_ANON_KEY env var not set")

# Client for read operations (uses anon key, respects RLS for SELECTs)
supabase_read = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# Client for write operations (uses service-role key if available, bypasses RLS)
supabase_write = None
if SUPABASE_SERVICE_ROLE_KEY:
    supabase_write = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    logger.info("SERVICE_ROLE_KEY provided; write operations will use service-role client")
else:
    logger.warning("SERVICE_ROLE_KEY not set; write operations will use anon key (not recommended for production)")
    supabase_write = supabase_read


def get_students(limit=100, offset=0):
    """
    Fetches a paginated list of students from the database.

    Args:
        limit (int): The maximum number of records to fetch.
        offset (int): The starting point for fetching records.

    Returns:
        list: A list of student records.
    """
    logger.info("Fetching students from the database with pagination")
    try:
        return supabase_read.table("students") \
            .select("id, full_name, course") \
            .range(offset, offset + limit - 1) \
            .execute().data
    except Exception as e:
        logger.error(f"Database error in get_students: {e}")
        raise


def get_risks(limit=100, offset=0):
    """
    Fetches a paginated list of risks from the database.

    Args:
        limit (int): The maximum number of records to fetch.
        offset (int): The starting point for fetching records.

    Returns:
        list: A list of risk records.
    """
    logger.info("Fetching risks from the database with pagination")
    try:
        return supabase_read.table("risk_scores") \
            .select("student_id, risk_score") \
            .range(offset, offset + limit - 1) \
            .execute().data
    except Exception as e:
        logger.error(f"Database error in get_risks: {e}")
        raise


def get_features(student_id, limit=100, offset=0):
    """
    Fetches a paginated list of features for a specific student.

    Args:
        student_id (str): The ID of the student.
        limit (int): The maximum number of records to fetch.
        offset (int): The starting point for fetching records.

    Returns:
        list: A list of feature records.
    """
    logger.info(f"Fetching features for student_id: {student_id} with pagination")
    try:
        return supabase_read.table("weekly_features") \
            .select("week, avg_session_time, videos_completed") \
            .eq("student_id", student_id) \
            .range(offset, offset + limit - 1) \
            .order("week") \
            .execute().data
    except Exception as e:
        logger.error(f"Database error in get_features for student_id {student_id}: {e}")
        raise


def get_interventions(student_id, limit=100, offset=0):
    """
    Fetches a paginated list of interventions for a specific student.

    Args:
        student_id (str): The ID of the student.
        limit (int): The maximum number of records to fetch.
        offset (int): The starting point for fetching records.

    Returns:
        list: A list of intervention records.
    """
    logger.info(f"Fetching interventions for student_id: {student_id} with pagination")
    try:
        return supabase_read.table("interventions") \
            .select("action, created_at") \
            .eq("student_id", student_id) \
            .range(offset, offset + limit - 1) \
            .order("created_at", desc=True) \
            .execute().data
    except Exception as e:
        logger.error(f"Database error in get_interventions for student_id {student_id}: {e}")
        raise


def add_intervention(student_id, action, note):
    logger.info(f"Adding intervention for student_id: {student_id}, action: {action}, note: {note}")
    try:
        supabase_write.table("interventions").insert({
            "student_id": student_id,
            "action": action,
            "note": note
        }).execute()
    except SQLAlchemyError as e:
        logger.error(f"Database error in add_intervention for student_id {student_id}: {e}")
        raise
