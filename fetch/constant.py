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
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cpc',
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
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cpc',
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
        'inline_link_clicks',
        'inline_link_click_ctr',
        'outbound_clicks',
        'outbound_clicks_ctr',
        'canvas_avg_view_percent',
        'cpc',
        'cost_per_outbound_click',
        'cost_per_inline_link_click',
        'cost_per_total_action',
        'relevance_score'
    ],
}

TIME = {
    # on local: 0.1, 0.5, 1.0, 2.0(local), 1.5(X), 3.0
    'loop_wait_time':3.0,
}

FETCH = {
    # yesterday
    'from_days':1,
    # minimum impression limit
    'min_imp_limit':10
}

MAIL = {
    'login_id': 'sb63w1@gmail.com',
    'login_pw': 'xowhghkd1!A',
    'from': 'sb63w1@gmail.com',
    'recipients': [
        'support@wizpace.com',
        'tony.hwang@wizpace.com',
        # 'danbee@wizpace.com',
        # 'jusung@wizpace.com'
    ]
}
