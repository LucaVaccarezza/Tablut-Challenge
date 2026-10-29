from tablut.common.enums.player import ROLE
from tablut.network.socket_client import SocketClient


def start_game(client):
    while True:
        state = client.receive_state()
        print(state)


if __name__ == "__main__":
    client = SocketClient(ROLE.WHITE, name="White")
    client.connect()
    client.send_name("WhiteTest")
    start_game(client)
