#include "Encode.h"
#include "MappingConfig.h"
#include <dis6/EntityStatePdu.h>
#include <GeographicLib/Geocentric.hpp>
#include <iostream>

#include <chrono>
#include <iostream>
#include <random>
#include <unordered_map>

Encode::Encode(MappingConfig& config)
    : config_(config)
{}

std::vector<uint8_t> Encode::encodeEvent(const FlightData& fd) {
    // Convert raw FlightData to InternalEvent
    InternalEvent event = config_.createEventFromFlightData(fd);

    if(event.name == "FlightDataUpdate") {
        double X, Y, Z;
        GeographicLib::Geocentric::WGS84().Forward(fd.latitude, fd.longitude, fd.altitude, X, Y, Z);
        //ellipsoidal::Point(-37.0, 144.0, 0.0, ellipsoidal::Datum::Type::WGS84);
        //erkir::ellipsoidal::Point cartesian = erkirPoint.toCartesianPoint();
        //printf("X: " + cartesian->x() + " Y: " + cartesian->y() + " Z: " + cartesian->z());
        event.payload["X"] = X;
        event.payload["Y"] = Y;
        event.payload["Z"] = Z;
        std::cout << "X: " << X << "\nY: " << Y << "\nZ: " << Z << "\n";
    }

    // Map InternalEvent → DIS PDU
    std::unique_ptr<DIS::Pdu> pdu = config_.createPduFromEvent(event);
    if (!pdu) {
        throw std::runtime_error("MappingConfig failed to create PDU from event");
    }

    // Create DataStream with default buffer
    DIS::DataStream ds(DIS::BIG);
    
    // Marshal the PDU
    pdu->marshal(ds);
    
    // Access the internal buffer through pointer arithmetic
    const char* buffer_ptr = &ds[0];
    size_t buffer_size = ds.size();
    
    return std::vector<uint8_t>(buffer_ptr, buffer_ptr + buffer_size);
}