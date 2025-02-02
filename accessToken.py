import requests


email = input('email: ')
#password = input('password: ')
code = input('code: ')
payload = {
    'account' : email,
#    'password' : password
    'code': code
}

query_url = "https://api.bambulab.com/v1/user-service/user/login"

response = requests.post(query_url, json=payload)
print(response.json())