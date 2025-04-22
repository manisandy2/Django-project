# import re
# from django.core.exceptions import ValidationError
# from django.core.validators import EmailValidator
# from urllib.parse import urlparse

# def validate_email(value):
#     validator = EmailValidator()
#     try:
#         validator(value)
#     except ValidationError:
#         raise ValidationError(f"{value} is not a valid email.")

# def validate_website(value):
#     try:
#         result = urlparse(value)
#         if not result.scheme or not result.netloc:
#             raise ValidationError(f"{value} is not a valid website URL.")
#     except Exception:
#         raise ValidationError(f"{value} is not a valid website URL.")