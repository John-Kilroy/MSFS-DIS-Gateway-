//-----------------------------------------------------------------------------
//
// Copyright (c) Microsoft Corporation. All Rights Reserved.
//
//-----------------------------------------------------------------------------

#ifndef _MSFS_AIRPORT_CONTEXT
#define _MSFS_AIRPORT_CONTEXT

#ifdef __cplusplus
extern "C" {
#endif

#define WASM_AIRPORT_ICAO_SIZE 18

#pragma pack(push, 4)
typedef struct
{
    char ICAO[WASM_AIRPORT_ICAO_SIZE];
} FsWasmAirportContext;


#pragma pack(pop)

#ifdef __cplusplus
}
#endif

#endif