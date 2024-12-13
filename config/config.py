
from os import path


class config():
    

    ARCHIVE_FOLDER = "0-Archive" 
    DATA_FOLDER = "sessions"
    REFERENCE_FOLDER = "reference"
    DEBUG_FOLDER = "Debug"
    DB = path.join('db','journal.db')

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB}"

    DM = "\033[32mDEBUG:\033[0m"
    DEBUG = True


    LANG = "french"  # french or english lowercase