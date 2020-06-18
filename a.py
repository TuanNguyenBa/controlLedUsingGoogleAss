import socket
import matplotlib.pyplot as plt


def converage_plot(data, i):
    hum = data.split(",")[0]
    tem = data.split(",")[1]
    print('temp=' + (str(tem)) + 'iter=' + str(i))
    plt.ion()
    fig = plt.figure(num=1, figsize=(5, 5))
    if i==0:
        plt.title('iot tem and hud')

    ax = fig.add_subplot(121)
    ax.plot(tem, i, c='r', marker=r'$\Theta$')
    plt.xlabel('Temp($^O C$)')
    ax.grid()
    ax = fig.add_subplot(122)
    ax.plot(hum, i, c='b', marker=r'$\Phi$')
    plt.xlabel('humidity ($\%$)')
    ax.grid()

    fig.show()
    fig.canvas.draw()
    plt.savefig('foo.png')


# create a udp socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('192.168.43.36', 10001)
sock.bind(server_address)
i=0
while True:
    data, address = sock.recvfrom(4096)
    with open("datalog.html", "a") as f:
        mess = str(data)
        mess=mess.replace('b','')
        f.write(mess)

       # converage_plot(mess, i)
        print(mess)
        i+=1
    f.close()
