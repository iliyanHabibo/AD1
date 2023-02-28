#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 44
Números de aluno: 58654, 58626 
"""
# Zona para fazer imports
import socket_utils
import sys
import net_client

ID = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])

# Programa principal

def main():
    s = net_client.server_connection(HOST, PORT)
    while True:
        command = input("Command: ")
        s.connect()
        #tenho que fazer check para ver se o comando é válido
        s.send_receive(command)

        if command == "exit":
            break
            s.close()




if __name__ == '__main__':
    main()