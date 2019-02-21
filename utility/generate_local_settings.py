from django.core.management.utils import get_random_secret_key

secret_key = get_random_secret_key()
text = 'SECRET_KEY = \'{0}\'\nDEBUG = True'.format(secret_key)

path = './config/local_settings.py'

with open(path, mode='w') as f:
    f.write(text)
