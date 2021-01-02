import sys
import json
import urllib.parse
import requests
from requests_oauthlib import OAuth1
from keys import client_key, client_secret

def authenticate():
	resource_owner_key=sys.argv[1]
	resource_owner_secret=sys.argv[2]
	verifier=sys.argv[3]

	oauth=OAuth1(client_key,
				client_secret=client_secret,
				resource_owner_key=resource_owner_key,
				resource_owner_secret=resource_owner_secret,
				verifier=verifier)
	access_token_url = 'https://api.twitter.com/oauth/access_token'
	r = requests.post(url=access_token_url, auth=oauth)
	cred=urllib.parse.parse_qs(r.text)
	resource_owner_key=cred.get('oauth_token')[0]
	resource_owner_secret=cred.get('oauth_token_secret')[0]
	ret={
		"access_key":resource_owner_key,
		"access_secret":resource_owner_secret
	}
	ret=json.dumps(ret)
	print(ret)

authenticate()