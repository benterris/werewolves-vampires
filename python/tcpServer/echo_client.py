#!/usr/bin/env python3

import socket
import struct
from python import state
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
    """
    receive the HUM command at the start of the game
    :param sock: the connection socket
    :return: n: number of homes, homes: list of (x,y) coordinates of homes
    """
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
    """
    receive the UPD command
    :param sock: the connection socket
    :return: n: number of changes in the map, changes: list of lists [(x,y),humans,vampires,werewolves]
    """
    n = read_int(sock)
    changes = [[(read_int(sock), read_int(sock)), read_int(sock), read_int(sock), read_int(sock)] for i in range(n)]
    return n, changes


def receive_map_command(sock):
    """
    receive MAP command at the start of the game
    :param sock:
    :return:
    """
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


def send_mov_command(sock, action):
    """
    Sends MOV command to move player's individuals
    :param sock: the connection socket
    :param deplacements: list of 4-uplets (type, number, (x_start, y_start), (x_end, y_end))
    :return: None
    """
    deplacements = action.get_deplacements()
    mov_list = [[deplacement[2], deplacement[1], deplacement[3]] for deplacement in
                deplacements]  # mov_list: list of movements: each element is a list in this format [(x_start, y_start), nb_of_indiv_to_move,(x_end, y_end)]
    trame = bytes()
    trame += 'MOV'.encode()
    trame += struct.pack("b", len(mov_list))
    for movement in mov_list:
        trame += struct.pack("b", movement[0][0])  # x : start position
        trame += struct.pack("b", movement[0][1])  # y : start position
        trame += struct.pack("b", movement[1])  # nb of individuals to move
        trame += struct.pack("b", movement[2][0])  # x : end position
        trame += struct.pack("b", movement[2][1])  # y : end position
    sock.send(trame)
    sleep(2)