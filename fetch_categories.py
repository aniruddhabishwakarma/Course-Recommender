import requests
import time
import pandas as pd

CLIENT_ID = "KgAcAKYRPDDJiQuDwLa8ONofIWM81fheeMRIva6U"
CLIENT_SECRET = "PBTIk3ESOKxBMXDU5aIplW3yGb2QpXzxbRq19icb8qhm6bo6nFF9QiMohKtSIchlfcqEIUIAxoYyjfh86h1Qo3WRnxbv07LSa9X3aZqrN0TjVBwOSJSAGYf9vzjUXugD"
UDEMY_API_URL = "https://www.udemy.com/api-2.0/courses/"

topics = [
    "Python", "Java", "JavaScript", "Deep Learning", "Machine Learning", "NLP", "Computer Vision", 
    "Data Science", "Data Analytics", "Mathematics", "Graphic Design", "IELTS"
]

# ✅ Function to Fetch Courses for Each Topic
def fetch_udemy_courses(topic, num_pages=4, page_size=100):
    all_courses = []
    
    for page in range(1, num_pages + 1):
        params = {
            "search": topic,
            "page": page,
            "page_size": page_size,
            "fields[course]": "id,title,url,image_480x270,visible_instructors,"
                              "num_subscribers,price,price_detail,content_info,"
                              "avg_rating,headline,num_published_lectures"
        }
        
        headers = {"Accept": "application/json"}
        response = requests.get(UDEMY_API_URL, params=params, headers=headers, auth=(CLIENT_ID, CLIENT_SECRET))

        if response.status_code == 200:
            courses = response.json().get("results", [])
            for course in courses:
                instructor_data = course.get("visible_instructors", [{}])[0]  # ✅ Get first instructor
                instructor_name = instructor_data.get("display_name", "Unknown")
                instructor_photo = instructor_data.get("image_100x100", "")  # ✅ Instructor photo
                
                num_lectures = course.get("num_published_lectures", 0)  # ✅ Number of lectures
                
                # ✅ Handle price safely (Fix ALL occurrences)
                price_detail = course.get("price_detail")
                price = price_detail["price_string"] if price_detail else "Free"
                currency = price_detail["currency"] if price_detail else "Unknown"

                course_data = {
                    "topic": topic,
                    "course_id": course.get("id", ""),
                    "title": course.get("title", ""),
                    "url": f"https://www.udemy.com{course.get('url', '')}",
                    "thumbnail": course.get("image_480x270", ""),
                    "instructor": instructor_name,
                    "instructor_photo": instructor_photo,
                    "num_lectures": num_lectures,
                    "subscribers": course.get("num_subscribers", 0),
                    "price": price,
                    "currency": currency,  # ✅ Fixed
                    "duration": course.get("content_info", ""),
                    "rating": course.get("avg_rating", 0),
                    "description": course.get("headline", "")
                }
                all_courses.append(course_data)

            print(f"✅ Topic '{topic}' - Page {page}: Fetched {len(courses)} courses")

        else:
            print(f"❌ API Request Failed for '{topic}' on Page {page}: {response.status_code}, {response.text}")

        # ✅ Pause to prevent API rate limits
        time.sleep(1.5)

    return all_courses
# ✅ Fetch Courses for Multiple Topics
all_courses_data = []

for topic in topics:
    courses = fetch_udemy_courses(topic, num_pages=4, page_size=100)  # Fetch up to 1000 per topic
    all_courses_data.extend(courses)

# ✅ Convert Data to Pandas DataFrame & Save to CSV
df = pd.DataFrame(all_courses_data)
output_csv = "udemy_courses_data.csv"
df.to_csv(output_csv, index=False)

print(f"✅ Successfully saved {len(all_courses_data)} Udemy courses from multiple topics to '{output_csv}'")