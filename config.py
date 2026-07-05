import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-in-production")
    
    # Database URI - supports MySQL and SQLite
    # For MySQL: mysql+pymysql://user:password@host/dbname
    # For SQLite: sqlite:///instance/app.db
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Default to SQLite for development - use absolute path
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "instance", "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
