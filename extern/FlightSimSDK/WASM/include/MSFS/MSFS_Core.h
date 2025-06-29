//-----------------------------------------------------------------------------
//
// Copyright (c) Microsoft Corporation. All Rights Reserved.
//
//-----------------------------------------------------------------------------

#ifndef _MSFS_CORE_H
#define _MSFS_CORE_H

// id of the user's sim object
#define SIM_OBJECT_ID_USER 0ul

#ifdef __cplusplus
extern "C" {
#endif

#pragma pack(push, 4)

// Useful struct to define various vector types
#pragma region vector
	typedef struct
	{
		union
		{
			float rgba[4];
			struct {
				float r, g, b, a;
			};
		};
	} FsColor;

	typedef struct
	{ 
		float x, y; 
	} FsVec2f;

	typedef struct
	{ 
		double x, y; 
	} FsVec2d;

	typedef struct
	{ 
		float x, y, z;
	} FsVec3f;

	typedef struct
	{
		double x, y, z;
	} FsVec3d;
#pragma endregion

	/// Execution context of a MSFS Callback, this context is different for each Gauge, System, ...
	typedef unsigned long long FsContext;

	typedef int FsTextureId;
	typedef int FsRenderImageFlags;
	typedef unsigned long FsSimObjId;
	typedef unsigned long long FsCRC;

	/// Some variable are indexed with parameters.
	/// And some Events can receive various parameters
	/// Parameters are shared through array of variant : FsVarParamArray
	/// The variant FsVarParamVariant contains a value and its type
	/// Finally eFsVarParamType enumerates all possible types
#pragma region VarParam
	enum eFsVarParamType : unsigned char
	{
		FsVarParamTypeInteger,
		FsVarParamTypeString,
		FsVarParamTypeCRC,
	};

	struct FsVarParamVariant
	{
		eFsVarParamType type;
		union {
			unsigned int	intValue;
			const char*		stringValue;
			FsCRC			CRCValue;
		};
	};

	struct FsVarParamArray
	{
		unsigned int size = 0;
		FsVarParamVariant* array = nullptr;

	};
#pragma endregion

#pragma pack(pop)

#ifdef __cplusplus
}
#endif

#endif