#pragma once

#include <crow.h>
#include "SimConnectBridge.h"
#include "Base64Encoder.h"
#include "Encode.h"
#include "MappingConfig.h"

class WebServer {
public:
    WebServer();
    void run();

private:
    void setupRoutes();

    crow::SimpleApp app;
    SimConnectBridge bridge;
    MappingConfig mappingConfig;
    Encode encoder;
};
