#pragma once

#ifndef MSFS_GAUGE_CONTEXT_H
#define MSFS_GAUGE_CONTEXT_H

#pragma pack(push, 4)

	struct sGaugeInstallData
	{
		int iSizeX;
		int iSizeY;
		char *strParameters;
	};

	struct sGaugeDrawData
	{
		double mx;
		double my;
		double t;
		double dt;
		int winWidth;
		int winHeight;
		int fbWidth;
		int fbHeight;
	};

#pragma pack(pop)

#endif // MSFS_GAUGE_CONTEXT_H
