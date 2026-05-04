import json

from flask import jsonify
from requests import Response
from api_principal.model import model_in
from api_principal.utils import utils
from api_principal.diplomat import http_out
import pandas as pd


def create_partner(partner_data: dict)-> tuple[Response, int]:
    if not isinstance(partner_data, dict):
        return jsonify({"error": "Invalid JSON format"}), 400

    is_partner_data_valid = model_in.partner_endpoint_schema.validate(partner_data)
    response = utils.validate_create_partner_body(partner_data,
                                                  is_partner_data_valid)

    if "error" in response:
        return jsonify({"error": response["error"]}), 400
    else:
        existent_partners = utils.get_partners()
        already_partner = utils.search_partner(partner_data['cnpj'],
                                               existent_partners)
        if already_partner:
            return jsonify({"error": "Partner already exists"}), 422
        else:
            listed_partner_values = {'name': [partner_data['name']],
                                     'cnpj': [partner_data['cnpj']]}
            partner_df = pd.DataFrame.from_dict(listed_partner_values)
            updated_partner_df = pd.concat([partner_df,
                                              existent_partners],
                                             axis=0)
            utils.set_partners(updated_partner_df)
            return jsonify({"success": "Added partner"}), 201

def calculate_quote(individual_data: dict)-> tuple[Response, int]:
    if not isinstance(individual_data, dict):
        return jsonify({"error": "Invalid JSON format"}), 400

    is_individual_data_valid = model_in.quote_endpoint_schema.validate(individual_data)

    response = utils.validate_individual_quote_body(individual_data,
                                                    is_individual_data_valid)
    if "error" in response:
        return jsonify({"error": response["error"]}), 400
    else:
        with open('api_principal/data/expiration_dates.json', 'r') as file:
            quotations = json.load(file)

        cached_quotation = utils.get_cached_expiration_date(quotations,
                                                            individual_data)
        if cached_quotation:
            return cached_quotation, 200
        else:
            auth_token = http_out.auth_insurance_company_api()
            response_to_quote_creation = http_out.post_create_quotations_api(individual_data,
                                                                             auth_token)
            if 'error' in response_to_quote_creation.keys():
                return jsonify({"error": response_to_quote_creation["error"]}), 400
            quotation_to_cache = utils.update_expiration_dates(quotations, individual_data, response_to_quote_creation)
            with open("api_principal/data/expiration_dates.json", "w", encoding="utf-8") as file:
                json.dump(quotation_to_cache, file, ensure_ascii=False, indent=4)

            return jsonify(response_to_quote_creation), 200

def create_policy(policy_data: dict)-> tuple[Response, int]:
    if not isinstance(policy_data, dict):
        return jsonify({"error": "Invalid JSON format"}), 400

    is_policy_data_valid = model_in.policy_endpoint_schema.validate(policy_data)
    response = utils.validate_create_policy_body(policy_data,
                                                 is_policy_data_valid)

    if "error" in response:
        return jsonify({"error": response["error"]}), 400
    else:
        auth_token = http_out.auth_insurance_company_api()
        response_to_policy_creation = http_out.post_create_policy(policy_data, auth_token)
        if response_to_policy_creation['code']==200:
            return jsonify(response_to_policy_creation['body']), 200
        else:
            return jsonify({"error": response_to_policy_creation['body']['message']}), 400

def get_policy(policy_id: str)-> tuple[Response, int]:
    if not utils.is_uuid_valid(policy_id):
        return jsonify({"error": "Invalid policy_id"}), 400
    else:
        auth_token = http_out.auth_insurance_company_api()
        response_to_get_policy = http_out.get_policy(policy_id, auth_token)
        if response_to_get_policy['code'] == 200:
            return jsonify(response_to_get_policy['body']), 200
        else:
            return jsonify({"error": response_to_get_policy['body']['message']}), 400
