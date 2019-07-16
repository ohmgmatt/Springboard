import smtplib
import ssl
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm
import numpy as np


## The main parse function. This pulls the p and ul tags in a description field

def parser(url):
    try:
        result = urllib.request.urlopen(url)
        soup = BeautifulSoup(result.read(), features="lxml")
        desc = soup.find('div', 'full-description')

        textfield = '\n'.join([item.text for item in desc.find_all(['p','ul'])])

        img = len(desc.find_all('img'))
        vid = len(desc.find_all('video'))

        img_count = img - vid

        return(textfield, img_count, vid)
    except AttributeError:
        return ('Missing Description', np.nan, np.nan)
    except:
        return ('Wrong connection', np.nan, np.nan)


## Start of script

df = pd.read_pickle('kickstarter.pkl')
mini = df[:40]
## library to track progresses in command line
tqdm.pandas()

mini['parsed'] = mini['web_url'].progress_apply(parser)

mini.to_pickle('kickstarter_desc_mini.pkl')


## Send an email when process is finished
port = 465
password = 'PASSWORD'
context = ssl.create_default_context()
msg = """\
Subject: End of Script

Your Script had ended(MINI)."""


email = 'EMAIL@EMAIL.COM'

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    server.sendmail(email, email, msg)
