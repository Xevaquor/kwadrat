import re

from app import db
from app.model.user import User

class ValidationError(object):
    def __init__(self, msg):
        self.message = msg


class PasswordValidator(object):
    def __init__(self, pass_func, confirmation_func):
        self.pass_func = pass_func
        self.confirmation_func = confirmation_func

    def validate(self):
        errors = []
        if self.pass_func() != self.confirmation_func():
            errors += [ValidationError("Hasło i jego potwierdzenie muszą być takie same")]
        if len(self.pass_func()) < 3:
            errors += [ValidationError("Hasło musi mieć co najmniej 3 znaki")]

        return errors, len(errors) == 0


class PhoneValidator(object):
    def __init__(self, phone):
        self.phone_func = phone

    def validate(self):
        errors = []
        pattern = '^[0-9]{9}'
        if not re.match(pattern, self.phone_func()):
            errors += [ValidationError("Numer telefonu ma niepoprawny format")]

        return errors, len(errors) == 0


class EmailValidator(object):
    def __init__(self, phone):
        self.phone_func = phone

    def validate(self):
        errors = []
        pattern = r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'
        if not re.match(pattern, self.phone_func()):
            errors += {ValidationError("Nieporawny adres e-mail")}
        return errors,  len(errors) == 0

class UniqueEmailValidator(object):
    def __init__(self, email):
        self.email_func = email

    def validate(self):
        existing_user = User.query.filter_by(email=self.email_func()).first()
        if existing_user is None:
            return [], True
        else:
            return [ValidationError('Użytkownik o podanym adresie e-mail już istnieje!')], False

class CombinedValidator(object):
    def __init__(self, validators):
        self.validators = validators

    def validate(self):
        errors = []
        for v in self.validators:
            e, _ = v.validate()
            errors += e
        return errors,  len(errors) == 0


