#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 44
Números de aluno: 58654, 58626 
"""

# Zona para fazer importação


###############################################################################

class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id

    def subscribe(self, client_id, time_limit):
        pass # Remover esta linha e fazer implementação da função

    def unsubscribe (self, client_id):
        pass # Remover esta linha e fazer implementação da função

    def status(self, client_id):
        pass # Remover esta linha e fazer implementação da função
   
    def __repr__(self):
        output = ""
        # R <resource_id> <list of subscribers>
        return output

###############################################################################

class resource_pool:
    def __init__(self, N, K, M):
        pass # Remover esta linha e fazer implementação da função
        
    def clear_expired_subs(self):
        pass # Remover esta linha e fazer implementação da função

    def subscribe(self, resource_id, client_id, time_limit):
        pass # Remover esta linha e fazer implementação da função

    def unsubscribe (self, resource_id, client_id):
        pass # Remover esta linha e fazer implementação da função

    def status(self, resource_id, client_id):
        pass # Remover esta linha e fazer implementação da função

    def infos(self, option, client_id):
        pass # Remover esta linha e fazer implementação da função

    def statis(self, option, resource_id):
        pass # Remover esta linha e fazer implementação da função

    def __repr__(self):
        output = ""
        # Acrescentar no output uma linha por cada recurso
        return output

###############################################################################

# código do programa principal
import socket_utils
import sys

HOST = sys.argv[1]
PORT = int(sys.argv[2])
M = int(sys.argv[3])
K = int(sys.argv[4])
N = int(sys.argv[5])


def main():
    while True:
        #tuple with socket and address
        s= socket_utils.create_tcp_server_socket(HOST, PORT, 100)
        msg = s[0].recv(1024)  #s[0] is the socket and s[1] is the address
        print(msg.decode())
        resposta = "adeus"
        s[0].sendall(resposta.encode())

        if msg.decode() == "exit":
            break

        s[0].close()

if __name__ == '__main__':
    main()