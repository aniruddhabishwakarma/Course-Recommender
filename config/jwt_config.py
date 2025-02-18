from flask_jwt_extended import JWTManager

def init_jwt(app):
    """Initialize JWT settings."""
    app.config["JWT_SECRET_KEY"] = "sajdlaskdjaksldjsakldjsakldjalkjdaklsdjaskldjaskldjaslkdjsakl"  # Change this in production!
    return JWTManager(app)