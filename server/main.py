import socket
import threading
from server.database import Database
from server.user import User, tel_sockets_dict


def session(conn, addr, database):
    print(f"New connection from {addr}")
    user = User(conn, addr, database)
    user.receive_messages()
    print(f"Disconnected from {addr}")
    tel_sockets_dict.pop(user.tel, None)
    conn.close()

def main():
    database = Database()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', 9090))
            s.listen()
            print("Server is listening on port 9090")
            while True:
                conn, addr = s.accept()
                client_thread = threading.Thread(target=session, args=(conn, addr, database))
                client_thread.start()
        except Exception as e:
            print(f"Error: failed to start server!\n{e}")

if __name__ == '__main__':
    main()