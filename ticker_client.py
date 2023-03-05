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
import time


ID = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])

# Programa principal


def main():
    s = net_client.server_connection(HOST, PORT)
    s.connect()
    #mandamos o ID do cliente ao servidor
    client_id_received = s.send_receive(ID)
    print(client_id_received)


    while True:
        #pedimos o comando ao utilizador
        command = input("comando > ")
        args = command.split()

        #Manipulate subscription timeout using time() function
        if args[0] == 'SUBSCR':
            try:
                timeout = int(args[2])
                args[2] = str(timeout + int(time.time()))
                
            except ValueError:
                print("INVALID-ARGUMENTS")
                continue

        # Check if command is valid
        if args[0] not in ['SUBSCR', 'CANCEL', 'STATUS', 'INFOS', 'STATIS', 'STATIS ALL', 'SLEEP', 'EXIT']:
            print("UNKNOWN-COMMAND")
            continue

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
        
        if args[0] == 'STATIS' and args[1] == 'L' and len (args) < 3:
            print("MISSING-ARGUMENTS")
            continue

        # # Check if required arguments are present
        # if args[0] == 'SUBSCR' and len(args) < 3:
        #     print("MISSING-ARGUMENTS")
        #     continue

        elif args[0] in ['CANCEL', 'STATUS', 'INFOS', 'STATIS'] and len(args) < 2:
            print("MISSING-ARGUMENTS")
            continue

        #sleep for number of seconds specified
        elif args[0] == 'SLEEP':
            time.sleep(int(args[1]))
            continue

        # Send command to server
        response = s.send_receive(command)

        # Print server response
        print(response)

        # Exit if command is EXIT
        if command == "EXIT":
            break


    # Disconnect from server
    s.close()


if __name__ == '__main__':
    main()
