#pragma once

#include <winsock2.h>
#include <Ws2tcpip.h>
#include <string>
#include <vector>
#include <cstdint>

#pragma comment(lib, "ws2_32.lib")

class UdpClient {
public:
    UdpClient();
    ~UdpClient();

    bool connect(const std::string& ipAddress, int port);
    void send(const std::vector<uint8_t>& data);
    void close();

private:
    SOCKET udpSocket;
    sockaddr_in destAddr;
    bool connected = false;
};
