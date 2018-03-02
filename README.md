# Weasel
A tool for downloading details of stuff posted you've posted Facebook & Twitter and running some basic analysis on it for naughty stuff.

# Install Requirements

sudo python -m pip install -e git+https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk
sudo python -m pip install python-twitter

# Facebook Auth

Get an Access Token from teh Facebook Graph API Explorer https://developers.facebook.com/tools/explorer/

# Twitter Auth

Create the following dictionary in a file call twitter_auth.dict

{
  consumer_key='consumer_key',
  consumer_secret='consumer_secret',
  access_token_key='access_token',
  access_token_secret='access_token_secret'
}

A detailed guide for this can be found here https://python-twitter.readthedocs.io/en/latest/
