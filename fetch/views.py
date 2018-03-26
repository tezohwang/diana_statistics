from django.shortcuts import render

from .database import connect_db
from .constant import FIELDS

import requests

# Create your views here.

# Routing View

# Control View
def get_users(db):
	return list(db['userinfo'].find())

def get_adaccounts(user):
	url = 'https://graph.facebook.com/v2.11/' + user['user_id'] + '/adaccounts?access_token=' + user['long_access_token']
	response = requests.get(url).json()
	# print(response)
	try:
		return response['data']
	except Exception as e:
		return []

def get_campaigns_list(user, adaccount):
	params = {
		# 'effective_status': "['ACTIVE', 'PAUSED', 'CAMPAIGN_PAUSED', 'ADSET_PAUSED']",
		'date_preset': 'lifetime',
	}
	url = 'https://graph.facebook.com/v2.11/' + adaccount['id'] + '/campaigns?access_token=' + user['long_access_token']
	response = requests.get(url, params=params).json()
	print(response)
	try:
		return response['data']
	except Exception as e:
		return []

def get_ads_list(user, adaccount):
	params = {
		'effective_status': "['ACTIVE', 'PAUSED', 'CAMPAIGN_PAUSED', 'ADSET_PAUSED']",
		'date_preset': 'lifetime',
	}
	url = 'https://graph.facebook.com/v2.11/' + adaccount['id'] + '/ads?access_token=' + user['long_access_token']
	response = requests.get(url, params=params).json()
	# print(response)
	try:
		return response['data']
	except Exception as e:
		return []

def get_campaign_insights(user, campaign, breakdowns):
	fields = FIELDS
	params = {
		'fields': str(fields),
		'date_preset': 'lifetime',
		'time_increment': 'all_days',
		'breakdowns': str('["' + breakdowns + '"]'),
	}
	# print(params)

	url = 'https://graph.facebook.com/v2.11/' + campaign['id'] + '/insights?access_token=' + user['long_access_token']
	response = requests.get(url, params=params).json()
	# print(response)
	# print(len(response['data']))
	try:
		return response['data']
	except Exception as e:
		return []

def get_ad_insights(user, ad):
	fields = FIELDS
	params = {
		'fields': str(fields),
		'date_preset': 'lifetime',
		'time_increment': 'all_days',
	}

	url = 'https://graph.facebook.com/v2.11/' + ad['id'] + '/insights?access_token=' + user['long_access_token']
	response = requests.get(url, params=params).json()
	# print(len(response['data']))
	try:
		return response['data']
	except Exception as e:
		return []

def update_db(db, insight):
	stats = db['stats_campaign']
	stats.replace_one(
		{
			'campaign_id':insight['campaign_id'],
		},
		insight,
		upsert=True,
	)
	return print("update_db done")

def fetch_all():
	db = connect_db('notification')
	users = get_users(db)
	db = connect_db('diana')
	for user in users:
		adaccounts = get_adaccounts(user)

		for adaccount in adaccounts:
			campaigns = get_campaigns_list(user, adaccount)
			# print(campaigns)

			for campaign in campaigns:
				insights_age = get_campaign_insights(user, campaign, 'age')
				insights_gender = get_campaign_insights(user, campaign, 'gender')
				# insights_region = get_campaign_insights(user, campaign, 'region')
				insights_country = get_campaign_insights(user, campaign, 'country')
				insights_platform = get_campaign_insights(user, campaign, 'publisher_platform')
				# print(insights_age)

	return print("fetch_all done")
