#include "SimConnectBridge.h"
#include <iostream>

#pragma comment(lib, "SimConnect.lib")

SimConnectBridge::SimConnectBridge() : encoder(mappingConfig) {}

SimConnectBridge::~SimConnectBridge() {
    stop();
}

bool SimConnectBridge::isRunning() const {
    return running;
}

void SimConnectBridge::start(const std::string& ipAddress, int port) {
    if (running) return;

    std::lock_guard<std::mutex> lock(bridgeMutex);
    running = true;
    udpClient.connect(ipAddress, port);
    bridgeThread = std::thread(&SimConnectBridge::run, this);
    std::cout << "[DIS Bridge] Started" << std::endl;
}

void SimConnectBridge::stop() {
    if (!running) return;

    running = false;
    if (bridgeThread.joinable()) {
        bridgeThread.join();
    }
    std::cout << "[DIS Bridge] Stopped" << std::endl;
}

void SimConnectBridge::setupDataDefinitions() {
    SimConnect_AddToDataDefinition(hSimConnect, 1, "GPS POSITION LAT", "degrees latitude");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "GPS POSITION LON", "degrees longitude");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "INDICATED ALTITUDE", "feet");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "ATTITUDE INDICATOR PITCH DEGREES", "degrees");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "ATTITUDE INDICATOR BANK DEGREES", "degrees");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "HEADING INDICATOR", "degrees");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "AIRSPEED INDICATED", "knots");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "ROTATION VELOCITY BODY Y", "feet per second");
}

void SimConnectBridge::run() {
    if (FAILED(SimConnect_Open(&hSimConnect, "DIS Bridge", nullptr, 0, 0, 0))) {
        std::cerr << "Failed to open SimConnect" << std::endl;
        running = false;
        return;
    }

    setupDataDefinitions();
    SimConnect_RequestDataOnSimObject(hSimConnect, 1, 1, SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD_SECOND);

    std::cout << "[DIS Bridge] Running..." << std::endl;

    while (running) {
        SimConnect_CallDispatch(hSimConnect, dispatchCallback, this);
        Sleep(100);
    }

    SimConnect_Close(hSimConnect);
    hSimConnect = NULL;
}

void CALLBACK SimConnectBridge::dispatchCallback(SIMCONNECT_RECV* pData, DWORD cbData, void* pContext) {
    auto* bridge = static_cast<SimConnectBridge*>(pContext);

    if (pData->dwID == SIMCONNECT_RECV_ID_SIMOBJECT_DATA) {
        auto* pObjData = (SIMCONNECT_RECV_SIMOBJECT_DATA*)pData;
        if (pObjData->dwRequestID == 1) {
            FlightData* fd = reinterpret_cast<FlightData*>(&pObjData->dwData);
            auto packet = bridge->encoder.encodeEvent(*fd);
            bridge->udpClient.send(packet);

            std::cout << "[DIS Bridge] lat=" << fd->latitude << " lon=" << fd->longitude << std::endl;
        }
    }
}
