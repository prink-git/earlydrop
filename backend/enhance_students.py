from supabase import create_client

SUPABASE_URL = "https://lqzvxxhwpirjowkqwjys.supabase.co"
SUPABASE_KEY = "sb_secret_G2P7kak0XO54kQcrAqvBgA_1FwmxgZ2"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

NAMES = [
    "Aarav Sharma","Riya Mehta","Kabir Verma","Ananya Gupta","Ishaan Jain",
    "Neha Kapoor","Siddharth Malhotra","Pooja Singh","Arjun Nair","Tanvi Deshpande",
    "Aditya Kulkarni","Simran Kaur","Rahul Iyer","Nikhil Bansal","Kritika Joshi",
    "Aman Choudhary","Sneha Rao","Vivek Mishra","Mehul Patel","Shreya Ghosh"
]

COURSES = [
    "Machine Learning",
    "Data Structures",
    "System Design",
    "Web Development",
    "Databases",
    "Operating Systems"
]

students = supabase.table("students").select("id").execute().data

for i, s in enumerate(students):
    supabase.table("students").update({
        "full_name": NAMES[i % len(NAMES)],
        "course": COURSES[i % len(COURSES)]
    }).eq("id", s["id"]).execute()

print("✅ Students now have diverse names & courses")
