import logging

from tablut.network.socket_slient import SocketClient


def start_game(client):
    while True:
        state = client.receive_state()
        print(state)


if __name__ == "__main__":
    client = SocketClient("White", host="localhost", port=5800, level=logging.DEBUG)
    client.connect()
    client.send_name("WhiteTest")
    start_game(client)
