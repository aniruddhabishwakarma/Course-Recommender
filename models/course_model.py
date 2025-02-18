class Course:
    def __init__(self, id, topic, course_id, title, url, thumbnail, instructor, instructor_photo, 
                 num_lectures, subscribers, price, currency, duration, rating, description):
        self.id = id
        self.topic = topic  # ✅ New Column
        self.course_id = course_id  # ✅ Unique Course ID from Udemy
        self.title = title  
        self.url = url  
        self.thumbnail = thumbnail  
        self.instructor = instructor  
        self.instructor_photo = instructor_photo  # ✅ New Column  
        self.num_lectures = num_lectures  # ✅ New Column  
        self.subscribers = subscribers  
        self.price = price  
        self.currency = currency  # ✅ New Column  
        self.duration = duration  
        self.rating = rating  
        self.description = description  

    def to_dict(self):
        """Convert object to dictionary for JSON response."""
        return self.__dict__