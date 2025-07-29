#include "FlightData.h"

// Function SimConnect sends data with
void CALLBACK MyDispatchProc(SIMCONNECT_RECV* pData, DWORD cbData, void* pContext) {

    switch (pData->dwID) {

    case SIMCONNECT_RECV_ID_OPEN: {
        std::cout << "EVENT: SIMCONNECT_RECV_ID_OPEN - Connection established." << std::endl;

        // Gets user vehicle ID
        userAircraftObjectID = SIMCONNECT_OBJECT_ID_USER;
        std::cout << "User aircraft ID: " << userAircraftObjectID << std::endl;

        setupDataRequests(userAircraftObjectID);
        break;
    }

    case SIMCONNECT_RECV_ID_EVENT: {
        SIMCONNECT_RECV_EVENT* pEvent = (SIMCONNECT_RECV_EVENT*)pData;

        if (pEvent->uEventID == EVENT_USER_VEHICLE) {
            userAircraftObjectID = pEvent->dwData;
            std::cout << "EVENT: Received UserVehicle. Aircraft Object ID is: " << userAircraftObjectID << std::endl;

            setupDataRequests(userAircraftObjectID);
        }
        break;
    }

    case SIMCONNECT_RECV_ID_SIMOBJECT_DATA: {
        SIMCONNECT_RECV_SIMOBJECT_DATA* pObjData = (SIMCONNECT_RECV_SIMOBJECT_DATA*)pData;

        if (pObjData->dwRequestID == REQUEST_FLIGHT_DATA) {
            FlightData* pFlightData = (FlightData*)&pObjData->dwData; // The takes data from simconnect and casts the flightdata struct on it


            // This is the data output to console, can be converted to file if necessary.
            std::cout << "\r"
                << "Lat: " << pFlightData->latitude
                << ", Lon: " << pFlightData->longitude
                << ", Alt: " << pFlightData->altitude << " ft"
                << ", Pitch: " << pFlightData->pitch << "°"
                << ", Bank: " << pFlightData->bank << "°"
                << ", Hdg: " << pFlightData->heading << "°"
                << ", IAS: " << pFlightData->airspeed << " kts"
                << ", Yaw: " << pFlightData->yaw << "ft/s"
                << "          " << std::flush;
        }
        break;
    }

    case SIMCONNECT_RECV_ID_QUIT: {
        std::cout << "\nEVENT: SIMCONNECT_RECV_ID_QUIT - Simulator has exited." << std::endl;

        hSimConnect = NULL;
        break;
    }

    case SIMCONNECT_RECV_ID_EXCEPTION: {
        SIMCONNECT_RECV_EXCEPTION* pException = (SIMCONNECT_RECV_EXCEPTION*)pData;
        std::cerr << "\n*** SIMCONNECT EXCEPTION! ***" << std::endl;
        std::cerr << "    Exception Code: " << pException->dwException
            << " (SendID: " << pException->dwSendID
            << ", Index: " << pException->dwIndex << ")" << std::endl;
        break;
        }
    }
}

// This function tells simconnect what data we want to extract
void setupDataRequests(DWORD objectID) {
    HRESULT hr;
    std::cout << "Setting up data requests for Object ID: " << objectID << std::endl;

    // Setup for data extraction.
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "GPS POSITION LAT", "degrees latitude");
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "GPS POSITION LON", "degrees longitude");
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "INDICATED ALTITUDE", "feet");
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "ATTITUDE INDICATOR PITCH DEGREES", "degrees");
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "ATTITUDE INDICATOR BANK DEGREES", "degrees");
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "HEADING INDICATOR", "degrees");
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "AIRSPEED INDICATED", "knots");
    hr = SimConnect_AddToDataDefinition(hSimConnect, DEFINITION_FLIGHT_DATA, "ROTATION VELOCITY BODY Y", "feet per second");

    // Request data SIMCONNECT_PERIOD_SECOND, can also be frame for period. We can have our own timing via the sleep call in main.
    hr = SimConnect_RequestDataOnSimObject(hSimConnect, REQUEST_FLIGHT_DATA, DEFINITION_FLIGHT_DATA, objectID, SIMCONNECT_PERIOD_SECOND);

    if (SUCCEEDED(hr)) {
        std::cout << "Successfully set up data request." << std::endl;
    }
    else {
        std::cerr << "Failed to request flight data." << std::endl;
    }
}
