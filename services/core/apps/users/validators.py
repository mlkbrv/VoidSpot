import re
from django.core.exceptions import ValidationError

def validate_mobile(value):
    rule = re.compile(r'^\d{10,14}$')
    if not rule.search(value):
        raise ValidationError("Invalid mobile number.")

def validate_name(value):
    rule = re.compile(r'^[a-zA-Z\s\-]{2,30}$')
    if not rule.search(value):
        raise ValidationError("Invalid name format.")

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall(r'[A-Z]', password):
            raise ValidationError("The password must contain at least one uppercase letter.")
        if not re.findall(r'[a-z]', password):
            raise ValidationError("The password must contain at least one lowercase letter.")
        if not re.findall(r'\d', password):
            raise ValidationError("The password must contain at least one digit.")
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError("The password must contain at least one special character.")

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."