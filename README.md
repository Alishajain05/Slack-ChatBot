# Slack-ChatBot

Implemented my learnings of APIs/Scraping/Flasks/Amazon Web Services/Processing data. Built a system that answers some questions via Slack.

Excecuted a REST API on an AWS Server that accepts POST requests. 

THe following tasks are being performed by the bot:

Task 1:
When you type in "<BOTS_RESPOND>" in #bot_chat(A Slack group where the bot responds). The bot should replies with:
"Hello, my name is INSERT_A_BOT_NAME_HERE. I belong to YOUR_NAME. I live at IP_ADDRESS."
e.g. my bot would respond like
"Hello, my name is alisha_bot. I belong to alishajain05. I live at 54.45.88.78."

Task 2:
When you type in "<I_NEED_HELP_WITH CODING>: THE_STUFF_YOU_WANT_TO_SEARCH"
e.g.
<I_NEED_HELP_WITH_CODING>: how to find duplicates in list python,
It returns a list of 5 StackOverflow questions that answer the question; it includes the title, a clickable link from Slack.
e.g.
alishajain05: <I_NEED_HELP_WITH_CODING>: how to find duplicates in list python
alisha_bot: How to find duplicates in a list, but ignore the first time it appears? LINK (Links to an external site.)Links to an external site. (3 responses) June 17, 2013
Python optimize how to find duplicate value and value index in a list LINK (Links to an external site.)Links to an external site. (4 responses), April 15 2015
...etc.

Task 3:
When you type in "<WHAT'S_THE_WEATHER_LIKE_AT>: SOME_ADDRESS_OR_ZIP"
THe bot responds with the current forecast for that area. 
alishajain05: <WHAT'S_THE_WEATHER_LIKE_AT>: 45 Main St Brooklyn, NY
zac_bot: Mostly Cloudy
60.1 °F
Feels Like 60.1 °F
N0.7
Wind Variable 
Gusts 2.2 mph
Tomorrow is forecast to be NEARLY THE SAME temperature as today.
Today
High 64 | Low 52 °F
20% Chance of Precip.
Yesterday
High 58.1 | Low 42.4 °F
Precip. 0 in

OR

alishajain05: <WHAT'S_THE_WEATHER_LIKE_AT>: 11201
zac_bot: Mostly Cloudy
60.1 °F
Feels Like 60.1 °F
N0.7
Wind Variable 
Gusts 2.2 mph
Tomorrow is forecast to be NEARLY THE SAME temperature as today.
Today
High 64 | Low 52 °F
20% Chance of Precip.
Yesterday
High 58.1 | Low 42.4 °F
Precip. 0 in

I used Open weather API to produce the output. 
