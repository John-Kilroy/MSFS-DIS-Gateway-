//-----------------------------------------------------------------------------
//
// Copyright (c) Microsoft Corporation. All Rights Reserved.
//
//-----------------------------------------------------------------------------

#ifndef MSFS_SIM_H
#define MSFS_SIM_H

#include "MSFS_Core.h"

#pragma pack(push, 4)

typedef int FsSimVarId;
typedef int FsNamedVarId;
typedef int FsUnitId;
typedef int FsCustomSimVarId;

typedef unsigned int FsVarError;
#define	FS_VAR_ERROR_NONE				0x00000000
#define	FS_VAR_ERROR_FAIL				0xffffffff
#define	FS_VAR_ERROR_BAD_DATA			0x00000002
#define	FS_VAR_ERROR_NOT_SUPPORTED		0x00000003
#define	FS_VAR_ERROR_INVALID_ARGS		0x00000004

enum eFsSimCustomSimVarScope : unsigned char
{
	FsSimCustomSimVarScopeSim,
	FsSimCustomSimVarScopeComponent,
	FsSimCustomSimVarScopeHierarchy,
};

#pragma pack(pop)

#ifdef __cplusplus
extern "C" {
#endif
FsUnitId fsVarsGetUnitId(const char* unitName);

FsSimVarId fsVarsGetAircraftVarId(const char* simVarName);
FsVarError fsVarsAircraftVarGet(FsSimVarId simvar, FsUnitId unit, FsVarParamArray param, double* result);
FsVarError fsVarsAircraftVarSet(FsSimVarId simvar, FsUnitId unit, FsVarParamArray param, double value);

FsNamedVarId fsVarsGetRegisteredNamedVarId(const char* name);
FsNamedVarId fsVarsRegisterNamedVar(const char* name);
void fsVarsNamedVarGet(FsNamedVarId var, FsUnitId unit, double* result);
void fsVarsNamedVarSet(FsNamedVarId var, FsUnitId unit, double value);

FsCustomSimVarId fsVarsRegisterCustomSimVar(const char* name, const char* componentPath, eFsSimCustomSimVarScope scope);
FsVarError fsVarsCustomSimVarGet(FsCustomSimVarId var, FsUnitId unit, double* result);
FsVarError fsVarsCustomSimVarSet(FsCustomSimVarId var, FsUnitId unit, double value);

#ifdef __cplusplus
}
#endif


#endif // MSFS_SIM_H
