#include "main.h"

// MAIN
int main() {
    HRESULT hr;

    // Attempts to open connection to sim
    if (SUCCEEDED(SimConnect_Open(&hSimConnect, "My C++ Client", NULL, 0, 0, 0)))
    {
        // Error checking for connection
        std::cout << "SimConnect_Open SUCCEEDED. Waiting for connection..." << std::endl;

        // The main loop.
        while (hSimConnect)
        {
            SimConnect_CallDispatch(hSimConnect, MyDispatchProc, NULL);
            Sleep(1); // Ensures program runs loop once every millisecond
        }

        // Sim close confirmation
        std::cout << "Loop exited. Connection closed." << std::endl;
    }
    else
    {
        // This will tell you if the initial connection failed entirely.
        std::cerr << "Error: SimConnect_Open FAILED!" << std::endl;
    }

    return 0;
}
