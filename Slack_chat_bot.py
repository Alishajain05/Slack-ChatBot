import os
import json
import requests
import time
import random


from flask import Flask, request, Response


from bs4 import BeautifulSoup
import requests
from urllib import quote_plus
from pprint import pprint

MY_BOT = "alisha_bot"
MY_USERNAME = "alishajain05"

RESPOND_TO_PROF_KEYWORD = "&lt;BOTS_RESPOND&gt;"
RESPOND_TO_PROF_MSG = "Hello, my name is {0}. I belong to {1}. I live at {2}."
CODING_HELP_KEYWORD = "&lt;I_NEED_HELP_WITH_CODING&gt;"

# api_key = 'f12dc2d47dc0c501'
# desired_state = 'New Jersey'
# desired_city = 'Metuchen'
# zipcode = '08840'


application = Flask(__name__)


my_bot_name = MY_BOT #e.g. zac_bot
my_slack_username = MY_USERNAME #e.g. zac.wentzell

my_chatbot_name = 'zac_bot'

slack_inbound_url = 'https://hooks.slack.com/services/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'


def beautiful_soup_stack_overflow(question, tags=None, result_limit=5):
    print "entering bs4"
    answers_list = []
    base_stackoverflow_url = 'http://stackoverflow.com'
    stackoverflow_search_url = base_stackoverflow_url + '/search?q='
    parse_question = quote_plus(question)
    request_url = stackoverflow_search_url + parse_question
    response = requests.get(request_url).text
    soup = BeautifulSoup(response, "lxml")
    all_results = soup.findAll("div", {"class": "question-summary"})
    answers_list = []

    for question_summary in all_results:
        answered_accepted = None
        question_answered = None

        answered_accepted = question_summary.find('div', {'class': "statscontainer"}).find(
            'div', {'class': "stats"}).find('div', {'class': "answered-accepted"})

        question_answered = question_summary.find('div', {'class': "statscontainer"}).find(
            'div', {'class': "stats"}).find('div', {'class': "answered"})


        if (question_answered or answered_accepted) and len(answers_list) < result_limit:

            link = question_summary.find('div', {'class': "summary"}).find(
                'div', {'class': "result-link"}).find('a')['href']

            title = question_summary.find('div', {'class': "summary"}).find(
                'div', {'class': "result-link"}).find('a')['title']

            try:
                answers_count = question_summary.find('div', {'class': "statscontainer"}).find(
                    'div', {'class': "stats"}).find('div', {'class': "status"}).find('strong').text
            except Exception as e:
                # print e
                answers_count = 0

            date_asked = question_summary.find('div', {'class': "summary"}).find(
                'div', {'class': "started"}).find('span', {'class': 'relativetime'}).text.replace(" '",", 20")

            answers_list.append({'question': question, 'link': base_stackoverflow_url + str(link), 'title': str(title), 'date_asked': str(
                date_asked), 'answers_count': str(answers_count)})

    return answers_list


def flask_search_endpoint(search_text):
    print "inside flask search endpoint"
    print search_text
    answers = []
    if CODING_HELP_KEYWORD in search_text:
        print "stackoverflow search engine for ", search_text
        search_term = search_text.split(CODING_HELP_KEYWORD)[1].strip()
        answers = beautiful_soup_stack_overflow(search_term)
    return answers


def convert_for_slack(list_of_so_dicts):
    """
    input = [...,
    {'answers_count': '3',
    'date_asked': "Jun 17 '13",
    'link': 'http://stackoverflow.com/questions/17153498/how-to-find-duplicates-in-a-list-but-ignore-the-first-time-it-appears',
    'question': 'How to find duplicates in a list, but ignore the first time it appears?',
    'title': 'How to find duplicates in a list, but ignore the first time it appears?'},
    ]
    
    requirement: How to find duplicates in a list, but ignore the first time it appears? LINK (Links to an external site.) (3 responses) June 17, 2013
    """
    # all_messages = []
    # for data_dict in list_of_so_dicts:
    #     curr_message = data_dict.get('title') 
    #     curr_message += " <" + data_dict.get('link') + "|LINK> (Links to an external site.)"
    #     curr_message += " (" + data_dict.get('answers_count') + " responses) "
    #     curr_message += data_dict.get('date_asked')
    #     all_messages.append(curr_message)
    # return all_messages
    all_messages = str ('')
    for data_dict in list_of_so_dicts:
         curr_message = data_dict.get('title')
         curr_message += "\n" + " <" + data_dict.get('link') + "|LINK> (Links to an external site.)"
         curr_message += " (" + data_dict.get('answers_count') + " responses) "
         curr_message += data_dict.get('date_asked')
         all_messages= all_messages + curr_message
    return all_messages

# def weather_forecast(api_key, request_type):
#     weather_url = 'http://api.wunderground.com/api/' +api_key+ '/' +request_type+ 'forecast/q/' +desired_state+ '/' +desired_city+ '.json'
#     # request_url = requests.get(weather_url)
#     request_url = requests.get('http://api.wunderground.com/api/'+api_key+ '/' +request_type+ 'forecast/q/' +desired_state+ '/' +desired_city+ 'q/{0}.json'.format(zipcode))
#     json_url = json.loads(request_url.text)
#     return json_url

# this handles POST requests sent to your server at SERVERIP:41953/slack
@application.route('/slack', methods=['POST'])
def inbound():
    delay = random.uniform(0, 20)
    time.sleep(delay)

    print '========POST REQUEST @ /slack========='
    response = {'username': my_bot_name, 'icon_emoji': ':robot_face:', 'text': ''}
    print 'FORM DATA RECEIVED IS:'
    print request.form

    channel = request.form.get('channel_name','channel error') #this is the channel name where the message was sent from
    username = request.form.get('user_name','username error') #this is the username of the person who sent the message
    text = request.form.get('text','text error') #this is the text of the message that was sent
    # text = unicodedata.normalize('NFKD', request.form.get('text')).encode('ascii', 'ignore')
    inbound_message = username + " in " + channel + " says: " + text
    print '\n\nMessage:\n' + inbound_message
    
    if username != my_chatbot_name and username in [MY_USERNAME, 'zac.wentzell']:
    # if username in [my_slack_username, 'zac.wentzell']:
        # Your code for the assignment must stay within this if statement
        # if (username == my_slack_username) and (RESPOND_TO_PROF_KEYWORD in text):
        if RESPOND_TO_PROF_KEYWORD in text:
            print "Responding to professor"
            ip_address = "52.35.176.89"
            response['text'] = RESPOND_TO_PROF_MSG.format(my_bot_name, my_slack_username, ip_address)
            print response

        # stackoverflow search for me and prof
        if CODING_HELP_KEYWORD in text:
            search_engine_data = flask_search_endpoint(text)
            if search_engine_data:
                return_data = convert_for_slack(search_engine_data)
                if return_data:
                    response['text'] = return_data
                else:
                    response['text'] = 'My bot broke in the stack overflow engine'
        

        # A sample response:
        if text == "What's your favorite color?":
        # you can use print statments to debug your code
            print 'Bot is responding to favorite color question'
            response['text'] = 'Blue!'
            print 'Response text set correctly'

        # print response['text'], "<- before returning to bot"
        
        if slack_inbound_url and response['text']:
            r = requests.post(slack_inbound_url, json=response)
            print response['text'], "<- before returning to bot"
            print r.status_code and r.text

    print '========REQUEST HANDLING COMPLETE========\n\n'

    return Response(), 200


# this handles GET requests sent to your server at SERVERIP:41953/
@application.route('/', methods=['GET'])
def test():
    return Response('Your flask app is running!')


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=41953)
    # forecast_json = weather_forecast(api_key, 'forecast')
    # yesterday_json = weather_forecast(api_key, 'yesterday')
