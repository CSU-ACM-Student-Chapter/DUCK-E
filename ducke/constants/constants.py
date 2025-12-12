import os

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

# Access to Resources Folder
RESOURCES_FOLDER= os.path.join(os.getcwd(), f'ducke\\resources\\')
RESOURCES_QUESTIONS_FOLDER= os.path.join(os.getcwd(), f'ducke\\resources\\questions\\')
RESOURCES_RESPONSES_FOLDER= os.path.join(os.getcwd(), f'ducke\\resources\\responses\\')

# Access to all Files within Resources Folder
RESOURCES_QUESTIONS_AZ_900_FILE= os.path.join(os.getcwd(), f'ducke\\resources\\questions\\az 900.csv')
RESOURCES_QUESTIONS_DATA_STRUCTURES_FILE=os.path.join(os.getcwd(), f'ducke\\resources\\questions\\data structure basics.csv')
RESOURCES_QUESTIONS_NETWORKING_BASICS_FILE=os.path.join(os.getcwd(), f'ducke\\resources\\questions\\networking basics.csv')

RESOURCES_RESPONSES_QUESTION_CHEATER= os.path.join(os.getcwd(), f'ducke\\resources\\responses\\question_cheater.txt')
RESOURCES_RESPONSES_QUESTION_CORRECT= os.path.join(os.getcwd(), f'ducke\\resources\\responses\\question_correct.txt')
RESOURCES_RESPONSES_QUESTION_INCORRECT= os.path.join(os.getcwd(), f'ducke\\resources\\responses\\question_incorrect.txt')

ACCESS_REQUEST_MESSAGE="❌ I don't have permissions to complete this command in this channel. Please grant access in the Discord Developer Portal."

POINTS_DB_PATH=os.path.join(os.getcwd(), f'ducke\\resources\\database\\points.db') #For local testing with sqlite
FLASH_EVENTS_DB_PATH=os.path.join(os.getcwd(), f'ducke\\resources\\database\\flash_events.db')  #For local testing with sqlite

MINUTE_IN_SECONDS=60
HOUR_IN_SECONDS=3600
DAY_IN_SECONDS=86400