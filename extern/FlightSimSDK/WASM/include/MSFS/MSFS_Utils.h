//-----------------------------------------------------------------------------
//
// Copyright (c) Microsoft Corporation. All Rights Reserved.
//
//-----------------------------------------------------------------------------

#pragma once

#ifndef MSFS_UTILS_H
#define MSFS_UTILS_H

#include "MSFS_Core.h"

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

	/// <summary>
	/// Get the CRC of a given string.
	/// </summary>
	FsCRC fsUtilsGetStrCRC(const char* str);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // !MSFS_UTILS_H
