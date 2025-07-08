#include "Encode.h"
#include "MappingConfig.h"
#include <DIS/EntityStatePdu.h>
#include <DIS/DataStream.h>
#include <iostream>

Encode::Encode(MappingConfig& config)
    : config_(config)
{}

std::vector<uint8_t> Encode::encodeEvent(const FlightData& fd) {
    // Convert raw FlightData to InternalEvent
    InternalEvent event = config_.createEventFromFlightData(fd);

    // Map InternalEvent → DIS PDU
    std::unique_ptr<DIS::Pdu> pdu = config_.createPduFromEvent(event);
    if (!pdu) {
        throw std::runtime_error("MappingConfig failed to create PDU from event");
    }

    // Marshal PDU to byte buffer
    DIS::DataStream ds;
    pdu->marshal(ds);
    const auto& raw = ds.getData();
    return std::vector<uint8_t>(raw.begin(), raw.end());
}
