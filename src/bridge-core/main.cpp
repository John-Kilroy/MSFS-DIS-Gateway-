#include "WebServer.h"
#include <iostream>

int main() {
    try {
        WebServer server;
        server.run();
    } catch (const std::exception& e) {
        std::cerr << "An unexpected error occurred: " << e.what() << std::endl;
        return 1;
    }
    return 0;
}
