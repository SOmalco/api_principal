from schema import Schema, And
from api_principal.utils import utils

partner_endpoint_schema = Schema(
    {'name': And(str, len),
     'cnpj': And(str, utils.is_cnpj_valid)}
)

quote_endpoint_schema = Schema(
    {'age': And(int, utils.is_age_valid),
     'sex': And(str, utils.is_sex_valid)}
)

policy_endpoint_schema = Schema(
    {'quotation_id': And(str, utils.is_uuid_valid),
     'name': And(str, len),
     'sex': And(str, utils.is_sex_valid),
     'date_of_birth': And(str, utils.is_valid_date_format) }
)