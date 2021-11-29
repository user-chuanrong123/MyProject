import socket
import ctypes
import fcntl
import time

from scapy.data import ETH_P_ALL

sockfd = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
print(sockfd)


class FLAGS(object):
    ETH_P_ALL = 0x0003
    ETH_P_IP = 0x0800
    IFF_PROMISC = 0x100
    SIOCGIFFLAGS = 0x8913
    SIOCSIFFLAGS = 0x8914

class ifreq(ctypes.Structure):
    _fields_ = [
        ("ifr_ifrn", ctypes.c_char*16),
        ("ifr_flags", ctypes.c_short)
    ]


ifr = ifreq()
ifr.ifr_ifrn = b'eth0'
fcntl.ioctl(sockfd, FLAGS.SIOCGIFFLAGS, ifr)
ifr.ifr_flags |= FLAGS.IFF_PROMISC
fcntl.ioctl(sockfd, FLAGS.SIOCSIFFLAGS, ifr)

while(1):
    time.sleep(1)
    nData, addr = sockfd.recvfrom(65535)
    print(nData)










