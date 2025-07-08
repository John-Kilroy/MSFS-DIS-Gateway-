cmake_minimum_required(VERSION 3.18)
project(msfs-dis-bridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

# ---------------------------------------------------------------------------
# 1) open‑DIS (DIS 6) submodule - now pointing to the correct folder
# ---------------------------------------------------------------------------
add_subdirectory(extern/open-dis-cpp
                 ${CMAKE_BINARY_DIR}/open-dis-build)

# ---------------------------------------------------------------------------
# 2) SimConnect SDK
# ---------------------------------------------------------------------------
set(SIMCONNECT_INCLUDE_DIR ${CMAKE_SOURCE_DIR}/extern/SimConnect/include)
set(SIMCONNECT_LIB_DIR     ${CMAKE_SOURCE_DIR}/extern/SimConnect/lib)

include_directories(${SIMCONNECT_INCLUDE_DIR})
link_directories(${SIMCONNECT_LIB_DIR})

# ---------------------------------------------------------------------------
# 3) bridge-core library
# ---------------------------------------------------------------------------
add_library(bridge-core
    src/bridge-core/Encode.cpp
    src/bridge-core/Decode.cpp
    src/bridge-core/MappingConfig.cpp
)

target_include_directories(bridge-core PUBLIC
    ${CMAKE_SOURCE_DIR}/src/bridge-core
    ${CMAKE_SOURCE_DIR}/extern/open-dis-cpp/src
)

target_link_libraries(bridge-core PRIVATE
    OpenDIS6         # Updated to match open-dis-cpp target name
)

# ---------------------------------------------------------------------------
# 4) TestBridge executable
# ---------------------------------------------------------------------------
add_executable(TestBridge
    tests/pdu-replay/TestBridge.cpp
)

target_include_directories(TestBridge PRIVATE
    ${SIMCONNECT_INCLUDE_DIR}
)

target_link_libraries(TestBridge PRIVATE
    bridge-core
    SimConnect
)

# ---------------------------------------------------------------------------
# 5) (Optional) install rules
# ---------------------------------------------------------------------------
# install(TARGETS bridge-core TestBridge EXPORT msfs_dis_bridge)
# install(DIRECTORY src/bridge-core/ DESTINATION include/bridge-core)
