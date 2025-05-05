import pytest
from contextlib import nullcontext as does_not_raise


class ValidationData:

    phone_validation_data = [
            (1111111,-5, pytest.raises(TypeError)),
            ((1,2),4, pytest.raises(TypeError)),
            ("+73333333333","+73333333333", does_not_raise()),
            ("73333333333","+73333333333", does_not_raise()),
            ("88899933333","88899933333", pytest.raises(ValueError)),
            ("788999333333","+788999333333", pytest.raises(ValueError)),
            ]

    username_validation_data = [
            (111111,111111,pytest.raises(TypeError)),
            ((1,2),4, pytest.raises(TypeError)),
            ("12", "12", pytest.raises(ValueError)),
            ('[}]', "[}]", pytest.raises(ValueError)),
            ('1111rke09gj0349gj0193j0g93j49gj314gj34g013jg90134g913j049gj13094jg0139j4g013j4g9013j',
            '1111rke09gj0349gj0193j0g93j49gj314gj34g013jg90134g913j049gj13094jg0139j4g013j4g9013j',
            pytest.raises(ValueError))
    ]

    gender_validation_data = [
        ("male", "male", does_not_raise()),
        ("female", "female", does_not_raise()),
        (("male",), ("male",), pytest.raises(TypeError)),
        ("egege", "egege", pytest.raises(ValueError)),
        (111,111,pytest.raises(TypeError))
    ]

    age_validation_data = [
        ('11', 11, pytest.raises(ValueError)),
        ('18', 18, does_not_raise()),
        ('11', 11, pytest.raises(ValueError)),
        (101, 101, pytest.raises(ValueError)),
        (-1, -1, pytest.raises(ValueError)),
        ('fnewonfei', 'fnewonfei', pytest.raises(ValueError)),
        (11, '11', pytest.raises(ValueError)),
    ]

    