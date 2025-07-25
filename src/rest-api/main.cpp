#include <crow.h>
#include "Encode.h"
#include "Decode.h"
#include "MappingConfig.h"
#include "FlightData.h"

#include <vector>
#include <string>
#include <iostream>
#include <mutex>
#include <thread>
#include <atomic>

// Base64 encoder (utility)
static const std::string base64_chars =
"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
"abcdefghijklmnopqrstuvwxyz"
"0123456789+/";

static std::string base64_encode(const std::vector<uint8_t>& bytes) {
    std::string ret;
    int val = 0, valb = -6;
    for (uint8_t c : bytes) {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0) {
            ret.push_back(base64_chars[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6) ret.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
    while (ret.size() % 4) ret.push_back('=');
    return ret;
}

// Global bridge state
std::atomic<bool> disBridgeRunning{ false };
std::mutex bridgeMutex;
std::thread bridgeThread;

void run_dis_bridge() {
    while (disBridgeRunning) {
        std::cout << "[DIS Bridge] Sending data..." << std::endl;
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    std::cout << "[DIS Bridge] Stopped thread" << std::endl;
}

int main() {
    crow::SimpleApp app;

    MappingConfig config;
    Encode encoder(config);
    Decode decoder(config);

    // POST /api/flightdata
    CROW_ROUTE(app, "/api/flightdata").methods("POST"_method)(
        [&](const crow::request& req) {
            auto x = crow::json::load(req.body);
            if (!x) return crow::response(400, "Invalid JSON");

            FlightData fd;
            fd.latitude = x["latitude"].d();
            fd.longitude = x["longitude"].d();
            fd.altitude = x["altitude"].d();
            fd.pitch = x["pitch"].d();
            fd.bank = x["bank"].d();
            fd.heading = x["heading"].d();
            fd.airspeed = x["airspeed"].d();

            std::vector<uint8_t> packet;
            try {
                packet = encoder.encodeEvent(fd);
            }
            catch (const std::exception& e) {
                return crow::response(500, e.what());
            }

            crow::json::wvalue res;
            res["packet"] = base64_encode(packet);
            return crow::response{ res };
        }
        );

    // GET /api/status
    CROW_ROUTE(app, "/api/status")([] {
        crow::json::wvalue res;
        res["status"] = disBridgeRunning ? "started" : "stopped";
        return crow::response{ res };
        });

    CROW_ROUTE(app, "/api/toggle").methods("POST"_method)(
        [] {
            std::lock_guard<std::mutex> lock(bridgeMutex);

            if (!disBridgeRunning) {
                disBridgeRunning = true;
                bridgeThread = std::thread(run_dis_bridge);
                std::cout << "[DIS Bridge] Started\n";
            }
            else {
                disBridgeRunning = false;
                if (bridgeThread.joinable()) bridgeThread.join();
                std::cout << "[DIS Bridge] Stopped\n";
            }

            crow::json::wvalue res;
            res["status"] = disBridgeRunning ? "started" : "stopped";
            return crow::response{ res };
        });

    std::cout << "DIS REST API Server running on http://localhost:8080" << std::endl;
    app.port(8080).multithreaded().run();
    return 0;
}
