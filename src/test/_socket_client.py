from tablut.network.socket_slient import SocketClient


def start_game(client):
    while True:
        state = client.receive_state()
        print(state)


if __name__ == "__main__":
    client = SocketClient()
    client.connect()
    start_game(client)
