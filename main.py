import socket

if __name__ == '__main__':
    ip = 'jdiaz.inf.santiago.usm.cl'
    port = 50008

    #Paso 1
    s1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    msg = 'GET NEW IMG DATA'.encode()
    s1.sendto(msg, (ip, port))

    res = s1.recvfrom(1024)[0].decode()

    res = res.split(' ')
    res = [x.split(':') for x in res]

    print(res)

    #Paso 2
    b_size = len(res) - 4
    id = int(res[0][1])

    ##Primera parte
    port = int(res[3][1])
    s21 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s21.connect((ip, port))

    msg = f'GET 1/{b_size} IMG ID:{id}'.encode()
    s21.sendall(msg)

    part_1 = s21.recv(1024)
    print('Primera parte obtenida con exito!')

    s21.close()

    #Segunda parte
    port = int(res[4][1])
    s22 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    msg = f'GET 2/{b_size} IMG ID:{id}'.encode()
    s22.sendto(msg, (ip, port))

    part_2 = s22.recvfrom(1024)
    print('Segunda parte obtenida con exito!')

    #Tercera parte
    if(b_size == 3):
        port = int(res[5][1])
        s23 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        msg = f'GET 3/{b_size} IMG ID:{id}'.encode()
        s23.sendto(msg, (ip, port))

        part_3 = s23.recvfrom(1024)
        print('Tercera parte obtenida con exito!')

    #Envio de todas las partes
    print(part_1, part_2, part_3)