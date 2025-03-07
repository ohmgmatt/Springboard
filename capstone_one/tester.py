import smtplib
import ssl
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm
import numpy as np
import re


## Setting up email connection
port = 465
password = 'creamery'
context = ssl.create_default_context()
email = 'bonilla.matthew44@gmail.com'

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    server.sendmail(email, email, msg)

## The main parse function. This pulls the p and ul tags in a description field
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
        return ('This Error: Missing Description', np.nan, np.nan, None)
    except Exception as e:
        msg = """\
        Subject: Error Received

        This is a notification that your script has received an error. Please
        check after this has finished"""

        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(email, password)
            server.sendmail(email, email, msg)

        return ("This Error: " + str(e), np.nan, np.nan, None)



## Start of script

df = pd.read_pickle('kickstarter.pkl')
mini = df[5000:5040]

## library to track progresses in command line
tqdm.pandas()

mini['description'] = mini['web_url'].progress_apply(parser)

mini.to_pickle('kickstarter_desc_small.pkl')


## Send an email when process is finished
ending = """\
Subject: End of Script

Your Script had ended.(testing)"""


email = 'bonilla.matthew44@gmail.com'

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    server.sendmail(email, email, ending)
