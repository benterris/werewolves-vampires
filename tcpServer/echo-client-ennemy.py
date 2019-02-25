#!/usr/bin/env python3

import socket
import struct
from time import sleep

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 5555  # The port used by the server


def read_int(sock):
    """
    receives 1 byte and converts it to int
    :param sock: the connection socket
    :return: int value of the received byte
    """
    data = sock.recv(1)
    return int.from_bytes(data, byteorder='big')


def read_command(sock):
    """
    receives 3 bytes and decodes them to read the command name
    :param sock: the connection socket
    :return: command name
    """
    return sock.recv(3).decode()


def receive_set_command(sock):
    """
    receive the SET command at the start of the game
    :param sock: the connection socket
    :return: n: number of lines & m: number of columns
    """
    n = read_int(sock)
    m = read_int(sock)
    return n, m


def receive_hum_command(sock):
    n = read_int(sock)
    homes = [(read_int(sock), read_int(sock)) for i in range(n)]
    return n, homes


def receive_hme_command(sock):
    """
    receive the HME command at the start of the game
    :param sock: the connection socket
    :return: x, y: start position coordinates
    """
    x = read_int(sock)
    y = read_int(sock)
    return x, y


def receive_upd_command(sock):
    n = read_int(sock)
    changes = [[(read_int(sock), read_int(sock)), read_int(sock), read_int(sock), read_int(sock)] for i in range(n)]
    return n, changes


def receive_map_command(sock):
    return receive_upd_command(sock)


def send_nme_command(sock, name):
    """
    sends NME command to define the name of the player and start the game
    :param sock: the connection socket
    :param name: the player name
    :return: None
    """
    trame = bytes()
    trame += 'NME'.encode()
    trame += struct.pack("b", len(name))
    trame += name.encode(encoding='ascii')
    sock.send(trame)


def send_mov_command(sock, mov_list):
    """
    Sends MOV command to move player's individuals
    :param sock: the connection socket
    :param mov_list: list of movements: each element is a list in this format [(x_start, y_start), nb_of_indiv_to_move,(x_end, y_end)]
    :return: None
    """
    trame = bytes()
    trame += 'MOV'.encode()
    trame += struct.pack("b", len(mov_list))
    for movement in mov_list:
        trame += struct.pack("b", movement[0][0])  # x : start position
        trame += struct.pack("b", movement[0][1])  # y : start position
        trame += struct.pack("b", movement[1])  # nb of individuals to move
        trame += struct.pack("b", movement[2][0])  # x : end position
        trame += struct.pack("b", movement[2][0])  # y : end position
    sock.send(trame)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send_nme_command(s, 'Warewolf')

        while True:
            command = read_command(s)
            print(command)
            if command == 'SET':
                print(receive_set_command(s))
            elif command == 'HUM':
                print(receive_hum_command(s))
            elif command == 'HME':
                print(receive_hme_command(s))
            elif command == 'MAP':
                print(receive_map_command(s))
            elif command == 'UPD':
                print(receive_upd_command(s))
            elif command == 'BYE':
                # sleep(2)
                pass
            elif command == 'END':
                break
            else:
                raise ValueError('Unknown command')
# Received b'SET\x05\nHUM\x04\x02\x02\t\x00\t\x02\t\x04HME\x04\x03'
