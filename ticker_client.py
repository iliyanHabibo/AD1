#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações Distribuídas - Projeto 1 - ticker_client.py
Grupo: 44
Números de aluno: 58654, 58626 
"""
# Zona para fazer imports
import sys
import net_client
import time


ID = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])

# Programa principal


def main():
    s = net_client.server_connection(HOST, PORT)
    s.connect()
    # mandamos o ID do cliente ao servidor
    # client_id_received =
    s.send_receive(ID)

    while True:

        # pedimos o comando ao utilizador
        command = input("comando > ")
        args = command.split()
        print("ligado a localhost ")

        # verifica se o comando é válido
        if args[0] not in ['SUBSCR', 'CANCEL', 'STATUS', 'INFOS', 'STATIS', 'STATIS ALL', 'SLEEP', 'EXIT']:
            print("UNKNOWN-COMMAND")
            continue

        # verifica se o comando tem o número correcto de argumentos
        if args[0] == 'SUBSCR':
            if len(args) < 3:
                print("MISSING-ARGUMENTS")
                continue
            try:
                timeout = int(args[2])
                args[2] = str(timeout + int(time.time()))
            except ValueError:
                print("INVALID-ARGUMENTS")
                continue

        if args[0] == 'STATIS' and args[1] == 'L' and len(args) < 3:
            print("MISSING-ARGUMENTS")
            continue

        elif args[0] in ['CANCEL', 'STATUS', 'INFOS', 'STATIS'] and len(args) < 2:
            print("MISSING-ARGUMENTS")
            continue

        # sleep durante o número de segundos especificado
        elif args[0] == 'SLEEP':
            time.sleep(int(args[1]))
            continue

        # enviar comando ao servidor
        response = s.send_receive(command)

        # resposta do servidor de impressão
        print(response)

        # Sair se o comando for EXIT
        if command == "EXIT":
            break

    print("ligacao terminada")
    # desconecta do servidor
    s.close()


if __name__ == '__main__':
    main()
