import praw
import sys
import re
import json
import os
import time

#Global Variables
already_done = set()
new_ids = set()
prog = re.compile("spaceships*[.!?]*$", re.IGNORECASE)
prog2 = re.compile("spaceships*", re.IGNORECASE)

def load_visited_set():
    path = "/Users/harrison/Desktop/benny-bot/already-done.data"
    if os.path.isfile(path):
        f = open(path, 'r')
        for submission_id in f:
            already_done.add(submission_id.rstrip('\n'))
        f.close()

def append_visited_set(new_ids):
    #Finally, write out the additional ids
    f = open(path, 'a+')
    for new_id in new_ids:
        f.write(new_id)
        f.write("\n")
    f.close()

def check_subs_comments(r,subs): 
    print("Checking comments.")
    result = -1
    try:
        for subreddit_title in subs:
            subreddit = r.get_subreddit(subreddit_title)
            subreddit_comments = subreddit.get_comments()

            for comment in subreddit_comments:
                match = prog.search(comment.body)
                if match and (comment.submission.id not in already_done):
                    print("Commenting...")
                    print("\t"+comment.body)
                    #Matches the regular expression
                    try:
                        comment.reply("Hi! I'm Ben! But you can call me Benny! And I can build a Spaceship!")
                        new_id = comment.submission.id
                        already_done.add(new_id)
                        new_ids.add(new_id)
                        result = 1
                        break;
                    except:
                        return -1
    except:
        return result
    return result

def check_subs_submissions(r,subs): 
    print("Checking submissions.")
    result = -1
    try:
        for subreddit_title in subs:
            subreddit = r.get_subreddit(subreddit_title)
            subreddit_comments = subreddit.get_hot(limit=20)

            for submission in subreddit_comments:
                match = prog2.search(submission.title)
                if match and (submission.id not in already_done):
                    print("Commenting...")
                    print("\t"+submission.title)
                    #Matches the regular expression
                    try:
                        submission.add_comment("Hi! I'm Ben! But you can call me Benny! And I can build a Spaceship!")
                        new_id = submission.id
                        already_done.add(new_id)
                        new_ids.add(new_id)
                        result = 1
                        break;
                    except:
                        return -1
    except:
        return result
    return result

def main():
    if len(sys.argv) != 3:
        print("Usage: python benney-boy.py <username> <password>")

    username = sys.argv[1]
    password = sys.argv[2]

    #Load up Past Comments
    print("loading past comments...")
    load_visited_set()

    r = praw.Reddit('Benney-Bot Spaceship commenter v. 0.01 by hpincket see https://github.com/hpincket/benny-bot')
    r.login(username,password)
    
    #subs = ["test"]
    subs = ["test","funny","lego","gifs","gaming"]

    base = 2
    power = 3
    while(True):
        result = check_subs_comments(r,subs)
        result+= check_subs_submissions(r,subs)
        if result < 0 and power < 10:
            power+=1
        else:
            power-=1
        print("Sleeping for %d" % base**power)
        time.sleep(base**power)
    append_visited_set(new_ids)

main()
