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
    p_size = len(res) - 4
    b_size = int(int(res[1][1]) * int(res[2][1]) * 3 / p_size)
    id = int(res[0][1])
    img_bytes = b''

    ##Primera parte
    port = int(res[3][1])
    s21 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s21.connect((ip, port))

    msg = f'GET 1/{p_size} IMG ID:{id}'.encode()
    s21.sendall(msg)

    part_1 = s21.recv(b_size)
    print('Primera parte obtenida con exito!')

    s21.close()

    img_bytes += part_1

    #Segunda parte
    port = int(res[4][1])
    s22 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    msg = f'GET 2/{p_size} IMG ID:{id}'.encode()
    s22.sendto(msg, (ip, port))

    part_2 = s22.recvfrom(b_size)[0]
    print('Segunda parte obtenida con exito!')

    img_bytes += part_2

    #Tercera parte
    if(p_size == 3):
        port = int(res[5][1])
        s23 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        msg = f'GET 3/{p_size} IMG ID:{id}'.encode()
        s23.sendto(msg, (ip, port))

        part_3 = s23.recvfrom(b_size)[0]
        print('Tercera parte obtenida con exito!')

        img_bytes += part_3

    #Envio de todas las partes
    port = int(res[len(res) - 1][1])
    s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print(len(img_bytes))

    s3.connect((ip, port))

    s3.sendall(img_bytes)

    final_res = s3.recv(1024).decode()
    print(final_res)

    s3.close()

    #Abrir foto
