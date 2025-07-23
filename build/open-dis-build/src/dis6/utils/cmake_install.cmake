# Install script for directory: C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/dis6/utils" TYPE FILE FILES
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/Conversion.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/DataStream.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/Endian.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/IBufferProcessor.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/IncomingMessage.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/IPacketProcessor.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/IPduBank.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/Masks.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/PacketFactory.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/PDUBank.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/PduFactory.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/PDUType.h"
    "C:/Users/kilro/MSFS-DIS-Gateway-/extern/open-dis-cpp/src/dis6/utils/StreamUtils.h"
    )
endif()

