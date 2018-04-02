from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .database import connect_db
from .constant import FIELDS, TIME, RESULT

import requests, time, datetime, json, gzip
from statistics import median

# Create your views here.

# Routing View
@csrf_exempt
def stats(request):
	if request.method == "POST":
		req = json.loads(request.body.decode('utf-8'))
		entity = req['entity']
		breakdown = req['breakdown']
		objective = req['objective']
		account_currency = req['account_currency']
		# print(entity, breakdown, objective, account_currency)

		db = connect_db('diana')
		for key in RESULT[breakdown].keys():
			print(breakdown, key)
			entities = list(db['stats_' + entity].find({
					'breakdowns':[breakdown],
					'objective':objective,
					'account_currency':account_currency,
					breakdown:key,
				})
			)
			if not entities:
				continue
			if not float(entities[0]['impressions']) * float(entities[0]['clicks']):
				continue
			# print(entities)

			spends = [float(entity['spend']) for entity in entities]
			impressions = [float(entity['impressions']) for entity in entities]
			reaches = [float(entity['reach']) for entity in entities]
			clicks = [float(entity['clicks']) for entity in entities]
			cpms = [float(entity['cpm']) for entity in entities]
			cpcs = [float(entity['cpc']) for entity in entities]
			ctrs = [float(entity['ctr']) for entity in entities]
			frequencys = [float(entity['frequency']) for entity in entities]

			RESULT[breakdown][key] = {
				'avg_cpm' : sum(spends)/sum(impressions)*1000,
				'avg_cpc' : sum(spends)/sum(clicks),
				'avg_frequency' : sum(impressions)/sum(reaches),
				'avg_ctr' : sum(clicks)/sum(impressions)*100,
				'med_cpm' : median(cpms),
				'med_cpc' : median(cpcs),
				'med_frequency' : median(frequencys),
				'med_ctr' : median(ctrs),
			}
		RESULT[breakdown]['currency'] = account_currency
		return HttpResponse(json.dumps(RESULT[breakdown]))
	return HttpResponse("error")

	
# Control View
def get_users(db):
	return list(db['userinfo'].find())

def get_adaccounts(user):
	url = 'https://graph.facebook.com/v2.12/' + user['user_id'] + '/adaccounts?access_token=' + user['long_access_token']
	response = requests.get(url).json()
	# print(response)
	try:
		return response['data']
	except Exception as e:
		return []

def get_entities_list(user, adaccount, entity):
	params = {'date_preset': 'last_90d'}
	url = 'https://graph.facebook.com/v2.12/' + adaccount['id'] + '/' + entity + 's?access_token=' + user['long_access_token']
	headers = {'Content-Type': 'application/json; charset=utf-8', 'content-encoding': 'gzip'}
	response = requests.get(url, params=params, headers=headers)
	# headers = response.headers
	response = response.json()
	print('-'*10)
	print(response)
	# print(headers)
	print(user['username'], adaccount, entity)
	print('-'*10)
	if 'error' in response:
		if response['error']['code'] == 17:
			print("reach api limit, wait {} seconds and retry".format(TIME['limit_wait_time']))
			time.sleep(TIME['limit_wait_time'])
			response['data'] = get_entities_list(user, adaccount, entity)
	try:
		return response['data']
	except Exception as e:
		return []

def get_entity_insights(user, entity_name, entity, breakdowns):
	fields = FIELDS[entity_name]
	params = {
		'fields': str(fields),
		'date_preset': 'last_90d',
		'time_increment': 'all_days',
		'breakdowns': str(breakdowns),
	}
	url = 'https://graph.facebook.com/v2.12/' + entity['id'] + '/insights?access_token=' + user['long_access_token']
	headers = {'Content-Type': 'application/json; charset=utf-8', 'content-encoding': 'gzip'}
	response = requests.get(url, params=params, headers=headers)
	# headers = response.headers
	response = response.json()
	print('-'*10)
	print(response)
	# print(headers)
	print(user['username'], entity_name, entity, breakdowns)
	print('-'*10)
	if 'error' in response:
		if response['error']['code'] == 17:
			print("reach api limit, wait {} seconds and retry".format(TIME['limit_wait_time']))
			time.sleep(TIME['limit_wait_time'])
			response['data'] = get_entity_insights(user, entity_name, entity, breakdowns)
	try:
		return response['data']
	except Exception as e:
		return []

def update_db(db, collection, id_field, insights, breakdowns):
	stats = db[collection]
	for insight in insights:
		insight['breakdowns'] = breakdowns
		if not breakdowns:
			insight['breakdowns'] = ['none']
		insight['updated_time'] = datetime.datetime.now()
		stats.replace_one(
			{
				id_field: insight[id_field],
				'breakdowns': insight['breakdowns'],
			},
			insight,
			upsert=True,
		)
	return print("update_db done")

def fetch_all():
	start_time = time.time()
	#------------------------
	db = connect_db('notification')
	users = get_users(db)
	db = connect_db('diana')
	
	for user in users:
		adaccounts = get_adaccounts(user)
		breakdowns = [['age'], ['gender'], ['country'], ['publisher_platform'], []]
		for breakdown in breakdowns:
			for adaccount in adaccounts:
				entity_types = ['campaign', 'adset', 'ad']
				for entity_type in entity_types:
					entities = get_entities_list(user, adaccount, entity_type)
					time.sleep(TIME['loop_wait_time'])
					for entity in entities:
							insights = get_entity_insights(user, entity_type, entity, breakdown)
							update_db(db, 'stats_' + entity_type, entity_type + '_id', insights, breakdown)
							time.sleep(TIME['loop_wait_time'])
	#------------------------
	print("start_time", start_time)
	print("--- %s seconds ---" %(time.time() - start_time))
	return print("fetch_all done -- {}".format(datetime.datetime.now()))
