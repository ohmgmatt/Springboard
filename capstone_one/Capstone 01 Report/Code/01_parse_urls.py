import smtplib
import ssl
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm
import numpy as np
import re

## Set up email
port = 465
password = 'PASSWORD'
context = ssl.create_default_context()
email = 'EMAIL@EMAIL.COM'


## Set up error counting
err_count = 0
multi_count = 1

## This function will send an email at 10,100,1000,10000 errors.
def errorCheck():
    global err_count
    global multi_count
    global port
    global context
    global email
    
    err_count +=1
    if err_count >= 10 ** multi_count:
        error_msg = "There are {} errors".format(err_count)
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(email, password)
            server.sendmail(email, email, error_msg)
        err_count = 0
        multi_count += 1


## The main parse function. This pulls in:
## the p tags and ul tags
## the img count and video counts
## the pledge amount information
def parser(url):
    try:
        result = urllib.request.urlopen(url)
        soup = BeautifulSoup(result.read(), features = 'html.parser')

        # Pulling the description fields
        desc = soup.find('div', 'full-description')
        textfield = '\n'.join([item.text for item in desc.find_all(['p','ul'])])

        # Pulling the image counts and video counts
        img = len(desc.find_all('img'))
        vid = len(desc.find_all('video'))
        img_count = img - vid

        # Pulling the rewards for the project into a single list
        pledges = []
        for pledge in soup.find_all('div', 'pledge__info'):
            amount = pledge.find('span', 'money').text
            i = re.search("[0-9]", amount)
            pledge = amount[i.start():]
            pledge = int(pledge.replace(',', ''))
            pledges.append(pledge)

        return(textfield, img_count, vid, pledges)

    except AttributeError:
        errorCheck()
        return ('This Error: Missing Description', np.nan, np.nan, None)

    except Exception as e:
        errorCheck()
        return ("This Error: " + str(e), np.nan, np.nan, None)

## Start of script

df = pd.read_pickle('kickstarter.pkl')

## library to track progresses in command line
tqdm.pandas()

df['description'] = df['web_url'].progress_apply(parser)

df.to_pickle('kickstarter_desc.pkl')


## Email when process is finished
ending = """\
Subject: End of Script

Your Script had ended."""

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    server.sendmail(email, email, ending)
