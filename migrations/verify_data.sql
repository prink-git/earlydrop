-- Run these in Supabase SQL Editor to verify all 500 students + data were imported

-- Check students count
SELECT COUNT(*) as total_students FROM public.students;

-- Check sample students with emails and status
SELECT id, full_name, email, course, gpa, status, enrollment_date 
FROM public.students 
LIMIT 5;

-- Check weekly features count (should be ~4000 = 500 students × 8 weeks)
SELECT COUNT(*) as total_weekly_features FROM public.weekly_features;

-- Check risk scores count (should be 500)
SELECT COUNT(*) as total_risk_scores FROM public.risk_scores;

-- Distribution of risk levels
SELECT risk_level, COUNT(*) as count FROM public.risk_scores GROUP BY risk_level;

-- Check interventions count
SELECT COUNT(*) as total_interventions FROM public.interventions;

-- Sample risk scores
SELECT student_id, risk_score, risk_level, predicted_dropout_reason 
FROM public.risk_scores 
WHERE risk_level = 'High' 
LIMIT 10;

-- Summary query
SELECT 
  (SELECT COUNT(*) FROM public.students) as students,
  (SELECT COUNT(*) FROM public.weekly_features) as weekly_features,
  (SELECT COUNT(*) FROM public.risk_scores) as risk_scores,
  (SELECT COUNT(*) FROM public.interventions) as interventions;
