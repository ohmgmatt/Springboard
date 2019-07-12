import smtplib
import ssl
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
from tqdm import tqdm


## The main parse function. This pulls the p and ul tags in a description field

def parser(url):
    try:
        result = urllib.request.urlopen(url)
        soup = BeautifulSoup(result.read())

        textfield = '\n'.join([item.text for item in soup.find(
                            'div', 'full-description').find_all(['p','ul'])])

        return(textfield)
    except AttributeError:
        return 'Missing Description'


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
