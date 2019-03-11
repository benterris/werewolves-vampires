import argparse
import socket
import sys
from alpha_beta import AlphaBeta
try:
    from tcpServer.echo_client import *
    import state

except:
    from python.tcpServer.echo_client import *
    from python import state

def generic_player(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        send_nme_command(s, 'MECHANTSLOUPS')
        alphabeta = AlphaBeta()
        game = None
        role = None
        while True:
            command = read_command(s)
            print(command)
            if command == 'BYE':
            # sleep(2)
                pass
            elif command == 'END':
                break
            if command == 'SET':
                set = receive_set_command(s)
                print(set)
                game = state.State(set[1], set[0])
            elif command == 'HUM':
                print(receive_hum_command(s))
            elif command == 'HME':
                x,y = receive_hme_command(s)
                print(x,y)
            elif command == 'MAP':
                map = receive_map_command(s)
                print(map)
                game.update(map[-1])
                role = game.findObjectAtLocation(x,y)['type']
            elif command == 'UPD':
                upd = receive_upd_command(s)
                print(upd)
                game.update(upd[-1])

                # send_mov_command(s, game.next_move_example_random('V'))
                send_mov_command(s, alphabeta.get_best_next_action(game, role))
                # TODO add a function that makes the next move (returns lov_list)
                # TODO send mov_list
            else:
                pass
                # raise ValueError('Unknown command')
                
if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2])

    generic_player(ip, port)
    
