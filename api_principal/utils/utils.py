import pandas as pd
import uuid
from datetime import datetime
from api_principal.constants import constants
import re

def is_cnpj_valid(cnpj: str)->bool:
    cleared_cnpj = cnpj.strip()
    cnpj_pattern = re.compile(r'^([A-Za-z0-9]{2}\.[A-Za-z0-9]{3}\.[A-Za-z0-9]{3}/[A-Za-z0-9]{4}-[A-Za-z0-9]{2}|[A-Za-z0-9]{14})$')

    return bool(cnpj_pattern.match(cleared_cnpj))

def is_age_valid(age: int)->bool:
    return 0 <= age <= 99

def is_sex_valid(sex:str)->bool:
    return sex in constants.sex_options

def is_uuid_valid(value: str)->bool:
    try:
        uuid.UUID(str(value))
        return True
    except ValueError:
        return False

def is_valid_date_format(date_str: str)-> bool:
    try:
        datetime.strptime(date_str, constants.default_date_format)
        return True
    except ValueError:
        return False

def validate_create_partner_body(body: dict,
                                 model_validated: bool)->dict:
    errors = []
    if not model_validated:
        if "name" not in body and "cnpj" not in body:
            return {"error": "Missing 'name' and 'cnpj'"}
        if "cnpj" not in body:
            errors.append("Missing 'cnpj'")
        if "name" not in body:
            errors.append("Missing 'name'")
        error_message = ", ".join(errors)
        return {"error": error_message}
    return {'success': 'Valid create partner body'}

def validate_individual_quote_body(individual_data: dict,
                                   model_validated: bool)->dict:
    errors = []
    if not model_validated:
        if "age" not in individual_data and "sex" not in individual_data:
            return {"error": "Missing 'age' and 'sex'"}
        if "age" not in individual_data:
            errors.append("Missing 'age'")
        if "sex" not in individual_data:
            errors.append("Missing 'sex'")
        error_message = ", ".join(errors)
        return {"error": error_message}
    return {'success': 'Valid individual quote body'}

def validate_create_policy_body(body: dict,
                                model_validated: bool)->dict:
    errors = []
    if not model_validated:
        if "quotation_id" not in body:
            errors.append("Missing 'quotation_id'")
        if "name" not in body:
            errors.append("Missing 'name'")
        if 'sex' not in body:
            errors.append("Missing 'sex'")
        if 'date_of_birth' not in body:
            errors.append("Missing 'date_of_birth'")
        error_message = ", ".join(errors)
        return {"error": error_message}
    return {'success': 'Valid create policy body'}

def get_partners():
    partners = pd.read_csv('api_principal/data/partners.csv', header=0)
    return partners

def search_partner(partner_cnpj: str,
                   partner_df: pd.DataFrame)->bool:
    return partner_cnpj in partner_df['cnpj'].values.tolist()

def set_partners(partners: pd.DataFrame):
    partners.to_csv('api_principal/data/partners.csv', index=False)

def get_cached_expiration_date(expiration_dates: dict,
                               individual_data: dict):
    try:
        if datetime.strptime(expiration_dates[str(individual_data['age'])][individual_data['sex'].lower()]['expire_at'],
                             constants.default_date_format) >=  datetime.now():

            return expiration_dates[str(individual_data['age'])][individual_data['sex'].lower()]
    except KeyError:
        return 0

def update_expiration_dates(expiration_dates: dict,
                            individual_data: dict,
                            new_quotation: dict):
    age_str = str(individual_data['age'])
    if age_str in expiration_dates.keys():
        expiration_dates[str(individual_data['age'])][individual_data['sex'].lower()] =  new_quotation
        return expiration_dates
    else:
        expiration_dates[str(individual_data['age'])] = {}
        expiration_dates[str(individual_data['age'])][individual_data['sex'].lower()] = new_quotation
        return expiration_dates