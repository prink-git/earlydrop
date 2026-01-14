import os
from dotenv import load_dotenv
from supabase import create_client


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("Supabase env vars not set")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

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

def main():
    students = supabase.table("students").select("id").execute().data

    for i, s in enumerate(students):
        supabase.table("students").update({
            "full_name": NAMES[i % len(NAMES)],
            "course": COURSES[i % len(COURSES)]
        }).eq("id", s["id"]).execute()

    print("✅ Students now have diverse names & courses")

if __name__ == "__main__":
    main()
