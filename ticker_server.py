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

        #criar recursos e adicionar ao dicionario resource_object
        for i in range(1, M+1):
            resource_object[i] = resource(i)    
    def clear_expired_subs(self):
        # usar unsubscribe da classe resource para remover os clientes que expiraram
        time_limit = int(time.time())
        # percorrer o dicionario resource_time_limit e dar unsubscribe nos clientes que expiraram
        for resource_id, client_id in resource_time_limit.keys():
            if time_limit > resource_time_limit[(resource_id, client_id)]:
                resource.unsubscribe(client_id)

    def subscribe(self, resource_id, client_id, time_limit):
        return resource_object[resource_id].subscribe(client_id, time_limit)

    def unsubscribe(self, resource_id, client_id):
        return resource_object[resource_id].unsubscribe(client_id)

    def status(self, resource_id, client_id):
        return resource_object[resource_id].status(client_id)

    def infos(self, option, client_id):
        """
        if option == "M":
            output = ""
            for resource_id in resource_object.keys():
                if client_id in resource_client_list[resource_id]:
                    output += resource_object[resource_id-1].__repr__() + "    "
            return output"""
        #lista de recursos a que o cliente subscreveu
        lista_subscritos = []
        for resource_id in resource_client_list.keys():
            if client_id in resource_client_list[resource_id]:
                lista_subscritos.append(resource_id)
        if option == "M":
            return lista_subscritos
        elif option == "K":
            return self.K - len(lista_subscritos)

    def statis(self, option, resource_id):
        if option == "L":
            return len(resource_client_list[resource_id])
        elif option == "ALL":
            return repr(self)
            """
            output = ""
            for resource_id in resource_client_list.keys():
                recurso = resource(resource_id)
                output += recurso.__repr__() + "    "
            return output"""

    def __repr__(self):
        output = ""
        for resource_id in resource_object.keys():
            output +="R" + repr(resource_object[resource_id]) + "\n"
        return output
        


###############################################################################


# código do programa principal
HOST = sys.argv[1]
PORT = int(sys.argv[2])
#numero maximo de recursos
M = int(sys.argv[3])
#numero maximo de recursos por cliente
K = int(sys.argv[4])
#numero maximo de subscritores por recurso
N = int(sys.argv[5])

#criar objeto para resource_pool para usarmos no main
resource_pool_object = resource_pool(N, K, M)

#funcao auxiliar que conta o numero de recursos a que o cliente subscreveu
def count_resources_client(client_id):
    count = 0
    for resource_id in resource_client_list.keys():
        if client_id in resource_client_list[resource_id]:
            count += 1
    return count

def main():
    # tuple with socket and address
    s = socket_utils.create_tcp_server_socket(HOST, PORT, 100)
    msg = s[0].recv(1024)  # s[0] is the socket and s[1] is the address
    msg = msg.decode()
    msg = msg.split()

    client_id = msg[1]

    while True:
        # tuple with socket and address
        #s = socket_utils.create_tcp_server_socket(HOST, PORT, 100)
        msg = s[0].recv(1024)  # s[0] is the socket and s[1] is the address
        msg = msg.decode()
        args = msg.split()

        if args[0] == "SUBSCR":
            if args[1] not in resource_client_list.keys():
                resposta = "UNKNOWN RESOURCE"
            elif count_resources_client(client_id) >= K:
                resposta = "NOK"
            elif len(resource_client_list[args[1]]) >= N:
                resposta = "NOK"
            else:
                resource_pool_object.subscribe(args[1], client_id, args[2])
                resposta = "OK"
        elif args[0] == "CANCEL":
            if args[1] not in resource_client_list.keys():
                resposta = "UNKNOWN RESOURCE"
            elif client_id not in resource_client_list[args[1]]:
                resposta = "NOK"
            else:
                resource_pool_object.unsubscribe(args[1], client_id)
                resposta = "OK"
        elif args[0] == "STATUS":
            if args[1] not in resource_client_list.keys():
                resposta = "UNKNOWN RESOURCE"
            else:
                resposta = resource_pool_object.status(args[1], client_id)
        elif args[0] == "INFOS":
            if args[1] == "M":
                resposta = " ".join(resource_pool_object.infos(args[1], client_id))
            elif args[1] == "K":
                resposta = str(resource_pool_object.infos(args[1], client_id))
        elif args[0] == "STATIS":
            if args[1] == "L":
                resposta = str(resource_pool_object.statis(args[1], args[2]))
            elif args[1] == "ALL":
                resposta = resource_pool_object.statis(args[1], args[2])
        elif args[0] == "EXIT":
            break
        elif msg.decode() == "exit":
            break


        s[0].sendall(resposta.encode())

        

        #a cada segundo dar clear aos clientes que expiraram
        resource_pool.clear_expired_subs()

    s[0].close()


if __name__ == '__main__':
    main()
