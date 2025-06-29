cmake_minimum_required(VERSION 3.15)
project(msfs-dis-bridge VERSION 0.1.0 LANGUAGES CXX)

#--------------------------------------
# Project-wide settings
#--------------------------------------
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

#--------------------------------------
# External Dependencies
#--------------------------------------
# 1) Open-DIS (DIS-6 only)
add_subdirectory(extern/open-dis)

# 2) SimConnect SDK
include_directories(${CMAKE_SOURCE_DIR}/extern/SimConnect/include)
link_directories(${CMAKE_SOURCE_DIR}/extern/SimConnect/lib)

# 3) Microsoft Flight Simulator 2024 SDK
include_directories(${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/include)
link_directories(${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/lib)

#--------------------------------------
# Modules
#--------------------------------------
# Bridge core: decode/encode, mapping, threading
add_subdirectory(src/bridge-core)

# SimConnect adapter: wraps SimConnect calls
add_subdirectory(src/simconnect-adapter)

# REST API service (C++ version)
add_subdirectory(src/rest-api)

# (Optional) UI module if using CMake for web UI assets
# add_subdirectory(src/ui)

#--------------------------------------
# Testing
#--------------------------------------
enable_testing()
add_subdirectory(tests/pdu-replay)
add_subdirectory(tests/simconnect-mock)

#--------------------------------------
# Install Rules
#--------------------------------------
# install(TARGETS bridge-core simconnect-adapter rest-api
#         RUNTIME DESTINATION bin
#         LIBRARY DESTINATION lib
#         ARCHIVE DESTINATION lib/static)

# install(DIRECTORY extern/open-dis/dis6/include DESTINATION include/open-dis)
