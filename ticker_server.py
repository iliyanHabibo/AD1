#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_server.py
Grupo: 44
Números de aluno: 58654, 58626 
"""

# Zona para fazer importação
import socket_utils
import sys
import time

###############################################################################
# dicionario cuja chave é o id do recurso e o valor é o objeto resource
resource_object = {}


class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id

    def subscribe(self, client_id, time_limit):
        if (self.resource_id, client_id) not in resource_time_limit.keys():
            resource_client_list[self.resource_id].append(client_id)

        # se o cliente já subscreveu o recurso, atualiza o tempo limite
        # se o cliente não subscreveu o recurso, adiciona o par (id do recurso, id do cliente) ao dicionario
        resource_time_limit[(self.resource_id, client_id)] = time_limit

    def unsubscribe(self, client_id):
        # remove o cliente da lista de clientes que subscreveram o recurso
        resource_client_list[self.resource_id].remove(client_id)

        # remove o par (id do recurso, id do cliente) do dicionario
        for key in resource_time_limit.keys():
            if key[0] == self.resource_id and key[1] == client_id:
                del resource_time_limit[key]

    def status(self, client_id):
        if client_id in resource_client_list[self.resource_id]:
            return "SUBSCRIBED"
        else:
            return "UNSUBSCRIBED"

    def __repr__(self):
        output = ""
        output += "R " + str(self.resource_id) + " " + \
            len(resource_client_list[self.resource_id]) + " "

        # Acrescentar no output a lista de clientes que subscreveram o recurso
        for client in resource_client_list[self.resource_id]:
            output += str(client) + " "

        # R <resource_id> <list of subscribers>
        return output

###############################################################################


class resource_pool:
    def __init__(self, N, K, M):
        # N - numero max de subscritores por recurso
        self.N = N
        # K - numero max de recursos por cliente
        self.K = K
        # M - numero max de recursos
        self.M = M

    def clear_expired_subs(self):
        # usar unsubscribe da classe resource para remover os clientes que expiraram
        time_limit = int(time.time())
        # percorrer o dicionario resource_time_limit e dar unsubscribe nos clientes que expiraram
        for resource_id, client_id in resource_time_limit.keys():
            if time_limit > resource_time_limit[(resource_id, client_id)]:
                resource.unsubscribe(client_id)

    def subscribe(self, resource_id, client_id, time_limit):
        recurso = resource(resource_id)
        return recurso.subscribe(client_id, time_limit)

    def unsubscribe(self, resource_id, client_id):
        recurso = resource(resource_id)
        return recurso.unsubscribe(client_id)

    def status(self, resource_id, client_id):
        recurso = resource(resource_id)
        return recurso.status(client_id)

    def infos(self, option, client_id):
        if option == "M":
            output = ""
            for resource_id in resource_client_list.keys():
                if client_id in resource_client_list[resource_id]:
                    recurso = resource(resource_id)
                    output += recurso.__repr__() + "    "
            return output
        elif option == "K":
            return self.K - len(resource_client_list[resource_id])

    def statis(self, option, resource_id):
        if option == "L":
            return len(resource_client_list[resource_id])
        elif option == "ALL":
            output = ""
            for resource_id in resource_client_list.keys():
                recurso = resource(resource_id)
                output += recurso.__repr__() + "    "
            return output


# não fiz esta

    def __repr__(self):
        output = ""
        return output


###############################################################################
# dicionario cuja chave é o id do recurso e o valor é a lista de clientes que subscreveram
resource_client_list = {}

# dicionario cuja chave é o par (id do recurso, id do cliente) e o valor é o tempo limite
resource_time_limit = {}


# código do programa principal
HOST = sys.argv[1]
PORT = int(sys.argv[2])
M = int(sys.argv[3])
K = int(sys.argv[4])
N = int(sys.argv[5])


def main():
    while True:
        # tuple with socket and address
        s = socket_utils.create_tcp_server_socket(HOST, PORT, 100)
        msg = s[0].recv(1024)  # s[0] is the socket and s[1] is the address
        print(msg.decode())
        resposta = "adeus"
        s[0].sendall(resposta.encode())

        if msg.decode() == "exit":
            break

        s[0].close()


if __name__ == '__main__':
    main()
