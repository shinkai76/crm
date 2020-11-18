#encoding=utf-8

import requests
import json
from datetime import datetime

url = "https://dingtalk.e.ikcrm.com"
user_name = "18858118708"
password = "Aa.123456"
user_token = "3a1d730777f6bff51c6c11ef449c7d36"


def get_user_token(url, user_name, password):

    params = {"device": "dingtalk", "version_code": "3.13.0", "login": user_name, "password": password}
    r = requests.post("%s/api/v2/auth/login" % url, params = params)
    print r.text

def get_contract_filter(url, user_token):
    params = {"device": "dingtalk", "version_code": "3.13.0", "user_token": user_token}
    r = requests.get("%s/api/v2/contracts/filter_sort_group" % url, params=params)
    print r.text

def get_contract_field(url, user_token, field):
    params = {"device": "dingtalk", "version_code": "3.13.0", "user_token": user_token}
    r = requests.get("%s/api/v2/contracts/%s/filter_options" % (url, field), params=params)
    print r.text

def get_contract(url, user_token):
    params = {"device": "dingtalk", "version_code": "3.13.0", "user_token": user_token, "page": 1, "per_page": 30, "category": 10730677}
    r = requests.get("%s/api/v2/contracts?end_at[]=2018-9-15&end_at[]=2018-10-15" % url, params=params)
    print r.status_code
    print r.text

def get_contract_by_title(url, user_token, title):
    params = {"device": "dingtalk", "version_code": "3.13.0", "user_token": user_token, "query": title}
    r = requests.get("%s/api/v2/contracts/by_name" % url, params=params)
    print r.text

def get_contract_detail(url, user_token, id):
    params = {"device": "dingtalk", "version_code": "3.13.0", "user_token": user_token}
    r = requests.get("%s/api/v2/contracts/%s" % (url, id), params=params)
    print r.text

def create_received_payments(url, user_token, id, receive_stage, amount, receive_date, **kwargs):
    params = {"device": "dingtalk", "version_code": "3.13.0", "user_token": user_token}
    received_payment = {"receive_stage": receive_stage, "amount": amount, "receive_date": receive_date}
    for item in kwargs:
        received_payment[item] = kwargs.get(item)
    data = {"received_payment": received_payment}
    r = requests.post("%s/api/v2/contracts/%s/received_payments" % (url, id), params=params, data=json.dumps(data))
    print r.text

def update_received_payments(url, user_token, contract_id, id, **kwargs):
    params = {"device": "dingtalk", "version_code": "3.13.0", "user_token": user_token}
    received_payment = {}
    for item in kwargs:
        received_payment[item] = kwargs.get(item)
    data = {"received_payment": received_payment}
    r = requests.put("%s/api/v2/contracts/%s/received_payments/%s" % (url, contract_id, id), params=params, data=json.dumps(data))
    print r.text

# get_user_token(url, user_name, password)
get_contract(url, user_token)
# get_contract_detail(url, user_token, 1759835)
# get_contract_filter(url, user_token)
# get_contract_field(url, user_token, "created_at")
# get_contract_by_title(url, user_token, "2018101501")