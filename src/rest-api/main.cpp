#include <crow.h>
#include "Encode.h"
#include "Decode.h"
#include "MappingConfig.h"
#include "FlightData.h"

#include <winsock2.h>
#include <Ws2tcpip.h>
#include <windows.h>
#include "SimConnect.h"

#include <vector>
#include <string>
#include <iostream>
#include <mutex>
#include <thread>
#include <atomic>
#include <chrono>
#include <unordered_map>

#pragma comment(lib, "ws2_32.lib")
#pragma comment(lib, "SimConnect.lib")

// JWT-like token structure (temp), will probably use JWT++ or other for ease of implementation
struct auth_token
{
    std::string token;
    std::chrono::steady_clock::time_point expiry;
    std::string username;
};

// hard-coded users (temp)
std::unordered_map<std::string, std::string> users = {
    {"admin", "password123"},
    {"operator", "bridge321"}};

// Active tokens
std::unordered_map<std::string, auth_token> active_tokens;
std::mutex auth_mutex;

// Base64 encoder
static const std::string base64_chars =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "abcdefghijklmnopqrstuvwxyz"
    "0123456789+/";

static std::string base64_encode(const std::vector<uint8_t> &bytes)
{
    std::string ret;
    int val = 0, valb = -6;
    for (uint8_t c : bytes)
    {
        val = (val << 8) + c;
        valb += 8;
        while (valb >= 0)
        {
            ret.push_back(base64_chars[(val >> valb) & 0x3F]);
            valb -= 6;
        }
    }
    if (valb > -6)
        ret.push_back(base64_chars[((val << 8) >> (valb + 8)) & 0x3F]);
    while (ret.size() % 4)
        ret.push_back('=');
    return ret;
}

// token generator (temp)
std::string generate_token(const std::string &username)
{
    auto now = std::chrono::steady_clock::now();
    auto timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
    return base64_encode(std::vector<uint8_t>(username.begin(), username.end())) +
           "_" + std::to_string(timestamp);
}

// Token validation middleware (separate module)
bool validate_token(const std::string &token)
{
    std::lock_guard<std::mutex> lock(auth_mutex);
    auto it = active_tokens.find(token);
    if (it == active_tokens.end())
        return false;

    auto now = std::chrono::steady_clock::now();
    if (now > it->second.expiry)
    {
        active_tokens.erase(it);
        return false;
    }
    return true;
}

// Extract token from Authorization header
std::string extract_token(const crow::request &req)
{
    auto auth_header = req.get_header_value("Authorization");
    if (auth_header.empty())
        return "";

    // Expect "Bearer <token>"
    if (auth_header.substr(0, 7) == "Bearer ")
    {
        return auth_header.substr(7);
    }
    return "";
}

// Get current timestamp
std::string get_timestamp()
{
    auto now = std::chrono::system_clock::now();
    auto time_t = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::gmtime(&time_t), "%Y-%m-%dT%H:%M:%SZ");
    return ss.str();
}

// Globals
std::atomic<bool> disBridgeRunning{false};
std::mutex bridgeMutex;
std::thread bridgeThread;
std::chrono::steady_clock::time_point bridgeStartTime;

HANDLE hSimConnect = NULL;
SOCKET udpSocket;
sockaddr_in dest;

static MappingConfig mappingConfig;
static Encode encoder(mappingConfig);
static Decode decoder(mappingConfig);

// SimConnect Callback
void CALLBACK MyDispatchProc(SIMCONNECT_RECV *pData, DWORD cbData, void *pContext)
{
    switch (pData->dwID)
    {
    case SIMCONNECT_RECV_ID_SIMOBJECT_DATA:
    {
        auto *pObjData = (SIMCONNECT_RECV_SIMOBJECT_DATA *)pData;
        if (pObjData->dwRequestID == 1)
        {
            FlightData *fd = reinterpret_cast<FlightData *>(&pObjData->dwData);
            auto packet = encoder.encodeEvent(*fd);

            // Send over UDP
            sendto(udpSocket,
                   reinterpret_cast<const char *>(packet.data()),
                   static_cast<int>(packet.size()), 0,
                   reinterpret_cast<sockaddr *>(&dest),
                   sizeof(dest));

            std::cout << "[DIS Bridge] lat=" << fd->latitude
                      << " lon=" << fd->longitude << std::endl;
        }
        break;
    }
    default:
        break;
    }
}

// DIS Bridge logic
void run_dis_bridge()
{
    // UDP setup
    udpSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    dest.sin_family = AF_INET;
    dest.sin_port = htons(12345);
    InetPtonA(AF_INET, "192.168.1.238", &dest.sin_addr);

    // SimConnect setup
    HRESULT hr = SimConnect_Open(&hSimConnect, "DIS Bridge", nullptr, 0, 0, 0);
    if (FAILED(hr))
    {
        std::cerr << "Failed to open SimConnect" << std::endl;
        disBridgeRunning = false;
        return;
    }

    SimConnect_AddToDataDefinition(hSimConnect, 1, "GPS POSITION LAT", "degrees latitude");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "GPS POSITION LON", "degrees longitude");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "INDICATED ALTITUDE", "feet");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "ATTITUDE INDICATOR PITCH DEGREES", "degrees");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "ATTITUDE INDICATOR BANK DEGREES", "degrees");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "HEADING INDICATOR", "degrees");
    SimConnect_AddToDataDefinition(hSimConnect, 1, "AIRSPEED INDICATED", "knots");

    SimConnect_RequestDataOnSimObject(hSimConnect, 1, 1, SIMCONNECT_OBJECT_ID_USER, SIMCONNECT_PERIOD_SECOND);

    std::cout << "[DIS Bridge] Running..." << std::endl;

    while (disBridgeRunning)
    {
        SimConnect_CallDispatch(hSimConnect, MyDispatchProc, nullptr);
        Sleep(100);
    }

    closesocket(udpSocket);
    SimConnect_Close(hSimConnect);
    std::cout << "[DIS Bridge] Stopped" << std::endl;
}

int main()
{
    crow::SimpleApp app;

    // Authentication

    CROW_ROUTE(app, "/api/auth/login").methods("POST"_method)([&](const crow::request &req)
                                                              {
            auto data = crow::json::load(req.body);
            if (!data || !data.has("username") || !data.has("password"))
                return crow::response(400, "Missing username or password");

            std::string username = data["username"].s();
            std::string password = data["password"].s();

            /*
            // Validation would be here
            */

            std::string token = generate_token(username);
            auto expiry = std::chrono::steady_clock::now() + std::chrono::hours(1);

            {
                std::lock_guard<std::mutex> lock(auth_mutex);
                active_tokens[token] = {token, expiry, username};
            }

            crow::json::wvalue res;
            res["token"] = token;
            return crow::response{res}; });

    CROW_ROUTE(app, "/api/auth/refresh").methods("POST"_method)([&](const crow::request &req) {

            auto data = crow::json::load(req.body);
            if (!data || !data.has("token"))
                return crow::response(400, "Missing token");

            std::string old_token = data["token"].s();

            {
                std::lock_guard<std::mutex> lock(auth_mutex);
                auto it = active_tokens.find(old_token);
                if (it == active_tokens.end())
                return crow::response(401, "Invalid token");

                std::string new_token = generate_token(it->second.username);
                auto expiry = std::chrono::steady_clock::now() + std::chrono::hours(1);

                active_tokens[new_token] = {new_token, expiry, it->second.username};
                active_tokens.erase(it);

                crow::json::wvalue res;
                res["token"] = new_token;
                return crow::response { res };
            }


    });

    CROW_ROUTE(app, "/api/flightdata").methods("POST"_method)([&](const crow::request &req)
                                                              {
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
            return crow::response{ res }; });

    CROW_ROUTE(app, "/api/status")([]
                                   {
        crow::json::wvalue res;
        res["status"] = disBridgeRunning ? "started" : "stopped";
        return crow::response{ res }; });

    // CROW_ROUTE(app, "/api/heatlh").methods("GET"_method)([&] (const crow::request &req) {});

    CROW_ROUTE(app, "/api/toggle").methods("POST"_method)([]
                                                          {
        std::lock_guard<std::mutex> lock(bridgeMutex);

        if (!disBridgeRunning) {
            disBridgeRunning = true;
            bridgeThread = std::thread(run_dis_bridge);
            std::cout << "[DIS Bridge] Started" << std::endl;
        }
        else {
            disBridgeRunning = false;
            if (bridgeThread.joinable()) bridgeThread.join();
            std::cout << "[DIS Bridge] Stopped" << std::endl;
        }

        crow::json::wvalue res;
        res["status"] = disBridgeRunning ? "started" : "stopped";
        return crow::response{ res }; });

    std::cout << "DIS REST API Server running on http://localhost:8080" << std::endl;
    app.port(8080).multithreaded().run();
    return 0;
}
