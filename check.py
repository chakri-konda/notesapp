import requests

r = requests.post('http://localhost:5000/app/user/auth', json={"username":"root", "password":"root"})

print(r.status_code)
print(r.json())
