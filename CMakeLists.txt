cmake_minimum_required(VERSION 3.17)
project(msfs-dis-bridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Output folders
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)


set(GEOLIB_SOURCE_DIR ${CMAKE_SOURCE_DIR}/extern/GeographicLib-2.5)
set(GEOLIB_BUILD_DIR  ${CMAKE_BINARY_DIR}/geographiclib-build)
set(GEOLIB_INSTALL_DIR ${GEOLIB_SOURCE_DIR}/install)
set(GEOLIB_INCLUDE_DIR ${GEOLIB_INSTALL_DIR}/include)
set(GeographicLib_DIR ${GEOLIB_INSTALL_DIR}/lib/cmake/GeographicLib)
find_package(GeographicLib CONFIG REQUIRED)
add_subdirectory(${GEOLIB_SOURCE_DIR} ${GEOLIB_BUILD_DIR})
include_directories (${GeographicLib_INCLUDE_DIRS})
#add_library(GeographicLib STATIC IMPORTED)
#find_library()

if (NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  # Set a default build type for single-configuration cmake generators
  # if no build type is set.
  set (CMAKE_BUILD_TYPE "Release")
endif ()

# ----------------------------------------------------------------------------
# 1) SimConnect SDK (headers + libs must already be in extern/FlightSimSDK)
# ----------------------------------------------------------------------------
set(SIMCONNECT_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/SimConnect SDK/include")
set(SIMCONNECT_LIB_DIR     "${CMAKE_SOURCE_DIR}/extern/FlightSimSDK/SimConnect SDK/lib")
include_directories(${SIMCONNECT_INCLUDE_DIR})

# ----------------------------------------------------------------------------
# 2) open‑DIS (DIS 6) submodule
# ----------------------------------------------------------------------------
set(OPENDIS_SOURCE_DIR ${CMAKE_SOURCE_DIR}/extern/open-dis-cpp)
set(OPENDIS_BUILD_DIR  ${CMAKE_BINARY_DIR}/open-dis-build)
add_subdirectory(${OPENDIS_SOURCE_DIR} ${OPENDIS_BUILD_DIR})
include_directories(${OPENDIS_SOURCE_DIR}/src)

# ----------------------------------------------------------------------------
# 3) Asio (header‑only) for Crow
# ----------------------------------------------------------------------------
set(ASIO_STANDALONE ON)
set(ASIO_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/extern/asio/asio/include")

# ----------------------------------------------------------------------------
# 4) Crow HTTP framework submodule
# ----------------------------------------------------------------------------
set(CROW_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/extern/crow/include")



# ----------------------------------------------------------------------------
# 5) bridge-core library (static)
# ----------------------------------------------------------------------------
add_library(bridge-core STATIC
    src/bridge-core/Encode.cpp
    src/bridge-core/Decode.cpp
    src/bridge-core/MappingConfig.cpp
)
target_include_directories(bridge-core PUBLIC
    ${CMAKE_SOURCE_DIR}/src/bridge-core
)
target_link_libraries(bridge-core PRIVATE OpenDIS6)

# ----------------------------------------------------------------------------
# 6) TestBridge executable
# ----------------------------------------------------------------------------
add_executable(TestBridge
    tests/pdu-replay/TestBridge.cpp
)
target_include_directories(TestBridge PRIVATE
    ${SIMCONNECT_INCLUDE_DIR}
    ${OPENDIS_SOURCE_DIR}/src
    ${GEOLIB_INCLUDE_DIR}
)
target_link_libraries(TestBridge PRIVATE
    bridge-core
    OpenDIS6
    GeographicLib
    "${SIMCONNECT_LIB_DIR}/SimConnect.lib"
)

# ----------------------------------------------------------------------------
# 7) REST‑API server using Crow
# ----------------------------------------------------------------------------
add_executable(rest-api
    src/rest-api/main.cpp
)

target_include_directories(rest-api PRIVATE
    ${CMAKE_SOURCE_DIR}/src/bridge-core   
    ${SIMCONNECT_INCLUDE_DIR}              
    ${OPENDIS_SOURCE_DIR}/src    
    ${GEOLIB_INCLUDE_DIR}
    ${CROW_INCLUDE_DIR}                   
    ${ASIO_INCLUDE_DIR} 
)

target_compile_definitions(rest-api PRIVATE
    ASIO_STANDALONE
)

target_link_libraries(rest-api PRIVATE
    bridge-core
    OpenDIS6
    "${SIMCONNECT_LIB_DIR}/SimConnect.lib"
    GeographicLib
)

if (WIN32)
    add_custom_command(TARGET TestBridge POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            "${SIMCONNECT_LIB_DIR}/SimConnect.dll"   $<TARGET_FILE_DIR:TestBridge>
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
            $<TARGET_FILE:OpenDIS6>                  $<TARGET_FILE_DIR:TestBridge>
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        "${GEOLIB_SOURCE_DIR}/build/bin/Debug/GeographicLib_d.dll"                  $<TARGET_FILE_DIR:TestBridge>
        COMMENT "Copying required DLLs"
    )
endif()
# ----------------------------------------------------------------------------
# 8) Packaging (CPack ZIP with both binaries + DLLs + README)
# ----------------------------------------------------------------------------
include(InstallRequiredSystemLibraries)
install(TARGETS TestBridge rest-api RUNTIME DESTINATION bin)
install(FILES
    "$<TARGET_FILE:OpenDIS6>"
    "${SIMCONNECT_LIB_DIR}/SimConnect.dll"
    DESTINATION bin
)
install(FILES "${CMAKE_SOURCE_DIR}/README.md" DESTINATION .)
set(CPACK_GENERATOR "ZIP")
set(CPACK_PACKAGE_NAME "msfs-dis-gateway-test")
set(CPACK_PACKAGE_VERSION "1.0.0")
include(CPack)
