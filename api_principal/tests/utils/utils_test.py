from api_principal.utils import utils
import pytest

@pytest.mark.parametrize("a,expected", [("29284858695043", True), #valid cnpj
                                        ("12.345.678/0001-95", True),
                                        ("123456b800019A",True),
                                        ("2928485869504", False), # invalid cnpj
                                        ("", False), # empty cnpj
                                        ("              ", False)]) # empty spaces string

def test_is_cnpj_valid_parametrized(a,expected):
    assert utils.is_cnpj_valid(a) == expected

@pytest.mark.parametrize("a,expected", [("265bda01-3ac0-4667-be0f-7013a42ac79c", True), #valid uuid
                                        ("2928485869504", False), # invalid uuid
                                        ("", False), # empty uuid
                                        ("        -    -    -    -            ", False)]) #smpty spaces string

def test_is_uuid_valid_parametrized(a,expected):
    assert utils.is_uuid_valid(a) == expected

@pytest.mark.parametrize("a,expected", [("2026-05-21", True), #valid date format
                                        ("2026-21-05", False), # inexistent date
                                        ("2026/05/21", False), # wrong date format
                                        ("21-05-2026", False), # invalid date format
                                        ("05-21-2026", False), # invalid date format
                                        ("", False)]) #empty date

def test_is_uuid_valid_parametrized(a,expected):
    assert utils.is_valid_date_format(a) == expected
