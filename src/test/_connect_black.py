import logging

from tablut.network.socket_slient import SocketClient


def start_game(client):
    while True:
        state = client.receive_state()
        print(state)


if __name__ == "__main__":
    client = SocketClient("Black", host="localhost", port=5801, level=logging.DEBUG)
    client.connect()
    client.send_name("BlackTest")
    start_game(client)
