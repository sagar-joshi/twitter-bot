import sys
import json
import urllib.parse
import requests
from requests_oauthlib import OAuth1
from keys import client_key, client_secret


def req_token():
	request_token_url='https://api.twitter.com/oauth/request_token'
	oauth=OAuth1(client_key,client_secret=client_secret)
	r=requests.post(url=request_token_url,auth=oauth)
	cred=urllib.parse.parse_qs(r.text)
	resource_owner_key=cred.get('oauth_token')[0]
	resource_owner_secret=cred.get('oauth_token_secret')[0]
	base_authorization_url = 'https://api.twitter.com/oauth/authorize'
	authorize_url = base_authorization_url + '?oauth_token='
	authorize_url = authorize_url + resource_owner_key
	ret={
	"temp_access_key":resource_owner_key,
	"temp_access_secret":resource_owner_secret,
	"authorize_url":authorize_url
	}
	ret=json.dumps(ret)
	print (ret)


req_token()

