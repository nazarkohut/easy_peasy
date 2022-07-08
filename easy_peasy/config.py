import os

secret_key = os.getenv('SECRET_KEY')

DB = {
    "NAME": os.getenv('NAME'),
    "PASSWORD": os.getenv('PASSWORD')
}

CLOUDINARY = {
    "CLOUD_NAME": os.getenv('CLOUD_NAME'),
    "API_KEY": os.getenv('API_KEY'),
    "API_SECRET": os.getenv('CLOUDINARY API_SECRET_KEY')
}
