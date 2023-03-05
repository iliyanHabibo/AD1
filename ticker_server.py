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
# dicionario cuja chave é o id do recurso e o valor é a lista de clientes que subscreveram
resource_client_list = {}

# dicionario cuja chave é o par (id do recurso, id do cliente) e o valor é o tempo limite
resource_time_limit = {}


class resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id

    def subscribe(self, client_id, time_limit):
        # se o cliente não subscreveu o recurso, adiciona o cliente à lista de clientes que subscreveram o recurso
        if client_id not in resource_client_list[self.resource_id]:
            resource_client_list[self.resource_id].append(client_id)

        # se o cliente já subscreveu o recurso, atualiza o tempo limite
        # se o cliente não subscreveu o recurso, adiciona o par (id do recurso, id do cliente) ao dicionario
        resource_time_limit[(self.resource_id, client_id)
                            ] = time_limit + time.time()

    def unsubscribe(self, client_id):
        # remove o cliente da lista de clientes que subscreveram o recurso
        resource_client_list[self.resource_id].remove(client_id)

        # remove o par (id do recurso, id do cliente) do dicionario
        for key in resource_time_limit.copy().keys():
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
            str(len(resource_client_list[self.resource_id])) + " "

        # Acrescentar no output a lista de clientes que subscreveram o recurso
        for client in resource_client_list[self.resource_id]:
            output += str(client) + " "

        # R <resource_id> <number of clients subscribed> <list of subscribers>
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

        # criar recursos e adicionar ao dicionario resource_object
        # recursos vao de 0 a M-1
        for i in range(0, M):
            resource_object[i] = resource(i)

        # criar listas de clientes vazias para o numero de recursos M e colocar no dicionario resource_client_list
        for i in range(0, M):
            resource_client_list[i] = []

    def clear_expired_subs(self):
        # usar unsubscribe da classe resource para remover os clientes que expiraram
        time_limit = int(time.time())

        # percorrer o dicionario resource_time_limit e dar unsubscribe nos clientes que expiraram
        if len(resource_time_limit) > 0:
            for resource_id, client_id in resource_time_limit.copy().keys():
                if time_limit > resource_time_limit[(resource_id, client_id)]:
                    resource_object[resource_id].unsubscribe(client_id)

    def subscribe(self, resource_id, client_id, time_limit):
        return resource_object[resource_id].subscribe(client_id, time_limit)

    def unsubscribe(self, resource_id, client_id):
        return resource_object[resource_id].unsubscribe(client_id)

    def status(self, resource_id, client_id):
        return resource_object[resource_id].status(client_id)

    def infos(self, option, client_id):
        # lista de recursos a que o cliente subscreveu
        lista_subscritos = []
        for resource_id in resource_client_list.keys():
            if client_id in resource_client_list[resource_id]:
                lista_subscritos.append(resource_id)
        if option == "M":
            return lista_subscritos
        elif option == "K":
            return self.K - len(lista_subscritos)

    def statis(self, option, resource_id=None):
        if option == "L":
            return len(resource_client_list[resource_id])
        elif option == "ALL":
            return repr(self)

    def __repr__(self):
        output = ""
        for resource_id in resource_object.keys():
            output += repr(resource_object[resource_id]) + "\n"
        return output


###############################################################################

# código do programa principal
HOST = sys.argv[1]
PORT = int(sys.argv[2])
# numero maximo de recursos
M = int(sys.argv[3])
# numero maximo de recursos por cliente
K = int(sys.argv[4])
# numero maximo de subscritores por recurso
N = int(sys.argv[5])

# funcao auxiliar que conta o numero de recursos a que o cliente subscreveu


def count_resources_client(client_id):
    count = 0
    for resource_id in resource_client_list.keys():
        if client_id in resource_client_list[resource_id]:
            count += 1
    return count


def main():
    # criar objeto para resource_pool para usarmos no main
    # ja cria os recursos
    resource_pool_object = resource_pool(N, K, M)

    # tuple with socket and address
    s = socket_utils.create_tcp_server_socket(HOST, PORT, 100)

    # recebe o id do cliente
    client_id = int(socket_utils.receive_all(s[0], 1024))

    # resposta a confirmar id do cliente
    s[0].sendall("mensagem do servidor: O ID do cliente é {}".format(
        str(client_id)).encode())

    while True:

        # mostrar info sobre ligaçao (HOST e PORT)
        print("Ligado a " + str(s[1][0]) + " e no porto " + str(s[1][1]))
        # começa a receber os comandos
        msg = s[0].recv(1024)  # s[0] is the socket and s[1] is the address
        msg = msg.decode()
        args = msg.split()

        # dar clear aos clientes que expiraram
        resource_pool_object.clear_expired_subs()
        if args[0] == "SUBSCR":
            if int(args[1]) not in resource_object.keys():
                resposta = "UNKNOWN-RESOURCE"
            elif count_resources_client(client_id) >= K:
                resposta = "NOK"
            elif len(resource_client_list[int(args[1])]) >= N:
                resposta = "NOK"
            else:
                resource_pool_object.subscribe(
                    int(args[1]), client_id, int(args[2]))
                resposta = "OK"
        elif args[0] == "CANCEL":
            if int(args[1]) not in resource_client_list.keys():
                resposta = "UNKNOWN-RESOURCE"
            elif client_id not in resource_client_list[int(args[1])]:
                resposta = "NOK"
            else:
                resource_pool_object.unsubscribe(int(args[1]), client_id)
                resposta = "OK"
        elif args[0] == "STATUS":
            if int(args[1]) not in resource_client_list.keys():
                resposta = "UNKNOWN-RESOURCE"
            else:
                resposta = resource_pool_object.status(int(args[1]), client_id)
        elif args[0] == "INFOS":
            if args[1] == "M":
                resposta = str(resource_pool_object.infos(
                    str(args[1]), client_id))
            elif args[1] == "K":
                resposta = str(resource_pool_object.infos(args[1], client_id))
        elif args[0] == "STATIS":
            if args[1] == "L":
                resposta = str(resource_pool_object.statis(
                    args[1], int(args[2])))
            elif args[1] == "ALL":
                resposta = resource_pool_object.statis(option=args[1])
        elif args[0] == "EXIT":
            break
        elif msg.decode() == "exit":
            break

        s[0].sendall(resposta.encode())

    print("ligacao terminada")

    s[0].close()


if __name__ == '__main__':
    main()
