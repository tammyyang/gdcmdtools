from botapi.stella_common import GoogleCredentials

class GFHANDLER:
    def __init__(self, user=None, cred = None)
        self.user = user # [username, password]
        self.cred = cred # [access_token, client_id, client_secret, refresh_token]
        self.login_gc()

    def login_gc(self):
        if self.user is not None: #user based login
            self.gc = gspread.login(self.user[0], self.user[1]) 
        else: #use token
            token_expiry = datetime.datetime.utcnow()
            token_uri = "https://www.google.com/accounts/o8/oauth2/token"
            user_agent = "stella-botapi/1.0"
            self.credentials = GoogleCredentials(self.cred[0], self.cred[1],
                                self.cred[2],-self.cred[3], token_expiry, token_uri, user_agent)
            self.gc = gspread.authorize(self.credentials)

class GoogleCredentials (OAuth2Credentials):
    def __init__ (self, *args, **kwargs):
        super(GoogleCredentials, self).__init__(*args, **kwargs)
        self.refresh()

    def is_expired(self):
        if (datetime.utcnow() - self.token_created_time).seconds > 3500:
            return True
        else:
            return False

    def get_access_token(self):
        if self.is_expired():
            self.refresh()
        return self.access_token

    def refresh(self, *args):
        self.token_created_time = datetime.utcnow()
        self.access_token = self._refresh_access_token(self.client_id, 
                            self.client_secret, self.refresh_token)

    def _refresh_access_token(self, client_id, client_secret, refresh_token):
        payload = {'client_id': client_id, 'client_secret': client_secret,
                   'refresh_token': refresh_token, 'grant_type': 'refresh_token'}
        url = 'https://accounts.google.com/o/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'Host':'accounts.google.com'}
        r = requests.post(url, data=payload, headers=headers)
        return json.loads(r.text)['access_token']


