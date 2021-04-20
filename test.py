from jose import jwt
from datetime import datetime

SECRET_KEY = 'ALKSJDFALKDJQOIURLOAKSJFLAKSJDLKFOCI'
payload = {
    'sub': 'hello',
    'exp': datetime.now().timestamp()
}

token = jwt.encode(payload, SECRET_KEY, 'HS256')
payload: dict = jwt.decode(token, SECRET_KEY, 'HS256')
exp = payload['exp']
exp_dt = datetime.fromtimestamp(exp)
print(exp_dt > datetime.now())