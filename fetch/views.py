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
		req = 				json.loads(request.body.decode('utf-8'))
		entity = 			req['entity']
		breakdown = 		req['breakdown']
		objective = 		req['objective']
		account_currency = 	req['account_currency']
		entity_id = 		''
		billing_event = 	''
		optimization_goal = ''

		if entity + '_id' in req:			entity_id = req[entity + '_id']
		if 'billing_event' in req:			billing_event = req['billing_event']
		if 'optimization_goal' in req:		optimization_goal = req['optimization_goal']

		db = connect_db('diana')
		for key in RESULT[breakdown].keys():
			print(entity, breakdown, objective, account_currency, key)
			query_obj = {
				'breakdowns':			[breakdown],
				'objective':			objective,
				'account_currency':		account_currency,
			}
			if entity_id: 					query_obj[entity + '_id']		= entity_id
			if billing_event: 				query_obj['billing_event'] 		= billing_event
			if optimization_goal: 			query_obj['optimization_goal'] 	= optimization_goal
			if not breakdown == 'none': 	query_obj[breakdown] 			= key
			
			print(query_obj)
			entities = list(db['stats_' + entity].find(query_obj))
			if not entities: continue
			if not float(entities[0]['impressions']) * float(entities[0]['clicks']): continue
			# print(entities)
			print(len(entities))
			spends = 						[float(entity['spend']) for entity in entities if 'spend' in entity]
			impressions = 					[float(entity['impressions']) for entity in entities if 'impressions' in entity]
			reaches = 						[float(entity['reach']) for entity in entities if 'reach' in entity]
			clicks = 						[float(entity['clicks']) for entity in entities if 'clicks' in entity]
			inline_link_clicks = 			[float(entity['inline_link_clicks']) for entity in entities if 'inline_link_clicks' in entity]
			inline_link_click_ctrs = 		[float(entity['inline_link_click_ctr']) for entity in entities if 'inline_link_click_ctr' in entity]
			outbound_clicks = 				[float(entity['outbound_clicks'][0]['value']) for entity in entities if 'outbound_clicks' in entity]
			outbound_clicks_ctrs = 			[float(entity['outbound_clicks_ctr'][0]['value']) for entity in entities if 'outbound_clicks_ctr' in entity]
			cost_per_outbound_clicks = 		[float(entity['cost_per_outbound_click'][0]['value']) for entity in entities if 'cost_per_outbound_click' in entity]
			cost_per_inline_link_clicks =	[float(entity['cost_per_inline_link_click']) for entity in entities if 'cost_per_inline_link_click' in entity]
			cost_per_total_actions = 		[float(entity['cost_per_total_action']) for entity in entities if 'cost_per_total_action' in entity]
			cpms = 							[float(entity['cpm']) for entity in entities if 'cpm' in entity]
			cpcs = 							[float(entity['cpc']) for entity in entities if 'cpc' in entity]
			ctrs = 							[float(entity['ctr']) for entity in entities if 'ctr' in entity]
			frequencys = 					[float(entity['frequency']) for entity in entities if 'frequency' in entity]

			RESULT[breakdown][key] = {
				'objective':						entities[0]['objective'],
				'avg_cpm' : 						round(sum(spends)/sum(impressions)*1000, 2),
				'avg_cpc' : 						round(sum(spends)/sum(clicks), 2),
				'avg_frequency' : 					round(sum(impressions)/sum(reaches), 2),
				'avg_ctr' : 						round(sum(clicks)/sum(impressions)*100, 2),
				'avg_cost_per_inline_link_click' : 	round(sum(spends)/sum(inline_link_clicks), 2),
				'avg_cost_per_outbount_click' : 	round(sum(spends)/sum(outbound_clicks), 2),
				'med_cpm' : 						round(median(cpms), 2),
				'med_cpc' : 						round(median(cpcs), 2),
				'med_frequency' : 					round(median(frequencys), 2),
				'med_ctr' : 						round(median(ctrs), 2),
				'med_cost_per_inline_link_click' :	round(median(cost_per_inline_link_clicks), 2),
				'med_cost_per_outbound_click' : 	round(median(cost_per_outbound_clicks), 2),
				'med_cost_per_total_action' : 		round(median(cost_per_total_actions), 2),
			}
		RESULT[breakdown]['currency'] = account_currency
		print(RESULT[breakdown])
		return HttpResponse(json.dumps(RESULT[breakdown]).encode('utf-8'))
	return HttpResponse(json.dumps("error").encode('utf-8'))

	
# Control View
def get_users(db):
	return list(db['userinfo'].find())

def get_adaccounts(user):
	url = 'https://graph.facebook.com/v2.12/' + user['user_id'] + '/adaccounts?access_token=' + user['long_access_token']
	response = requests.get(url).json()
	# print(response)
	try: return response['data']
	except Exception as e: return []

def nocap_check(db, adaccounts):
	nocap_list = list(db['nocap_list'].find())
	new_adaccounts = list(set([adaccount['account_id'] for adaccount in adaccounts]) - set([nocap['adaccount'] for nocap in nocap_list]))
	result = []
	for new_adaccount in new_adaccounts:
		result.append(
			{
				'account_id':	new_adaccount,
				'id': 			'act_' + new_adaccount,
			}
		)
	return result

def get_entities_list(db, user, adaccount, entity):
	params = {'date_preset': 'last_30d'}
	url = 'https://graph.facebook.com/v2.12/' + adaccount['id'] + '/' + entity + 's?access_token=' + user['long_access_token']
	headers = {'Content-Type': 'application/json; charset=utf-8', 'content-encoding': 'gzip'}
	response = requests.get(url, params=params, headers=headers)
	response = response.json()
	print('-'*10)
	# print(response)
	print(user['username'], adaccount, entity)
	print('-'*10)
	if 'error' in response:
		if response['error']['code'] == 3:
			print("Application does not have the capability to make this API call.")
			return update_nocap_list(db, user, adaccount, entity)
		if response['error']['code'] == 17:
			# return []
			print("reach api limit, wait {} seconds and retry".format(TIME['limit_wait_time']))
			time.sleep(TIME['limit_wait_time'])
			response['data'] = get_entities_list(db, user, adaccount, entity)
	try: return response['data']
	except Exception as e: return []

def get_entity_field_values(db, user, adaccount, entity, entity_type):
	params = {'date_preset': 'last_90d'}
	if entity_type != 'adset': return []
	params['fields'] = str([
		'id',
		'account_id',
		'campaign_id',
		'name',
		'billing_event',
		'budget_remaining',
		'daily_budget',
		'lifetime_budget',
		'optimization_goal',
	])
	url = 'https://graph.facebook.com/v2.12/' + entity['id'] + '?access_token=' + user['long_access_token']
	headers = {'Content-Type': 'application/json; charset=utf-8', 'content-encoding': 'gzip'}
	response = requests.get(url, params=params, headers=headers)
	response = response.json()
	print('-'*30)
	print(response)
	print(user['username'], adaccount, entity)
	print('-'*30)
	if 'error' in response:
		if response['error']['code'] == 3:
			print("Application does not have the capability to make this API call.")
			return update_nocap_list(db, user, adaccount, entity)
		if response['error']['code'] == 17:
			# return []
			print("reach api limit, wait {} seconds and retry".format(TIME['limit_wait_time']))
			time.sleep(TIME['limit_wait_time'])
			response = get_entity_field_values(db, user, adaccount, entity, entity_type)
	try: return response
	except Exception as e: return []

def get_entity_insights(user, entity_name, entity, breakdowns):
	fields = FIELDS[entity_name]
	params = {
		'fields': 			str(fields),
		'date_preset': 		'last_90d',
		'time_increment': 	'all_days',
		'breakdowns': 		str(breakdowns),
	}
	url = 'https://graph.facebook.com/v2.12/' + entity['id'] + '/insights?access_token=' + user['long_access_token']
	headers = {'Content-Type': 'application/json; charset=utf-8', 'content-encoding': 'gzip'}
	response = requests.get(url, params=params, headers=headers)
	response = response.json()
	print('-'*10)
	# print(response)
	print(user['username'], entity_name, entity, breakdowns)
	print('-'*10)
	if 'error' in response:
		if response['error']['code'] == 17:
			# return []
			print("reach api limit, wait {} seconds and retry".format(TIME['limit_wait_time']))
			time.sleep(TIME['limit_wait_time'])
			response['data'] = get_entity_insights(user, entity_name, entity, breakdowns)
	try: return response['data']
	except Exception as e: return []

def update_db(db, collection, id_field, insights, breakdown):
	stats = db[collection]
	for insight in insights:
		insight['breakdowns'] = breakdown
		if not breakdown: insight['breakdowns'] = ['none']
		insight['updated_time'] = datetime.datetime.now()
		stats.replace_one(
			{
				id_field: 		insight[id_field],
				'breakdowns': 	insight['breakdowns'],
			},
			insight,
			upsert=True,
		)
	return print("update_db done")

def update_field_values(db, user, field_values, breakdown):
	stats_adset = db['stats_adset']
	if not breakdown: breakdown = ['none']
	stats_adset.update(
		{
			'adset_id': 	field_values['id'],
			'breakdowns': 	breakdown,
		},
		{
			'$set': {
				'billing_event': 		field_values['billing_event'],
				'budget_remaining': 	field_values['budget_remaining'],
				'daily_budget': 		field_values['daily_budget'],
				'lifetime_budget': 		field_values['lifetime_budget'],
				'optimization_goal': 	field_values['optimization_goal'],
			}
		}
	)
	return print("update_field_values done")

def update_nocap_list(db, user, adaccount, entity):
	nocap_list = db['nocap_list']
	replace_data = {
		'user':			user['username'],
		'adaccount':	adaccount['account_id'],
		'entity':		entity,
		'updated_time':	datetime.datetime.now(),
	}
	nocap_list.replace_one(
		{
			'adaccount':adaccount['id'],
		},
		replace_data,
		upsert=True,
	)
	print("update_nocap_list done")
	return "nocap"

def fetch_all():
	start_time = time.time()
	#------------------------
	db = 		connect_db('notification')
	users = 	get_users(db)
	db = 		connect_db('diana')
	
	for user in users:
		adaccounts = get_adaccounts(user)
		# adaccounts = nocap_check(db, adaccounts)
		breakdowns = [['age'], ['gender'], ['country'], ['publisher_platform'], []]
		for breakdown in breakdowns:
			for adaccount in adaccounts:
				entity_types = ['campaign', 'adset', 'ad']
				# entity_types = ['adset']
				for entity_type in entity_types:
					entities = get_entities_list(db, user, adaccount, entity_type)
					time.sleep(TIME['loop_wait_time'])
					if entities == "nocap": break
					for entity in entities:
							insights = get_entity_insights(user, entity_type, entity, breakdown)
							if insights:
								update_db(db, 'stats_' + entity_type, entity_type + '_id', insights, breakdown)
								time.sleep(TIME['loop_wait_time'])
								field_values = get_entity_field_values(db, user, adaccount, entity, entity_type)
								if field_values: update_field_values(db, user, field_values, breakdown)

	#------------------------
	print("start_time", start_time)
	print("--- %s seconds ---" %(time.time() - start_time))
	return print("fetch_all done -- {}".format(datetime.datetime.now()))
