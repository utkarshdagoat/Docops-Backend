import environ
import os
from docops.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


TOKEN_REQUEST_URL=env('TOKEN_REQUEST_URL')
CLIENT_ID=env('CLIENT_ID') 
BACKEND_URL_REDIRECT=env('BACKEND_URL_REDIRECT')
CLIENT_SECRET = env('CLIENT_SECRET')
AUTH_CODE_URL=env('AUTH_CODE_URL')
USER_INFO_URL=env('USER_INFO_URL')

REQUEST_STATE =  [
    ('pending' , 'pending'),
    ('accepted' , 'accepted'),
    ('rejected' , 'rejected')
]