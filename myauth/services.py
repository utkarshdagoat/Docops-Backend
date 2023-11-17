import environ
import os
import requests
import traceback
from docops.settings import BASE_DIR

from .models import User
from constants.constants import CLIENT_ID , CLIENT_SECRET , BACKEND_URL_REDIRECT, TOKEN_REQUEST_URL

def headerFromCode(code:str)->dict:    
    '''
        Call the TOKEN request url for accesstoken from the code provided by channel i outh client
    '''
    request_data = {
            "client_id":CLIENT_ID,
            "client_secret":CLIENT_SECRET,
            "grant_type":"authorization_code",
            "redirect_uri" : f"{BACKEND_URL_REDIRECT}",
            "code":code
    } 
    res = requests.post(TOKEN_REQUEST_URL, data=request_data)
    res = res.json()
    try: 
        ACCESS_TOKEN=res["access_token"]
        REFRSH_TOKEN=res["refresh_token"]
        TOKEN_TYPE=res["token_type"]
        return {"Authorization" : f"{TOKEN_TYPE} {ACCESS_TOKEN}"}
    except:
        return {'res':res , "error":"some"}



def UserFromRequest(user:dict) -> list :
    '''
        Takes the user from oauth2 provided by channeli converts it into a list providing user and is the user member and is empty when dict passed is invalid
    '''
    try:
        username : str = user["person"]["fullName"]
        display_picture = user["person"]["displayPicture"]
        roles:list = user["person"]["roles"]
        year : int = user["student"]["currentYear"]
        email : str = user["contactInformation"]["emailAddress"]
        isMember : bool = False
        for role in roles:
            try:
                if role['role'] == "Maintainer" :
                    isMember=True
            except:
                pass
        user , _ =User.objects.get_or_create( username=username, email=email , display_picture=display_picture, year=year)  

        return [user , isMember ] 
    except:
        traceback.print_exc()
        return []
