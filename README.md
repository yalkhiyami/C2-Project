# C2-Project

This project implements a basic Command and Control (C2) framework with encrypted communication between a server and multiple client agents. The C2 framework is designed for educational and cybersecurity research purposes, demonstrating the fundamentals of secure client-server communication, remote command execution, and encryption.

## Features
- **C2 Server**: The server manages client registrations, issues commands to clients, and receives execution results.
- **C2 Client**: The client registers with the server, fetches commands, executes them locally, and returns the results.
- **Encryption**: Communication between the server and client is encrypted using AES (Advanced Encryption Standard) in CBC mode for secure data transfer.

## Configuration

### Prerequisites
- **Python 3.x**
- **Required Libraries**:
  - `Flask` (for the server)
  - `Requests` (for client-server communication)
  - `PyCryptodome` (for AES encryption)

You can install the required libraries using pip:
```bash
pip install flask requests pycryptodome
```

### Setting Up the Server
1. Run the C2 server using the following command:
   ```bash
   python c2_server.py
   ```
2. The server will start and listen for incoming client requests on `http://127.0.0.1:5000`.

### Setting Up the Client
1. Configure the `SERVER_URL` variable in `c2_client.py` to point to your server's address:
   ```python
   SERVER_URL = "http://127.0.0.1:5000"
   ```
   Replace `127.0.0.1` with your server's IP address if it's hosted on a different machine.
2. Run the client using:
   ```bash
   python c2_client.py
   ```
3. The client will register with the server, fetch commands, execute them, and send back the results.

### Sending Commands to the Client
1. Use tools like `curl`, Postman, or a script to send commands to the server.
2. Example `curl` command to send a command to a specific client:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"client_id": "client1", "command": "ls"}' http://127.0.0.1:5000/add_command
   ```

## Security and Encryption
Communication between the client and server is encrypted using AES with CBC mode for confidentiality. The `SECRET_KEY` and initialization vector (IV) should be configured consistently between the client and server.
