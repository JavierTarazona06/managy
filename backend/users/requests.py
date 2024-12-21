import base64
import requests
from decouple import config

api = config('API')
username = config('APIUSERNAME')
mypassword = config('API_PWD')

tokenapi = api+"/api/token/"
api_batch = api+"/users/admin/createuser/"


def send_post_token(data):
    response = requests.post(tokenapi, json=data)

    if (response.status_code == 200) or (response.status_code == 201):
        print("Post created successfully:", response.json())
        response_data = response.json()
        token = response_data.get('access')
        return token
    else:
        raise ValueError("Failed to create POST:", response.status_code, response.text)


def send_post_request_createBatch(data):
    '''auth_token = send_post_token({
        "username": username,
        "password": config('DB_PWD')
    })'''

    credentials = f"{username}:{mypassword}"
    auth_token = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {auth_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_batch, json=data, headers=headers)

    if response.status_code == 201:
        print("Post created successfully:", response.json())
        response_data = response.json()
        post_id = response_data.get('id')
        return post_id
    else:
        raise ValueError("Failed to create POST:", response.status_code, response.text)


# Example usage
'''api_url = "http://127.0.0.1:8000/users/admin/createuser/"  # Your Django API endpoint
data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "username": "johndoe",
    "password": "yourpassword"
}

send_post_request(api_url, data)

try:
    response = requests.post(api_url, json=data)

    if response.status_code == 201:
        print("Post created successfully:", response.json())
    else:
        print("Failed to create POST:", response.status_code, response.text)

except requests.exceptions.RequestException as e:
    print("Error during request:", e)
'''