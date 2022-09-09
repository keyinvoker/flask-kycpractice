import requests

BASE = 'http://127.0.0.1:5000/'

# data = [
#     {
#         "name": "Post Man but in the Python file",
#         "email": "postman@gmail.com",
#         "phone": "082231599970",
#         "address": "Postmans house",
#         "salary": 5000000,
#         "ktp": "31730504000",
#         "npwp": "1234567890"
#     },
#     {
#         "name": "Post Man but in the Python file 2",
#         "email": "postman2@gmail.com",
#         "phone": "082231599972",
#         "address": "Postmans house 2",
#         "salary": 5000002,
#         "ktp": "31730504002",
#         "npwp": "1234567892"
#     }
# ]

# for i in range(len(data)):
#     response = requests.post(BASE + 'register', data[i])
#     print(response.json()) #TODO: {'message': "Did not attempt to load JSON data because the request Content-Type was not 'application/json'."}
#     # but can POST in Postman

response = requests.get(BASE + 'mail')
print(response.json())