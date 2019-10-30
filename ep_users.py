#!/usr/bin/env python
import json
import requests
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

csvfile = "ep_users.csv"
with open(csvfile, "a") as output:
	writer = csv.writer(output, lineterminator='\n')
	writer.writerow( ['userid', 'escalation', 'policy,username'])
	

#API_ACCESS_KEY='Msz4iBvMUp4FMRCm_Mr5'
API_ACCESS_KEY='jv7CXR3xTmyJ5i2rAMXy'
BASE_URL = 'https://api.pagerduty.com'
HEADERS = {
		'Accept': 'application/vnd.pagerduty+json;version=2',
		'Authorization': 'Token token={token}'.format(token=API_ACCESS_KEY),
		'Content-type': 'application/json'
	}

user_count = 0
ep_count = 0

def get_user_count():
	global user_count
	count = requests.get(BASE_URL + '/users', headers=HEADERS, params='total=true')
	user_count = count.json()['total']
	print(str(user_count))
	
def get_ep_count(userid):
	global ep_count
	query = { 
			'user_ids[]':userid,
			'total': 'true'
		}
	count = requests.get(BASE_URL + '/escalation_policies', headers=HEADERS, params=query)
	#print(count.json())
	ep_count = count.json()['total']
	#print(str(ep_count))

def write_csv(row):
	with open(csvfile, 'a') as output:
		writer = csv.writer(output, lineterminator='\n')
		#print(row)
		writer.writerow(row)
		
def get_users(offset):
	global user_count
	global ep_count
	params = {
		'offset':offset
	}
	all_users = requests.get(BASE_URL + '/users', headers=HEADERS, params=params)
	for user in all_users.json()['users']:
		#print(user['name'])
		get_ep_count(user['id'])
		#print(str(ep_count))
		if ep_count != 0:
			for offset in xrange(0,ep_count):
				if offset % 25 == 0:
					params = {
						'offset':offset,
						'user_ids[]':user['id']
					}
					all_eps = requests.get(BASE_URL + '/escalation_policies', headers=HEADERS, params=params)
				#print(all_eps.json())
				for ep in all_eps.json()['escalation_policies']:
					row = [user['id'], ep['summary'], user['name']]
					write_csv(row)
		else:
			row = [user['id'], 'none', user['name']]
			write_csv(row)
	    	
def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	get_user_count()
	for offset in xrange(0,user_count):
		if offset % 25 == 0:
			get_users(offset)
	

if __name__=='__main__':
	sys.exit(main())
