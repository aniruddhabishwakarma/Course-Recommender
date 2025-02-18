class User:
    def __init__(self, id, username, email, password_hash, fullname, contact, thumbnail, created_at):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.fullname = fullname
        self.contact = contact
        self.thumbnail = thumbnail
        self.created_at = created_at

    def to_dict(self):
        """Convert the User object to a dictionary (for JSON responses)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "fullname": self.fullname,
            "contact": self.contact,
            "thumbnail": self.thumbnail,
            "created_at": self.created_at
        }