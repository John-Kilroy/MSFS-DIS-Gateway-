# Install script for directory: C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "C:/Program Files/msfs-dis-bridge")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/dis6" TYPE FILE FILES
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AcknowledgePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AcknowledgeReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AcousticBeamData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AcousticBeamFundamentalParameter.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AcousticEmitter.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AcousticEmitterSystemData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AcousticEmitterSystem.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ActionRequestPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ActionRequestReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ActionResponsePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ActionResponseReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AggregateID.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AggregateMarking.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AggregateStatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AggregateType.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AngularVelocityVector.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/AntennaLocation.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ApaData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ArealObjectStatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ArticulationParameter.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/BeamAntennaPattern.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/BeamData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/BurstDescriptor.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ClockTime.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/CollisionElasticPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/CollisionPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/CommentPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/CommentReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/CreateEntityPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/CreateEntityReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DataPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DataQueryPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DataQueryReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DataReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DeadReckoningParameter.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DesignatorPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DetonationPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/DistributedEmissionsFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EightByteChunk.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ElectromagneticEmissionBeamData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ElectromagneticEmissionsPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ElectromagneticEmissionSystemData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EmitterSystem.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EntityID.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EntityInformationFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EntityManagementFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EntityStatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EntityStateUpdatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EntityType.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EnvironmentalProcessPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Environment.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EventID.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EventReportPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/EventReportReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/FastEntityStatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/FirePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/FixedDatum.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/FourByteChunk.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/FundamentalParameterData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/FundamentalParameterDataIff.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/GridAxisRecord.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/GridAxisRecordRepresentation0.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/GridAxisRecordRepresentation1.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/GridAxisRecordRepresentation2.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/GriddedDataPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IffAtcNavAidsLayer1Pdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IffAtcNavAidsLayer2Pdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IffFundamentalData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IntercomCommunicationsParameters.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IntercomControlPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IntercomSignalPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IsGroupOfPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/IsPartOfPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/LayerHeader.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/LinearObjectStatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/LinearSegmentParameter.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/LogisticsFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/LogisticsPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Marking.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/MinefieldDataPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/MinefieldFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/MinefieldPduFamily.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/MinefieldQueryPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/MinefieldResponseNackPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/MinefieldStatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ModulationType.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/NamedLocation.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ObjectType.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Orientation.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/PduContainer.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Pdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Point.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/PointObjectStatePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/PropulsionSystemData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RadioCommunicationsFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RadioEntityType.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ReceiverPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RecordQueryReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RecordSet.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Relationship.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RemoveEntityPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RemoveEntityReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RepairCompletePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/RepairResponsePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ResupplyCancelPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ResupplyOfferPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ResupplyReceivedPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SeesPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ServiceRequestPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SetDataPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SetDataReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SetRecordReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/ShaftRPMs.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SignalPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SimulationAddress.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SimulationManagementFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SimulationManagementWithReliabilityFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SixByteChunk.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SphericalHarmonicAntennaPattern.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/StartResumePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/StartResumeReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/StopFreezePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/StopFreezeReliablePdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SupplyQuantity.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/symbolic_names.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SyntheticEnvironmentFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/SystemID.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/TrackJamTarget.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/TransferControlRequestPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/TransmitterPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/TwoByteChunk.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/UaPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/VariableDatum.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Vector3Double.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/Vector3Float.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/VectoringNozzleSystemData.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/WarfareFamilyPdu.h"
    "C:/Users/Jack/MSFS-DIS-Gateway-/build/open-dis-build/src/dis6/opendis6_export.h"
    )
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("C:/Users/Jack/MSFS-DIS-Gateway-/build/open-dis-build/src/dis6/utils/cmake_install.cmake")

endif()

