#pragma once

#include "UdpClient.h"
#include "FlightData.h"
#include "MappingConfig.h"
#include "Encode.h"
#include <windows.h>
#include "SimConnect.h"
#include <string>
#include <thread>
#include <atomic>
#include <mutex>

class SimConnectBridge {
public:
    SimConnectBridge();
    ~SimConnectBridge();

    void start(const std::string& ipAddress, int port);
    void stop();
    bool isRunning() const;

private:
    void run();
    void setupDataDefinitions();
    static void CALLBACK dispatchCallback(SIMCONNECT_RECV* pData, DWORD cbData, void* pContext);

    std::atomic<bool> running{false};
    std::thread bridgeThread;
    std::mutex bridgeMutex;

    HANDLE hSimConnect = NULL;
    UdpClient udpClient;
    MappingConfig mappingConfig;
    Encode encoder;
};
