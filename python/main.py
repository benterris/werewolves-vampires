import argparse
import socket

try:
    from tcpServer import werewolf_player, vampire_player
    from tcpServer.echo_client import *
    import state

except:
    from python.tcpServer import werewolf_player, vampire_player
    from python.tcpServer.echo_client import *
    from python import state

def generic_player(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        send_nme_command(s, 'Equipe4')
        game = None
        command = read_command(s)
        print(command)

        if command == 'SET':
            set = receive_set_command(s)
            print(set)
            game = state.State(set[1], set[0])
        elif command == 'HUM':
            print(receive_hum_command(s))
        elif command == 'HME':
            x,y = receive_hme_command(s)
            print(x,y)
            print(game.findObjectAtLocation(x,y)['type'])

        elif command == 'MAP':
            map = receive_map_command(s)
            print(map)
            game.update(map[-1])

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--ipAddress", required=True, type=str, help="The game server ip")
    ap.add_argument("-p", "--port", required=True, type=str, help="The game server port")
    ap.add_argument("-r", "--role", required=True, type=str, help="Our player role")

    args = vars(ap.parse_args())

    if args['role'] == 'W':
        generic_player(args['ipAddress'], args['port'])
    if args['role'] == 'V':
        vampire_player.vampire_game(args['ipAddress'], args['port'])
    else:
        raise ValueError('Unkown player!')