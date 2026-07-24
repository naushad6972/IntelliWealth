import requests
base='http://127.0.0.1:8000/api/v1'
creds={'email':'demo@intelliwealth.com','password':'Password123!'}
print('Logging in...')
r=requests.post(f'{base}/auth/login',json=creds)
print('login', r.status_code)
if r.status_code!=200:
    print(r.text)
    raise SystemExit(1)
token=r.json().get('access_token')
headers={'Authorization':f'Bearer {token}'}
paths=['/transactions','/notifications','/chat/history','/reports/download/csv']
for p in paths:
    try:
        rr=requests.get(base+p, headers=headers, timeout=10)
        print(p, rr.status_code, 'len=', len(rr.content))
    except Exception as e:
        print(p, 'error', e)
