import pandas as pd
import mysql.connector
from datetime import datetime

# Database connection settings
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "LEapfrog@33",
    "database": "course_recommendation"
}

# Load the CSV file
csv_file = "udemy_courses_data.csv"  # Change this to the actual path
df = pd.read_csv(csv_file)

df = df.fillna({
    "topic": "Unknown",
    "course_id": 0,
    "title": "Unknown Title",
    "url": "#",
    "thumbnail": "#",
    "instructor": "Unknown Instructor",
    "instructor_photo": "#",  # ✅ New Column
    "num_lectures": 0,        # ✅ New Column
    "subscribers": 0,
    "price": "Free",
    "currency": "USD",
    "duration": "0 hours",
    "rating": 0.0,
    "description": "No description available"
})

# ✅ Convert data types to ensure MySQL compatibility
df["course_id"] = df["course_id"].astype(int)
df["num_lectures"] = df["num_lectures"].astype(int)
df["subscribers"] = df["subscribers"].astype(int)
df["rating"] = df["rating"].astype(float)

# Establish MySQL connection
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

insert_query = """
    INSERT INTO courses (topic, course_id, title, url, thumbnail, instructor, instructor_photo, 
                         num_lectures, subscribers, price, currency, duration, rating, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE 
        title = VALUES(title), 
        instructor = VALUES(instructor), 
        instructor_photo = VALUES(instructor_photo),
        num_lectures = VALUES(num_lectures),
        subscribers = VALUES(subscribers), 
        price = VALUES(price), 
        currency = VALUES(currency), 
        duration = VALUES(duration), 
        rating = VALUES(rating), 
        description = VALUES(description);
"""

# ✅ Insert each row into MySQL
for _, row in df.iterrows():
    data = (
        row['topic'], row['course_id'], row['title'], row['url'], row['thumbnail'],
        row['instructor'], row['instructor_photo'], row['num_lectures'], row['subscribers'], 
        row['price'], row['currency'], row['duration'], row['rating'], row['description']
    )
    cursor.execute(insert_query, data)

# ✅ Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print(f"✅ Successfully inserted {len(df)} courses into MySQL!")
