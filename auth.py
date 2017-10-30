# -*- coding: utf-8 -*-
# Классы для прохождения авторизации и обновления access_token при работе с API MyTarget
# В рамках задачи https://support.rt.ru/browse/ANALYTICS-76

import requests
from datetime import datetime
import http

class Auth():
    """
    Прохождение авторизации при работе с API MyTarget:
    1. 

    2. 
    """

    def __init__( self, client_id, client_secret, agency_client_name, refresh_token = '' ):
        """
        Задание client_id и client_secret для генерации refresh_token при первом запуске
        """

        self.client_id = client_id
        self.client_secret = client_secret
        self.agency_client_name = agency_client_name
        self.refresh_token = refresh_token

    def generateRefreshToken( self ):
        """
        Прохождение процедуры авторизации при первом запуске. Получаем refresh token.
        Результат пишется в файл auth_info.txt

        При последнем тесте была блокировка со стороны MyTarget:
        {u'error_description': u'Active access token limit reached. Please contact support_target@corp.my.com and provide your client id in the message.', u'error': u'token_limit_exceeded'}
        """

        authData = http.HTTP( 'post', '/oauth2/token.json', client_id = self.client_id, client_secret = self.client_secret, grant_type = 'agency_client_credentials', agency_client_name = 'ce2b63ed9f@agency_client' ).makeRequest()

        """
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'agency_client_credentials',
            'agency_client_name': 'ce2b63ed9f@agency_client'
        }
        
        r = requests.post( self.api_url + '/oauth2/token.json', data = params )

        with open('auth_info.txt', 'w') as f:
            f.write( '{}\n{}\n{}\n{}'.format(datetime.now(), r.status_code, r.headers, r.text) )
        """
        
        print authData

        return authData

    def updateAccessToken( self ):
        """
        Обновление access_token после истечения его срока действия.
        """

        return http.HTTP( 'post', '/oauth2/token.json', client_id = self.client_id, client_secret = self.client_secret, grant_type = 'refresh_token', refresh_token = self.refresh_token ).makeRequest()