# DUCK-E
DUCK-E is a fun and interactive bot designed for Computer Science and Tech communities platformed on discord. It's core objective is to create a fun and interactive space for learning and discussion amongst its server members. This bot was created and is maintained by students at Columbus State University within the ACM Chapter. The duck represents the official mascot for the ACM @ CSU organization and is beloved by all. We hope you enjoy our project. 😄

## Commands
### Trivia and Studying
- _**/flash-events-start**_ One 'Quick event' question will be sent at random on a daily occurence. Those on that're able to answer quickly and correctly will be rewarded a generous amount of server points.
- _**/flash-events-stop**_ Stops the flash-events in the channel where the command was given. **(Admin Only)**
- _**/question**_ Posts a random multiple-choice question from a selected topic, allows reactions, and evaluates answers.
- _**/quiz**_ Posts multiple random questions from the chosen topic into a dedicated thread within the interactions channel. Great for studying!
### Member Points
- _**/add-points**_ Provided the user and amount of points. Will add the given the amount to the named user. **(Admin Only)**
- _**/leaderboard**_ Returns the Top 10 Users with the highest point value
- _**/my-points**_ Returns user points
- _**/remove-points**_ Provided the user and amount of points. Will remove the given the amount from the named user. **(Admin Only)**
### Client Server Comms
- _**/ping**_ Tests bot latency. Helpful for performing health checks on the server.

# Getting Started
All code should be tested and approved by a 2nd developer prior to integrating code with main. To test, please walkthrough the information listed on how to get started locally.

## Grabbing the repo
Create a branch based off main. It is recommended to name it after the task being done but `{Name}'s First Bot` will suffice if unsure of what to pick up at first.
 
## Optional:
#### Virual Environment
- A python virtual environment to run on
    - `python -m venv myenv`

## Required:

#### Python
- Python 3.9+
- Packages
    - `pip install requirements.txt -r`
    - **Warning :warning::** If skipped and package versions are off far enough, your code may break once pushed to production. Please be cautious of this when skipping this command.

#### Discord Bot
- Add a *.env* file
    - Create a *.env* file at the root of the project directory.
    - Insert `DISCORD_TOKEN=your-token-here`
    - We'll come back here shortly to enter this token
- Creating a discord bot token and bot placed
on a server for testing
    - This video will kindly walk you through all the needed steps.
    [Creating a Discord Bot in Python (2025) | Episode 1: Setup & Basics](https://www.youtube.com/watch?v=CHbN_gB30Tw)
        - No need to implement their code, although all is helpful and recommended for beginners to watch
        - **Key time stamps:** 1:15-7:15, 13:51-16:10
        - **Note:** In the 2nd portion, you will instead add your token to *.env*

## Going past the first run 🫡
- Open the [Issues Tab](https://github.com/CSU-ACM-Student-Chapter/DUCK-E/labels) and look for **good first issue**. This will help you gain good footing and understanding of the repo while still contributing to important tasks.
    - Once complete, submit a PR and notify the *@Bot Programmer* role members in the ACM discord, a kept up to date link of our discord channel is provided [here](https://csuinvolve.columbusstate.edu/organization/computermachinery).
- Feel free to read up on some other issues, TODOs, and discussion plans. Your help is greatly appreciated!! :heart:

# Future Features
For more information on planned features please refer to the [Issues Tab](https://github.com/CSU-ACM-Student-Chapter/DUCK-E/labels).
At a high level this will provide:

- Personal studying material - _/add-subject_, _/remove-subjuct_
- Study Progress Tracking - _/quiz-progress-chart_
- Club Info Reporting - _/announcements_
- Board Games - _/start-game_
- Board Game Server Tournaments - /start-game-tournament

# Credits
DUCK-E picture: [flikr - Jo Blakely](https://flickr.com/photos/pickledjo/)
