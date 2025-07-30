#include "WebServer.h"
#include "FlightData.h"
#include <iostream>

WebServer::WebServer() : encoder(mappingConfig) {
    setupRoutes();
}

void WebServer::setupRoutes() {
    CROW_ROUTE(app, "/api/flightdata").methods("POST"_method)([&](const crow::request& req) {
        auto x = crow::json::load(req.body);
        if (!x) {
            return crow::response(400, "Invalid JSON");
        }

        FlightData fd;
        fd.latitude = x["latitude"].d();
        fd.longitude = x["longitude"].d();
        fd.altitude = x["altitude"].d();
        fd.pitch = x["pitch"].d();
        fd.bank = x["bank"].d();
        fd.heading = x["heading"].d();
        fd.airspeed = x["airspeed"].d();
        fd.yaw = x["yaw"].d();

        try {
            auto packet = encoder.encodeEvent(fd);
            crow::json::wvalue res;
            res["packet"] = Base64Encoder::encode(packet);
            return crow::response{res};
        } catch (const std::exception& e) {
            return crow::response(500, e.what());
        }
    });

    CROW_ROUTE(app, "/api/status")([&] {
        crow::json::wvalue res;
        res["status"] = bridge.isRunning() ? "started" : "stopped";
        return crow::response{res};
    });

    CROW_ROUTE(app, "/api/toggle").methods("POST"_method)([&] {
        if (bridge.isRunning()) {
            bridge.stop();
        } else {
            bridge.start("192.168.1.238", 12345);
        }
        crow::json::wvalue res;
        res["status"] = bridge.isRunning() ? "started" : "stopped";
        return crow::response{res};
    });
}

void WebServer::run() {
    std::cout << "DIS REST API Server running on http://localhost:8080" << std::endl;
    app.port(8080).multithreaded().run();
}
