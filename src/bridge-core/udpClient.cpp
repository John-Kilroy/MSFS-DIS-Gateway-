#include "UdpClient.h"
#include <iostream>

UdpClient::UdpClient() {
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        throw std::runtime_error("WSAStartup failed");
    }
    udpSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (udpSocket == INVALID_SOCKET) {
        throw std::runtime_error("UDP socket creation failed");
    }
}

UdpClient::~UdpClient() {
    close();
    WSACleanup();
}

bool UdpClient::connect(const std::string& ipAddress, int port) {
    destAddr.sin_family = AF_INET;
    destAddr.sin_port = htons(port);
    connected = InetPtonA(AF_INET, ipAddress.c_str(), &destAddr.sin_addr) == 1;
    return connected;
}

void UdpClient::send(const std::vector<uint8_t>& data) {
    if (!connected) return;
    sendto(udpSocket,
           reinterpret_cast<const char*>(data.data()),
           static_cast<int>(data.size()), 0,
           reinterpret_cast<sockaddr*>(&destAddr),
           sizeof(destAddr));
}

void UdpClient::close() {
    if (udpSocket != INVALID_SOCKET) {
        closesocket(udpSocket);
        udpSocket = INVALID_SOCKET;
    }
    connected = false;
}
