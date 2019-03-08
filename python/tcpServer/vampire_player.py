from python.tcpServer.echo_client import *
from python.alpha_beta import AlphaBeta
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server

if __name__ == "__main__":

    alphabeta = AlphaBeta()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send_nme_command(s, 'Vampire')
        counter = 0
        game = None
        while True:
            counter += 1
            print('---------', counter, '---------')
            command = read_command(s)
            print(command)
            if command == 'BYE':
                # sleep(2)
                pass
            elif command == 'END':
                break
            elif command == 'SET':
                set = receive_set_command(s)
                print(set)
                game = state.State(set[1], set[0])
            elif command == 'HUM':
                print(receive_hum_command(s))
            elif command == 'HME':
                print(receive_hme_command(s))
            elif command == 'MAP':
                map = receive_map_command(s)
                print(map)
                game.update(map[-1])
            elif command == 'UPD':
                upd = receive_upd_command(s)
                print(upd)
                game.update(upd[-1])

                # send_mov_command(s, game.next_move_example_random('V'))
                send_mov_command(s, alphabeta.get_best_next_action(game, 'V'))
                # TODO add a function that makes the next move (returns lov_list)
                # TODO send mov_list
            else:
                pass
                # raise ValueError('Unknown command')
