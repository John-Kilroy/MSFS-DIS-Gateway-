cmake_minimum_required(VERSION 3.18)
project(msfs-dis-bridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set output directories
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)  # For static libraries
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)  # For shared libraries
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)  # For executables

# ---------------------------------------------------------------------------
# 1) open‑DIS (DIS 6) submodule
# ---------------------------------------------------------------------------
set(OPENDIS_SOURCE_DIR ${CMAKE_SOURCE_DIR}/extern/open-dis-cpp)
set(OPENDIS_BUILD_DIR ${CMAKE_BINARY_DIR}/open-dis-build)
add_subdirectory(${OPENDIS_SOURCE_DIR} ${OPENDIS_BUILD_DIR})
include_directories(
    ${OPENDIS_SOURCE_DIR}/src
    ${OPENDIS_BUILD_DIR}/src
)

# ---------------------------------------------------------------------------
# 2) SimConnect SDK
# ---------------------------------------------------------------------------
set(SIMCONNECT_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/SimConnect SDK/include")
set(SIMCONNECT_LIB_DIR "${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/SimConnect SDK/lib")
include_directories(${SIMCONNECT_INCLUDE_DIR})

# ---------------------------------------------------------------------------
# 3) bridge-core library - BUILD AS STATIC LIBRARY
# ---------------------------------------------------------------------------
# Change to static library
add_library(bridge-core STATIC
    src/bridge-core/Encode.cpp
    src/bridge-core/Decode.cpp
    src/bridge-core/MappingConfig.cpp
)

target_include_directories(bridge-core PUBLIC
    ${CMAKE_SOURCE_DIR}/src/bridge-core
    ${OPENDIS_SOURCE_DIR}/src
    ${OPENDIS_BUILD_DIR}/src
)

target_link_libraries(bridge-core PRIVATE
    OpenDIS6
)

# ---------------------------------------------------------------------------
# 4) TestBridge executable with DLL copy
# ---------------------------------------------------------------------------
add_executable(TestBridge
    tests/pdu-replay/TestBridge.cpp
)

target_include_directories(TestBridge PRIVATE
    ${SIMCONNECT_INCLUDE_DIR}
    ${OPENDIS_SOURCE_DIR}/src
    ${OPENDIS_BUILD_DIR}/src
)

if(WIN32)
    target_link_libraries(TestBridge PRIVATE
        bridge-core
        "${SIMCONNECT_LIB_DIR}/SimConnect.lib"
        OpenDIS6
    )
    
    # Add DLL copy command
    add_custom_command(TARGET TestBridge POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy
            "${SIMCONNECT_LIB_DIR}/SimConnect.dll"
            $<TARGET_FILE_DIR:TestBridge>
        COMMENT "Copying SimConnect.dll to output directory"
    )
endif()

# ---------------------------------------------------------------------------
# 5) (Optional) install rules
# ---------------------------------------------------------------------------
# install(TARGETS bridge-core TestBridge EXPORT msfs_dis_bridge)
# install(DIRECTORY src/bridge-core/ DESTINATION include/bridge-core)