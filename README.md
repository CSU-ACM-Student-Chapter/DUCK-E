# DUCK-E
DUCK-E is a fun and interactive bot designed for Computer Science and Tech communities platformed on discord. It's core objective is to create a fun and interactive space for learning and discussion amongst its server members. This bot was created and is maintained by students at Columbus State University within the ACM Chapter. The duck represents the official mascot for the ACM @ CSU organization and is beloved by all. We hope you enjoy our project. :grinning:

## Commands
- **/announcement** (Planned) Announces the message at the specified date and time.
- **/ping** Tests bot latency. Helpful for performing health checks on the server.
- **/question** Posts a random multiple-choice question from a selected topic, allows reactions, and evaluates answers.
- **/question-flash-events** 'Quick event' questions are sent at random within a repeating frame that will continue until closed out by a mod or admin. 
- **/quiz** Posts multiple random questions from the chosen topic into a dedicated thread within the interactions channel. Great for studying!
> [!NOTE]
> /question-flash-events and /quiz are currently not in production
> /question-flash-events requires an end-task command which is currently not implemented.

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
For more information on features please refer to the [Issues Tab](https://github.com/CSU-ACM-Student-Chapter/DUCK-E/labels). At a high level this will provide a(n):

- Interactive Command Prompt
- Member Points System
- Club Info Reporting
- Daily Trivia Question Posts

# Credits
DUCK-E picture: [flikr - Jo Blakely](https://flickr.com/photos/pickledjo/)
