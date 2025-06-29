//-----------------------------------------------------------------------------
//
// Copyright (c) Microsoft Corporation. All Rights Reserved.
//
//-----------------------------------------------------------------------------

#pragma once

#ifndef MSFS_IO_H
#define MSFS_IO_H

#pragma once

#pragma pack(push, 4)

typedef unsigned long long FsIOFile;
#define FS_IO_ERROR_FILE 0

enum FsIOErr : unsigned int
{
	FsIOErr_Success = 0,
	FsIOErr_BadParams,					// There is error in the paramters given to the function
	FsIOErr_FileNotFound,
	FsIOErr_AccessNotAllowed,           // Access to the file is not allowed. For example, the file is in another package
	FsIOErr_FileNotOpened,              // The file is not opened, but the operation need a opened file
	FsIOErr_ReadNotAllowed,             // The read to the file is imposssble. For example the file is not opened with the right flags
	FsIOErr_PartialReadImpossible,      // For the file, it is impossible to read just a part of the file
	FsIOErr_OperationImpossible,        // Impossible to do the operation. For example a open/read/write is processing and trying to close the file

	FsIOErr_UnknownError = 0xFFFFFFFF
};

enum _FsIOOpenFlags : unsigned int
{
	FsIOOpenFlag_NONE = 0,
	FsIOOpenFlag_RDONLY = 1 << 0,		// Read only

	FsIOOpenFlagsMax // Keep it at the end
};

typedef unsigned int FsIOOpenFlags;

typedef void(*FsIOFileOpenCallback)(FsIOFile file, void* pUserData);

typedef void(*FsIOFileReadCallback)(FsIOFile file, char* outBuffer, int byteOffset, int bytesRead, void* pUserData);

#pragma pack(pop)


#ifdef __cplusplus
extern "C" {
#endif // __cplusplus
	FsIOFile fsIOOpen(const char* path, FsIOOpenFlags flags, FsIOFileOpenCallback callback, void* pUserData);
	FsIOErr fsIORead(FsIOFile file, char* outBuffer, int byteOffset, int bytesToRead, FsIOFileReadCallback callback, void* pUserData);
	FsIOFile fsIOOpenRead(const char* path, FsIOOpenFlags flags, int byteOffset, int bytesToRead, FsIOFileReadCallback callback, void* pUserData);
	FsIOErr fsIOClose(FsIOFile file);

	bool fsIOIsOpened(FsIOFile file);
	bool fsIOInProgress(FsIOFile file);
	bool fsIOIsDone(FsIOFile file);
	bool fsIOHasError(FsIOFile file);
	FsIOErr fsIOGetLastError(FsIOFile file);
	unsigned long long fsIOGetFileSize(FsIOFile file);
#ifdef __cplusplus
}
#endif // __cplusplus

#endif // !MSFS_IO_H
