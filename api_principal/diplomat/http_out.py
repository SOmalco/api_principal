import json

import requests
from api_principal.constants import constants
from resources import api_principal

insurance_url = api_principal.routes['insurance_company_api']
jwt_auth = ''

def auth_insurance_company_api():
    insurance_company_auth_url = f'{insurance_url}/api/auth'
    headers = {'X-API-Key': f'{constants.api_key}'}
    response = requests.post(insurance_company_auth_url,
                             headers=headers)
    global jwt_auth
    jwt_auth = response.json()['access_token']
    return jwt_auth

def post_create_quotations_api(individual_data: dict,
                               auth_token: str)->dict:
    create_quote_url = f'{insurance_url}/api/quotations'
    headers = {'Authorization': f'Bearer {auth_token}',
               "Content-Type": "application/json"}
    body = json.dumps(individual_data)
    response = requests.post(create_quote_url,
                             data=body,
                             headers=headers)
    return response.json()

def post_create_policy(request_body,
                       auth_token: str):
    create_policy_url = f'{insurance_url}/api/policies'
    headers = {'Authorization': f'Bearer {auth_token}',
               "Content-Type": "application/json"}
    body = json.dumps(request_body)
    response = requests.post(create_policy_url,
                             data=body,
                             headers=headers)
    return {'code': response.status_code,
            'body': response.json()}

def get_policy(policy_id: str,
               auth_token: str):
    get_policy_url = f'{insurance_url}/api/policies/{policy_id}'
    headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get(get_policy_url,
                            headers=headers)
    return {'code': response.status_code,
            'body': response.json()}
