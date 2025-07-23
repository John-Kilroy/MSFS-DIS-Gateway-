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
)

# ---------------------------------------------------------------------------
# 2) SimConnect SDK
# ---------------------------------------------------------------------------
set(SIMCONNECT_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/SimConnect SDK/include")
set(SIMCONNECT_LIB_DIR     "${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/SimConnect SDK/lib")
include_directories(${SIMCONNECT_INCLUDE_DIR})

# ---------------------------------------------------------------------------
# 3) Crow HTTP framework submodule
# ---------------------------------------------------------------------------
set(CROW_SOURCE_DIR ${CMAKE_SOURCE_DIR}/extern/crow)
set(CROW_INCLUDE_DIR ${CROW_SOURCE_DIR}/include)
add_subdirectory(${CROW_SOURCE_DIR} ${CMAKE_BINARY_DIR}/crow-build)
include_directories(${CROW_INCLUDE_DIR})

# ---------------------------------------------------------------------------
# 4) bridge-core library - BUILD AS STATIC LIBRARY
# ---------------------------------------------------------------------------
add_library(bridge-core STATIC
    src/bridge-core/Encode.cpp
    src/bridge-core/Decode.cpp
    src/bridge-core/MappingConfig.cpp
)

target_include_directories(bridge-core PUBLIC
    ${CMAKE_SOURCE_DIR}/src/bridge-core
)

target_link_libraries(bridge-core PRIVATE
    OpenDIS6
)

# ---------------------------------------------------------------------------
# 5) TestBridge executable with DLL copy
# ---------------------------------------------------------------------------
add_executable(TestBridge
    tests/pdu-replay/TestBridge.cpp
)

target_include_directories(TestBridge PRIVATE
    ${SIMCONNECT_INCLUDE_DIR}
    ${OPENDIS_SOURCE_DIR}/src
)

target_link_libraries(TestBridge PRIVATE
    bridge-core
    OpenDIS6
    "${SIMCONNECT_LIB_DIR}/SimConnect.lib"
)

if(WIN32)
    add_custom_command(TARGET TestBridge POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${SIMCONNECT_LIB_DIR}/SimConnect.dll"
            $<TARGET_FILE_DIR:TestBridge>
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            $<TARGET_FILE:OpenDIS6>
            $<TARGET_FILE_DIR:TestBridge>
        COMMENT "Copying required DLLs"
    )
endif()

# ---------------------------------------------------------------------------
# 6) REST-API server using Crow
# ---------------------------------------------------------------------------
add_executable(rest-api
    src/rest-api/main.cpp
)

target_include_directories(rest-api PRIVATE
    ${CMAKE_SOURCE_DIR}/src/bridge-core
    ${SIMCONNECT_INCLUDE_DIR}
    ${OPENDIS_SOURCE_DIR}/src
    ${CROW_INCLUDE_DIR}
)

target_link_libraries(rest-api PRIVATE
    bridge-core
    OpenDIS6
    crow
)

# ---------------------------------------------------------------------------
# 7) install & packaging rules
# ---------------------------------------------------------------------------
#include(InstallRequiredSystemLibraries)
#install(TARGETS TestBridge rest-api RUNTIME DESTINATION bin)
#install(FILES
#    "$<TARGET_FILE:OpenDIS6>"
#    "${SIMCONNECT_LIB_DIR}/SimConnect.dll"
#    DESTINATION bin
#)
#install(FILES "${CMAKE_SOURCE_DIR}/README.md" DESTINATION .)
#set(CPACK_GENERATOR "ZIP")
#set(CPACK_PACKAGE_NAME "msfs-dis-gateway-test")
#set(CPACK_PACKAGE_VERSION "1.0.0")
#include(CPack)
