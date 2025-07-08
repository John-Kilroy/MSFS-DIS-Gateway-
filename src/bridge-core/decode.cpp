#include "Decode.h"
#include "MappingConfig.h"
#include <DIS/PduFactory.h>
#include <DIS/DataStream.h>
#include <iostream>

Decode::Decode(MappingConfig& config)
    : config_(config)
{}

FlightData Decode::decodePacket(const std::vector<uint8_t>& buffer) {
    // Unmarshal buffer into DIS PDU
    DIS::DataStream ds(buffer.begin(), buffer.end());
    std::unique_ptr<DIS::Pdu> pdu(DIS::PduFactory::createPdu(&ds));
    if (!pdu) {
        throw std::runtime_error("Failed to decode PDU from buffer");
    }

    // Convert PDU to InternalEvent
    InternalEvent event = config_.createEventFromPdu(*pdu);

    // Map InternalEvent to FlightData
    return config_.createFlightDataFromEvent(event);
}
