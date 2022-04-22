import requests

response = requests.get(
    'http://127.0.0.1:5000/api/user/5',
    params={'apikey': '36b45570-68cf-4112-8803-635c1df00c95'})

print(response.json(), response.status_code)
