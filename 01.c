#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/ether.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <arpa/inet.h>
#include <sys/ioctl.h>
#include <net/if.h>
#include <string.h>
#include <sys/time.h>


int main(){
	//创建原始socket
	int sockfd;
	if((sockfd=socket(AF_PACKET, SOCK_RAW, htons(ETH_P_ALL))) < 0){
		perror("创建socket失败!\n");
		exit(1);
	}
	printf("sockfd = %d\n", sockfd);
	


	//开启混杂模式
	struct ifreq ethreq;
	strcpy(ethreq.ifr_name, "ens33");

	if(ioctl(sockfd, SIOCGIFFLAGS, &ethreq) != 0)
	{
		perror("获取网络接口标记失败!\n");
		close(sockfd);
		exit(1);
	}
	printf("获取网络接口标记成功!\n");
	
	
	ethreq.ifr_flags |= IFF_PROMISC;
	printf("加入混杂模式到标志位中\n");

	if(ioctl(sockfd, SIOCSIFFLAGS, &ethreq))
	{
		perror("设置网络接口标记失败!\n");
                close(sockfd);
                exit(1);
	}
	printf("设置网络接口标记成功!\n");	
	

	
	//接收数据
	printf("开始捕获信号...\n");
	unsigned char msg[1600] = "";
	while (1){
		sleep(1);
		if(recvfrom(sockfd, msg, sizeof(msg), 0, NULL, NULL) < 0){
			perror("接收数据失败!\n");
			exit(1);	
		}
		

		//分析接收到的数据包
		unsigned char dst_mac[18] = "";
		unsigned char src_mac[18] = "";
		unsigned short type;

		sprintf(dst_mac, "%x:%x:%x:%x:%x:%x", msg[0], msg[1], msg[2], msg[3], msg[4], msg[5]);
		sprintf(src_mac, "%x:%x:%x:%x:%x:%x", msg[6], msg[7], msg[8], msg[9], msg[10], msg[11]);
		type = ntohs(*(unsigned short*)(msg+12));

		printf("源mac:%s--->目的mac:%s\n", src_mac, dst_mac);
		printf("type = %#x\n", type);

		if(type == 0x0800)
		{
			printf("捕获到IP数据报!\n");
			//IP数据报头部长度，总长度
			unsigned char ip_head_len;
			unsigned char ip_len;

			ip_head_len = ((*(unsigned short*)(msg+14))&0x0f)*4;
			ip_len = ntohs(*(unsigned short*)(msg+16));
			
			printf("ip头部:%d, ip数据报总长度:%d\n", ip_head_len, ip_len);
			
			//ip地址
			unsigned char src_ip[16] = "";
			unsigned char dst_ip[16] = "";

			sprintf(src_ip, "%u.%u.%u.%u", msg[26], msg[27], msg[28], msg[29]);
			sprintf(dst_ip, "%u.%u.%u.%u", msg[30], msg[31], msg[32], msg[33]);

			printf("源ip地址:%s--->目的ip地址:%s\n", src_ip, dst_ip);

			unsigned char ip_type;
			ip_type = *(msg+23);
			printf("ip_type = %d\n", ip_type);
			
			if(ip_type == 1)
			{
				printf("ICMP报文\n");
			}
			else if(ip_type == 2)
			{
				printf("IGMP报文\n");
			}
			else if(ip_type == 6)
			{
				printf("TCP报文\n");
				unsigned short src_port;
				unsigned short dst_port;

				src_port = (*(unsigned short*)(msg+34));
				dst_port = (*(unsigned short*)(msg+36));

				printf("源端口号:%d--->目的端口号:%d\n", src_port, dst_port);
			}
			else if(ip_type == 17)
			{
				printf("UDP报文\n");
				unsigned short src_port;
                                unsigned short dst_port;

                                src_port = (*(unsigned short*)(msg+34));
                                dst_port = (*(unsigned short*)(msg+36));

                                printf("源端口号:%d--->目的端口号:%d\n", src_port, dst_port);
			}


		}
		else if(type == 0x0806)
		{
			printf("ARP数据帧\n");
		}
		else if(type == 0x8035)
		{
			printf("RARP数据帧\n");
		}
		printf("***************************************\n");

	}	
	return 0;
}
