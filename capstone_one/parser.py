import smtplib
import ssl
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm
import numpy as np
import re


## The main parse function. This pulls the p and ul tags in a description field

def parser(url):
    try:
        result = urllib.request.urlopen(url)
        soup = BeautifulSoup(result.read(), features = 'html.parser'))

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
        return ('This Error: Missing Description', np.nan, np.nan, None)
    except Exception as e:
        return ("This Error: " + str(e), np.nan, np.nan, None)


## Start of script

df = pd.read_pickle('kickstarter.pkl')

## library to track progresses in command line
tqdm.pandas()

df['description'] = df['web_url'].progress_apply(parser)

df.to_pickle('kickstarter_desc.pkl')


## Send an email when process is finished
port = 465
password = 'PASSWORD'
context = ssl.create_default_context()
msg = """\
Subject: End of Script

Your Script had ended."""


email = 'EMAIL@EMAIL.COM'

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    server.sendmail(email, email, msg)
