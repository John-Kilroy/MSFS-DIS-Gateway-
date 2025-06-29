#pragma once

#ifndef MSFS_EVENTS_H
#define MSFS_EVENTS_H

#include "MSFS_Core.h"
#include "Types/MSFS_EventsEnum.h"

#pragma pack(push, 4)
typedef int FsEventId;
typedef void(*FsEventsKeyEventHandler)(FsEventId eventId, FsVarParamArray* param, void* pUserParam);
#pragma pack(pop)

#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

	void fsEventsTriggerKeyEvent(FsEventId eventId, FsVarParamArray param);
	void fsEventsRegisterKeyEventHandler(FsEventsKeyEventHandler handler, void* pUserParam);
	void fsEventsUnregisterKeyEventHandler(FsEventsKeyEventHandler handler, void* pUserParam);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // !MSFS_EVENTS_H
