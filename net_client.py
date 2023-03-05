# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - net_client.py
Grupo: 44
Números de aluno: 58654, 58626 
"""

# zona para fazer importação
import socket
import socket_utils

# definição da classe server_connection 

class server_connection:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.sock = None

    def connect(self):
        """
        Estabelece a ligação ao servidor especificado na inicialização.
        """
        self.sock = socket_utils.create_tcp_client_socket(self.address, self.port)
        return self.sock
    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        #s = self.connect()
        #self.sendall(data.encode())
        #data = socket_utils.receive_all(self,1024)
        #return data.decode()
        self.sock.sendall(data.encode())
        data = socket_utils.receive_all(self.sock, 1024)
        return data
    
    def close(self):
        """
        Termina a ligação ao servidor.
        """
        return self.sock.close()
        



