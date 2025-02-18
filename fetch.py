import requests
import os
import time
import pandas as pd
import mysql.connector
from config.config import DATABASE_CONFIG

CLIENT_ID = "KgAcAKYRPDDJiQuDwLa8ONofIWM81fheeMRIva6U"
CLIENT_SECRET = "PBTIk3ESOKxBMXDU5aIplW3yGb2QpXzxbRq19icb8qhm6bo6nFF9QiMohKtSIchlfcqEIUIAxoYyjfh86h1Qo3WRnxbv07LSa9X3aZqrN0TjVBwOSJSAGYf9vzjUXugD"
UDEMY_API_URL = "https://www.udemy.com/api-2.0/courses/"


csv_path = "udemy_courses.csv"  # Change this to the actual path
df = pd.read_csv(csv_path)

# ✅ Ensure required columns exist in CSV
if "thumbnail_url" not in df.columns:
    df["thumbnail_url"] = ""

if "instructor" not in df.columns:
    df["instructor"] = ""

# ✅ Connect to MySQL
conn = mysql.connector.connect(**DATABASE_CONFIG)
cursor = conn.cursor()

# ✅ Function to Fetch Full Course Details
def get_course_details(course_title):
    params = {
        "search": course_title, 
        "page_size": 1,
        "fields[course]": "title,url,image_480x270,visible_instructors,num_subscribers,price,content_info,avg_rating,headline"
    }
    
    headers = {"Accept": "application/json"}
    response = requests.get(UDEMY_API_URL, params=params, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))

    if response.status_code == 200:
        data = response.json()
        courses = data.get("results", [])
        print(courses)
        if courses:
            course = courses[0]
            return {
                "title": course.get("title", ""),
                "url": f"https://www.udemy.com{course.get('url', '')}",
                "thumbnail": course.get("image_480x270", ""),
                "instructor": course.get("visible_instructors", [{}])[0].get("display_name", "Unknown"),
                "subscribers": course.get("num_subscribers", 0),
                "price": course.get("price", "Unknown"),
                "duration": course.get("content_info", ""),
                "rating": course.get("avg_rating", 0),
                "description": course.get("headline", "")
            }

    print(f"❌ API Request Failed for {course_title}: {response.status_code}, {response.text}")
    return {"title": "", "url": "", "thumbnail": "", "instructor": "Unknown", "subscribers": 0, "price": "Unknown", "duration": "", "rating": 0, "description": ""}

# ✅ Fetch Courses Without Thumbnails & Instructors
cursor.execute("SELECT id, course_title FROM courses WHERE thumbnail_url = '' OR instructor = ''")
courses = cursor.fetchall()

# ✅ Update Each Course
for course_id, course_title in courses:
    details = get_course_details(course_title)

    # ✅ Update MySQL
    cursor.execute("""
        UPDATE courses 
        SET thumbnail_url = %s, instructor = %s, num_subscribers = %s, price = %s, 
            duration = %s, avg_rating = %s, course_url = %s, description = %s
        WHERE id = %s
    """, (
        details["thumbnail"], details["instructor"], details["subscribers"], details["price"],
        details["duration"], details["rating"], details["url"], details["description"], course_id
    ))

    # ✅ Update CSV
    df.loc[df["course_title"] == course_title, "thumbnail_url"] = details["thumbnail"]
    df.loc[df["course_title"] == course_title, "instructor"] = details["instructor"]
    df.loc[df["course_title"] == course_title, "num_subscribers"] = details["subscribers"]
    df.loc[df["course_title"] == course_title, "price"] = details["price"]
    df.loc[df["course_title"] == course_title, "duration"] = details["duration"]
    df.loc[df["course_title"] == course_title, "avg_rating"] = details["rating"]
    df.loc[df["course_title"] == course_title, "course_url"] = details["url"]
    df.loc[df["course_title"] == course_title, "description"] = details["description"]

    print(f"✅ Updated: {course_title} → {details['instructor']} ({details['rating']}⭐)")

    # ✅ Add a short delay to prevent hitting API limits
    time.sleep(1.5)  # Adjust as needed to avoid rate limits

# ✅ Commit & Close MySQL Connection
conn.commit()
cursor.close()
conn.close()
print("✅ All courses updated in MySQL!")

# ✅ Save Updated CSV
updated_csv_path = "udemy_courses_with_details.csv"
df.to_csv(updated_csv_path, index=False)
print(f"✅ Updated CSV saved at: {updated_csv_path}")