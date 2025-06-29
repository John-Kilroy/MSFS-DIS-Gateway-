#pragma once

#ifndef SIM_PARAM_ARRAY_HELPER
#define SIM_PARAM_ARRAY_HELPER

#include <MSFS\MSFS_Core.h>
#include <cstring>
#include <cstdarg>
#include <stdio.h>
#include <stdlib.h>

/// <summary>
/// Helper to create a FsSimParamArray.
/// The first argument specify the type of the param :
///		- 'c' : crc (FsSimCRC / unsigned long long)
///		- 's' : string (const char*)
///		- 'i' : index (unsigned int)
/// 
/// Example : FsCreateParamArray("iics", 0, 1, 123456, "Hey");
/// 0 and 1 are index, 123456 a CRC and "Hey" a string.
/// 
/// /!\ DO NOT FORGET TO FREE PARAM ARRAY /!\
/// </summary>
static FsVarParamArray FsCreateParamArray(const char* fmt, ...)
{
	size_t nArgs = strlen(fmt);

	FsVarParamArray result;
	result.size = nArgs;
	result.array = (FsVarParamVariant*)malloc(nArgs * sizeof(FsVarParamVariant));

	va_list args;
	va_start(args, fmt);

	for (int i = 0; i < nArgs; ++i)
	{
		if (fmt[i] == 'c')
		{
			result.array[i].type = FsVarParamTypeCRC;
			result.array[i].CRCValue = va_arg(args, FsCRC);
		}
		else if (fmt[i] == 's')
		{
			result.array[i].type = FsVarParamTypeString;
			result.array[i].stringValue = va_arg(args, const char*);
		}
		else if (fmt[i] == 'i')
		{
			result.array[i].type = FsVarParamTypeInteger;
			result.array[i].intValue = va_arg(args, unsigned int);
		}
		else
		{
			fprintf(stderr, "Unknown format for FsCreateParamArray (%c)", fmt[i]);
			free(result.array);
			result.size = 0;
			result.array = nullptr;
			return result;
		}
	}

	va_end(args);

	return result;
}

static void FsDestroyParamArray(FsVarParamArray* pParamArray)
{
	if (pParamArray->size != 0)
	{
		free(pParamArray->array);
	}
	pParamArray->size = 0;
	pParamArray->array = nullptr;

}

#endif // SIM_PARAM_ARRAY_HELPER
