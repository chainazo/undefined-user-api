from rest_framework.validators import ValidationError


class PasswordValidator(object):
    """
    Validator for password
    """

    def _is_sufficiently_long(self, value):
        """
        checks whether password is at least 8 characters long
        :return: True if does, False if does not
        """
        return len(value) >= 8

    def _does_contain_uppercase(self, value):
        """
        checks whether password contains at least one uppercase
        :return: True if does, False if does not
        """
        return value.lower() != value

    def _does_contain_number(self, value):
        """
        checks whether password contains at least one number
        :return: True if does, False if does not
        """
        return any(char.isdigit() for char in value)

    def __call__(self, value, *args, **kwargs):
        if self._is_sufficiently_long(value) is False:
            raise ValidationError(
                'Password must be at least 8 characters long')
        if self._does_contain_number(value) is False:
            raise ValidationError('Password must contain number(s)')
        if self._does_contain_uppercase(value) is False:
            raise ValidationError('Password must contain uppercase(s)')


class PhoneNumberValidator(object):
    """
    Validator for phone number
    """

    def __init__(self):
        self._message = 'Invalid phone number'

    def __call__(self, value, *args, **kwargs):
        _split_number = value.split('-')
        if len(_split_number) != 3:
            raise ValidationError(self._message)
        elif _split_number[0] != '010' or len(_split_number[1]) != 4 or len(_split_number[2]) != 4:
            raise ValidationError(self._message)


class GenderValidator(object):
    """
    Validator for gender
    """

    def __init__(self):
        self._message = 'Invalid gender'

    def __call__(self, value, *args, **kwargs):
        if value != 'M' and value != 'W':
            raise ValidationError(self._message)
