import json
import jwt
import time
import hashlib
import requests


def is_json(data):
    try:
        json.loads(data)
    except ValueError:
        return False
    return True


# USER
USER = 'admin'

# ACCESS KEY from navigation >> Tests >> API Keys
ACCESS_KEY = 'amlyYTphY2ViNDc0Yi02NTBmLTQ3NTQtODE1My02OWQ3ZTNlYzg2NzUgYWRtaW4gVVNFUl9ERUZBVUxUX05BTUU'

# ACCESS KEY from navigation >> Tests >> API Keys
SECRET_KEY = '9D35qG7tZFMCBwD9ILHAM18PYFt1Yk0oRAae7M2DWUM'

# JWT EXPIRE how long token been to be active? 3600 == 1 hour
JWT_EXPIRE = 3600

# BASE URL for Zephyr for Jira Cloud
BASE_URL = 'https://79d3cb71.ngrok.io'

# RELATIVE PATH for token generation and make request to api
RELATIVE_PATH = '/public/rest/api/1.0/executions'

# CANONICAL PATH (Http Method & Relative Path & Query String)
CANONICAL_PATH = 'GET&'+RELATIVE_PATH+'&projectId=10000&issueId=10000&offset=0&size=10'

# TOKEN HEADER: to generate jwt token
payload_token = {
            'sub': USER,
            'qsh': hashlib.sha256(CANONICAL_PATH.encode('utf-8')).hexdigest(),
            'iss': ACCESS_KEY,
            'exp': int(time.time())+JWT_EXPIRE,
            'iat': int(time.time())
        }

# GENERATE TOKEN
token = JWTGenerator.jwt(payload_token, SECRET_KEY, algorithm='HS256').strip().decode('utf-8')

print(token)

# REQUEST HEADER: to authenticate and authorize api
headers = {
            'Authorization': 'JWT '+token,
            'Content-Type': 'application/json',
            'zapiAccessKey': ACCESS_KEY
        }


# REQUEST PAYLOAD: to create cycle
cycle = {
            'name': 'Sample Cycle',
            'projectId':  10000,
            'versionId': -1
        }

# MAKE REQUEST:
raw_result = requests.get(BASE_URL + RELATIVE_PATH + '?projectId=10000&issueId=10000&offset=0&size=10', headers=headers, json=cycle)
if is_json(raw_result.text):

    # JSON RESPONSE: convert response to JSON
    json_result = json.loads(raw_result.text)

    # PRINT RESPONSE: pretty print with 4 indent
    print(json.dumps(json_result, indent=4, sort_keys=True))

else:
    print(raw_result.text)
