from App import server, app, broadcast
from AppSocket import client_socket

if __name__ == "__main__":
    server.run(app, debug=True)
    # Listen to the stream, the code is generated using Copilot
    # while True:
    #     data = client_socket.recv(1024)
    #     print(data.decode())
    #     # TODO
    #     # 