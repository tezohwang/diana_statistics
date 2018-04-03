# 앱에 쓰이는 상수 선언

DATABASE = {
    'diana': {
        'db_uri': 'mongodb://wizpace:wizpace0@52.78.216.222:27017/diana',
        'db_name': 'diana'
    },
    'notification': {
        'db_uri': 'mongodb://tezohwang:xowhghkd1!@ds113826.mlab.com:13826/diana_notification',
		'db_name': 'diana_notification'
    }
}
FB_APP = {
    'app_id': '1633923886632047',
    'app_secret': '4ec9658c91944be5fe71e0c20fcb3786'
}

FIELDS = {
    'campaign': [
        'account_id',
        'account_name',
        'account_currency',
        'campaign_id',
        'campaign_name',
        'objective',
        'actions',
        'spend',
        'impressions',
        'reach',
        'frequency',
        'cpm',
        'clicks',
        'ctr',
        'cpc',
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cost_per_outbound_click',
        'cost_per_inline_link_click',
        'cost_per_total_action',
        'relevance_score'
    ],
    'adset': [
        'account_id',
        'account_name',
        'account_currency',
        'campaign_id',
        'campaign_name',
        'adset_id',
        'adset_name',
        'objective',
        'actions',
        'spend',
        'impressions',
        'reach',
        'frequency',
        'cpm',
        'clicks',
        'ctr',
        'cpc',
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cost_per_outbound_click',
        'cost_per_inline_link_click',
        'cost_per_total_action',
        'relevance_score'
    ],
    'ad': [
        'account_id',
        'account_name',
        'account_currency',
        'campaign_id',
        'campaign_name',
        'adset_id',
        'adset_name',
        'ad_id',
        'ad_name',
        'objective',
        'actions',
        'spend',
        'impressions',
        'reach',
        'frequency',
        'cpm',
        'clicks',
        'ctr',
        'cpc',
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cost_per_outbound_click',
        'cost_per_inline_link_click',
        'cost_per_total_action',
        'relevance_score'
    ],
}

TIME = {
    'loop_wait_time':1.0,
    'limit_wait_time':310,
}

RESULT = {
    'age':{
        '13-17':{},
        '18-24':{},
        '25-34':{},
        '35-44':{},
        '45-54':{},
        '55-64':{},
        '65+':{},
    },
    'gender':{
        'male':{},
        'female':{},
    },
    'country':{
        'US':{},
        'KR':{},
        'MX':{},
        'PE':{},
        'RO':{},
        'DZ':{},
        'GD':{},
    },
    'publisher_platform':{
        'facebook':{},
        'instagram':{},
        'messenger':{},
        'audience_network':{},
    },
    'none':{
        'data':{},
    },
}

MAIL = {
    'login_id': 'sb63w1@gmail.com',
    'login_pw': 'xowhghkd1!A',
    'from': 'sb63w1@gmail.com',
    'recipients': [
        'support@wizpace.com',
        'tony.hwang@wizpace.com',
    ]
}
