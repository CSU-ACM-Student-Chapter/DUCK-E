import os, mysql.connector
import mysql.connector.cursor#, sqlite3

'''
PURPOSE
------------
In order to encourage devs to remain within 'DUCK-E' as the cwd, we promote 
the usage of constants to access needed resources. As this project changes, 
as will its file structure. This single access point will help keep project 
consistency and circumvent the tedious code changes that're typically needed 
following any changes to file structure. And instead will be changed inside of here 
and only here.

NOTE
------------
.env is not used for two primary reasons. 
1. It serves to store production critical information 
2. It doesn't have the needed modules for variable creation
'''

# Access to Resource Directories
RESOURCES_FOLDER= os.path.join(os.getcwd(), 'ducke', 'resources')
RESOURCES_QUESTIONS_FOLDER= os.path.join(RESOURCES_FOLDER, 'questions')
RESOURCES_RESPONSES_FOLDER= os.path.join(RESOURCES_FOLDER, 'responses')
RESOURCES_JOKE_ATTACHMENTS_FOLDER= os.path.join(RESOURCES_FOLDER, 'joke_attachments')

# Access to all Files within Resources Questions Directory
RESOURCES_QUESTIONS_PYTHON_IMAGES_FOLDER= os.path.join(RESOURCES_QUESTIONS_FOLDER, 'python_images')
RESOURCES_QUESTIONS_PYTHON_CSV_FILE= os.path.join(RESOURCES_QUESTIONS_FOLDER, 'python.csv')
RESOURCES_QUESTIONS_PYTHON_TXT_FILE= os.path.join(RESOURCES_QUESTIONS_FOLDER, 'python.txt')

# Access to all Response Text Files
RESOURCES_RESPONSES_QUESTION_CHEATER= os.path.join(RESOURCES_RESPONSES_FOLDER, 'question_cheater.txt')
RESOURCES_RESPONSES_QUESTION_CORRECT= os.path.join(RESOURCES_RESPONSES_FOLDER, 'question_correct.txt')
RESOURCES_RESPONSES_QUESTION_INCORRECT= os.path.join(RESOURCES_RESPONSES_FOLDER, 'question_incorrect.txt')
RESOURCES_RESPONSES_FLASH_QUESTION_ANNOUNCEMENTS= os.path.join(RESOURCES_RESPONSES_FOLDER, 'flash_question_announcements.txt')

RESOURCES_RESPONSES_JOKES= os.path.join(RESOURCES_RESPONSES_FOLDER, 'jokes.csv')
RESOURCES_RESPONSE_JOKE_ANNOUNCEMENTS= os.path.join(RESOURCES_RESPONSES_FOLDER, 'joke_announcements.txt')

# Access to denied request messages
ACCESS_REQUEST_MESSAGE="❌ I don't have permissions to complete this command in this channel. Please grant access in the Discord Developer Portal."

# MySQL Connection
MYSQL_CONNECTION = mysql.connector.connect(
    host=os.getenv('DATABASE_HOSTNAME'),
    user=os.getenv('DATABASE_USERNAME'),
    password=os.getenv('DATABASE_PASSWORD'),
    database=os.getenv('DATABASE_NAME')
)

def get_cursor() -> mysql.connector.cursor.MySQLCursor:
    MYSQL_CONNECTION.ping(reconnect=True, attempts=3, delay=5)
    return MYSQL_CONNECTION.cursor()

# Time Constants
MINUTE_IN_SECONDS=60
HOUR_IN_SECONDS=3600
DAY_IN_SECONDS=86400

# Points Constants
POINTS_FOR_CORRECT_QUIZ_ANSWER=5
POINTS_FOR_CORRECT_QUESTION_ANSWER=10
POINTS_FOR_CORRECT_FLASH_QUESTION_ANSWER=100

POINTS_FOR_FIRST_DAILY_MESSAGE=10
POINTS_FOR_MESSAGE=1

'''
For local testing with sqlite3

- Uncomment below code blocks
- Uncomment import of sqlite3 above
- Comment out mysql.connector code blocks above
- Ensure points.db exists in the resources/database/ directory
- Adjust code in points.py accordingly
  - Replacing MYSQL_CONNECTION with SQLITE_CONNECTION
  - Adjusting SQL syntax where necessary such as %s to ?
'''
# Access to SQLite Database Files
# POINTS_DB_PATH=os.path.join(os.getcwd(), f'ducke\\resources\\database\\points.db')

# SQLite Connection
# SQLITE_CONNECTION = sqlite3.connect(POINTS_DB_PATH)