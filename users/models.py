from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# setting User email field to be unique
User._meta.get_field('email')._unique = True

# setting custom max_length on User fields
User._meta.get_field("username").max_length = 128
User._meta.get_field("first_name").max_length = 64
User._meta.get_field("last_name").max_length = 64
