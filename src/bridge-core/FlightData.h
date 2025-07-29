#pragma once

#include <iostream>
#include <windows.h>
#include "SimConnect.h"

HANDLE hSimConnect = NULL; // Holds connection to SimConnect
DWORD userAircraftObjectID;

// Flight Data Struct
struct FlightData {
    double latitude;
    double longitude;
    double altitude;
    double pitch;
    double bank;
    double heading;
    double airspeed;
    double yaw;
};

// Constants
enum EVENT_ID {
    EVENT_USER_VEHICLE = 1
};

enum DATA_DEFINE_ID {
    DEFINITION_FLIGHT_DATA = 1
};

enum DATA_REQUEST_ID {
    REQUEST_FLIGHT_DATA = 1
};

// Prototypes
void CALLBACK MyDispatchProc(SIMCONNECT_RECV* pData, DWORD cbData, void* pContext);
void setupDataRequests(DWORD objectID);
