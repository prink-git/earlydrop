-- ========================================
-- EarlyDrop Database Schema & RLS Policies
-- ========================================
-- This file defines the core schema and Row-Level Security (RLS) policies.
-- RUN THIS IN SUPABASE SQL EDITOR (not as-is; adapt for your setup).

-- ============================================
-- 1. TABLES (create if not already present)
-- ============================================

-- Students table
CREATE TABLE IF NOT EXISTS students (
  id BIGSERIAL PRIMARY KEY,
  full_name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  course TEXT NOT NULL,
  enrollment_date DATE,
  gpa FLOAT CHECK (gpa >= 0 AND gpa <= 4.0),
  status TEXT DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'dropout')),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Risk scores table
CREATE TABLE IF NOT EXISTS risk_scores (
  id BIGSERIAL PRIMARY KEY,
  student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  risk_score FLOAT NOT NULL CHECK (risk_score >= 0 AND risk_score <= 100),
  risk_level TEXT CHECK (risk_level IN ('Low', 'Medium', 'High')),
  predicted_dropout_reason TEXT,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Weekly features (engagement data)
CREATE TABLE IF NOT EXISTS weekly_features (
  id BIGSERIAL PRIMARY KEY,
  student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  week INT NOT NULL CHECK (week > 0),
  avg_session_time FLOAT NOT NULL CHECK (avg_session_time >= 0),
  videos_completed INT CHECK (videos_completed >= 0),
  assignments_submitted INT CHECK (assignments_submitted >= 0),
  forum_posts INT CHECK (forum_posts >= 0),
  gpa_trend FLOAT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Interventions (action logs)
CREATE TABLE IF NOT EXISTS interventions (
  id BIGSERIAL PRIMARY KEY,
  student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  action TEXT NOT NULL,
  note TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- 2. INDEXES (for performance)
-- ============================================

CREATE INDEX IF NOT EXISTS idx_risk_scores_student_id ON risk_scores(student_id);
CREATE INDEX IF NOT EXISTS idx_weekly_features_student_id ON weekly_features(student_id);
CREATE INDEX IF NOT EXISTS idx_interventions_student_id ON interventions(student_id);

-- ============================================
-- 3. ROW-LEVEL SECURITY (RLS) - ENABLE
-- ============================================

-- Enable RLS on all tables
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE weekly_features ENABLE ROW LEVEL SECURITY;
ALTER TABLE interventions ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 4. RLS POLICIES - PUBLIC READ (Anon Key)
-- ============================================

-- Anonymous users (frontend via anon key) can READ all student data
CREATE POLICY "public_read_students" ON students
  FOR SELECT
  USING (true);

CREATE POLICY "public_read_risk_scores" ON risk_scores
  FOR SELECT
  USING (true);

CREATE POLICY "public_read_weekly_features" ON weekly_features
  FOR SELECT
  USING (true);

CREATE POLICY "public_read_interventions" ON interventions
  FOR SELECT
  USING (true);

-- ============================================
-- 5. RLS POLICIES - SERVICE-ROLE WRITE
-- ============================================

-- Service role (backend via service-role key) can WRITE interventions
-- (authenticated users with service-role claim can insert/update/delete)
CREATE POLICY "service_role_write_interventions" ON interventions
  FOR INSERT
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "service_role_update_interventions" ON interventions
  FOR UPDATE
  USING (auth.role() = 'service_role');

CREATE POLICY "service_role_delete_interventions" ON interventions
  FOR DELETE
  USING (auth.role() = 'service_role');

-- ============================================
-- 6. NOTES FOR DEPLOYMENT
-- ============================================
-- 
-- STEPS TO APPLY THIS SCHEMA:
-- 
-- 1. Go to Supabase Dashboard > SQL Editor
-- 2. Click "New Query"
-- 3. Copy-paste sections 1-5 above (skip comments for clarity)
-- 4. Run the query
-- 5. Verify tables exist: Supabase Dashboard > Table Editor
-- 6. Verify RLS is enabled: Supabase Dashboard > Tables > [table] > RLS
-- 
-- KEYS:
-- - Use ANON_KEY in frontend (.env.local) and for SELECT operations
-- - Use SERVICE_ROLE_KEY in backend (.env) for INSERT/UPDATE/DELETE
-- - Never expose SERVICE_ROLE_KEY to client (frontend)
-- 
-- RLS POLICIES:
-- - SELECT: anyone (anon key or auth'd user)
-- - INSERT interventions: only service role (backend server-side only)
-- - UPDATE/DELETE: only service role
-- 
-- If you need to seed data while developing:
-- 1. Temporarily DISABLE RLS: ALTER TABLE [table] DISABLE ROW LEVEL SECURITY;
-- 2. Seed data
-- 3. Re-enable RLS: ALTER TABLE [table] ENABLE ROW LEVEL SECURITY;
--
