
from os import path


class config():
    

    ARCHIVE_FOLDER = "0-Archive" 
    DATA_FOLDER = "sessions"
    REFERENCE_FOLDER = "reference"
    DEBUG_FOLDER = "Debug"
    DB = path.join('db','journal.db')

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB}"



    LANG = "english"