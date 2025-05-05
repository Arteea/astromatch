import pytest
from bot.validators.registration_validators import RegistrationValidator
from tests.test_data.validation_data import ValidationData as v

class TestValidator:

    @pytest.mark.parametrize(
        "phone, res, expectation",
        v.phone_validation_data
    )
    def test_validate_phone(self, phone, res, expectation):
        with expectation:
            assert RegistrationValidator.validate_phone(phone) == res

    
    @pytest.mark.parametrize(
        "username, res, expectation", 
        v.username_validation_data
    )
    def test_validate_username(self, username, res, expectation):
        with expectation:
            assert RegistrationValidator.validate_username(username) == res

    
    @pytest.mark.parametrize(
        "gender, res, expectation",
        v.gender_validation_data
    )
    def test_validate_gender(self, gender, res, expectation):
        with expectation:
            assert RegistrationValidator.validate_gender(gender) == res

    
    @pytest.mark.parametrize(
        "age, res, expectation",
        v.age_validation_data
    )
    def test_validate_age(self, age, res, expectation):
        with expectation:
            assert RegistrationValidator.validate_age(age) == res