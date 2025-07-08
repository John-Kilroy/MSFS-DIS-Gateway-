#include "MappingConfig.h"
#include <DIS/EntityStatePdu.h>
#include <stdexcept>

MappingConfig::MappingConfig() {
    // Hard-code one mapping: FlightData events ↔ EntityStatePdu
    eventToPduMap_["FlightDataUpdate"] = "EntityStatePdu";
    pduToEventMap_["EntityStatePdu"] = "FlightDataUpdate";
}

InternalEvent MappingConfig::createEventFromFlightData(const FlightData& fd) const {
    InternalEvent ev;
    ev.name = "FlightDataUpdate";
    ev.payload.clear();
    ev.payload["latitude"]  = fd.latitude;
    ev.payload["longitude"] = fd.longitude;
    ev.payload["altitude"]  = fd.altitude;
    ev.payload["pitch"]     = fd.pitch;
    ev.payload["bank"]      = fd.bank;
    ev.payload["heading"]   = fd.heading;
    ev.payload["airspeed"]  = fd.airspeed;
    return ev;
}

std::unique_ptr<DIS::Pdu> MappingConfig::createPduFromEvent(const InternalEvent& event) const {
    auto it = eventToPduMap_.find(event.name);
    if (it == eventToPduMap_.end()) return nullptr;

    if (it->second == "EntityStatePdu") {
        auto pdu = std::make_unique<DIS::EntityStatePdu>();
        const auto& pl = event.payload;
        pdu->setEntityLocation(
            static_cast<float>(pl.at("latitude")),
            static_cast<float>(pl.at("longitude")),
            static_cast<float>(pl.at("altitude"))
        );
        pdu->setOrientation(
            static_cast<float>(pl.at("pitch")),
            static_cast<float>(pl.at("bank")),
            static_cast<float>(pl.at("heading"))
        );
        // Optionally set velocity or other fields here
        return pdu;
    }
    return nullptr;
}

InternalEvent MappingConfig::createEventFromPdu(const DIS::Pdu& pdu) const {
    std::string type = pdu.getClassName();
    auto it = pduToEventMap_.find(type);
    if (it == pduToEventMap_.end()) return {};

    InternalEvent ev;
    ev.name = it->second;
    if (type == "EntityStatePdu") {
        const auto& esp = static_cast<const DIS::EntityStatePdu&>(pdu);
        auto& pl = ev.payload;
        auto pos = esp.getEntityLocation();
        auto orient = esp.getOrientation();
        pl["latitude"]  = pos.getX();
        pl["longitude"] = pos.getY();
        pl["altitude"]  = pos.getZ();
        pl["pitch"]     = orient.getPhi();
        pl["bank"]      = orient.getTheta();
        pl["heading"]   = orient.getPsi();
    }
    return ev;
}

FlightData MappingConfig::createFlightDataFromEvent(const InternalEvent& event) const {
    FlightData fd{};
    const auto& pl = event.payload;
    fd.latitude  = pl.at("latitude");
    fd.longitude = pl.at("longitude");
    fd.altitude  = pl.at("altitude");
    fd.pitch     = pl.at("pitch");
    fd.bank      = pl.at("bank");
    fd.heading   = pl.at("heading");
    fd.airspeed  = pl.count("airspeed") ? pl.at("airspeed") : 0.0;
    return fd;
}
