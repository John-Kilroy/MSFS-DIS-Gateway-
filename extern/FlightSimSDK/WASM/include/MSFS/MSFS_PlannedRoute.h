#ifndef _MSFS_PLANNEDROUTE_H
#define _MSFS_PLANNEDROUTE_H

#ifdef __cplusplus
extern "C" {
#endif

  typedef enum
  {
    FsFlightAltitudeType_None,
    FsFlightAltitudeType_Feet,
    FsFlightAltitudeType_FlightLevel
  } FsFlightAltitudeType;

  typedef enum
  {
    FsEnrouteLegType_Normal,
    FsEnrouteLegType_LatLon,
    FsEnrouteLegType_PointBearingDistance
  } FsEnrouteLegType;

  typedef enum
  {
    FsRunwayIdentifierDesignator_None,
    FsRunwayIdentifierDesignator_Left,
    FsRunwayIdentifierDesignator_Right,
    FsRunwayIdentifierDesignator_Center,
    FsRunwayIdentifierDesignator_Water,
    FsRunwayIdentifierDesignator_A,
    FsRunwayIdentifierDesignator_B
  } FsRunwayIdentifierDesignator;

  typedef enum
  {
    FsRunwayIdentifierNumber_None,
    FsRunwayIdentifierNumber_1,
    FsRunwayIdentifierNumber_2,
    FsRunwayIdentifierNumber_3,
    FsRunwayIdentifierNumber_4,
    FsRunwayIdentifierNumber_5,
    FsRunwayIdentifierNumber_6,
    FsRunwayIdentifierNumber_7,
    FsRunwayIdentifierNumber_8,
    FsRunwayIdentifierNumber_9,
    FsRunwayIdentifierNumber_10,
    FsRunwayIdentifierNumber_11,
    FsRunwayIdentifierNumber_12,
    FsRunwayIdentifierNumber_13,
    FsRunwayIdentifierNumber_14,
    FsRunwayIdentifierNumber_15,
    FsRunwayIdentifierNumber_16,
    FsRunwayIdentifierNumber_17,
    FsRunwayIdentifierNumber_18,
    FsRunwayIdentifierNumber_19,
    FsRunwayIdentifierNumber_20,
    FsRunwayIdentifierNumber_21,
    FsRunwayIdentifierNumber_22,
    FsRunwayIdentifierNumber_23,
    FsRunwayIdentifierNumber_24,
    FsRunwayIdentifierNumber_25,
    FsRunwayIdentifierNumber_26,
    FsRunwayIdentifierNumber_27,
    FsRunwayIdentifierNumber_28,
    FsRunwayIdentifierNumber_29,
    FsRunwayIdentifierNumber_30,
    FsRunwayIdentifierNumber_31,
    FsRunwayIdentifierNumber_32,
    FsRunwayIdentifierNumber_33,
    FsRunwayIdentifierNumber_34,
    FsRunwayIdentifierNumber_35,
    FsRunwayIdentifierNumber_36,
    FsRunwayIdentifierNumber_North,
    FsRunwayIdentifierNumber_Northeast,
    FsRunwayIdentifierNumber_East,
    FsRunwayIdentifierNumber_Southeast,
    FsRunwayIdentifierNumber_South,
    FsRunwayIdentifierNumber_Southwest,
    FsRunwayIdentifierNumber_West,
    FsRunwayIdentifierNumber_Northwest
  } FsRunwayIdentifierNumber;

  typedef enum
  {
    FsApproachProcedureType_None,
    FsApproachProcedureType_Gps,
    FsApproachProcedureType_Vor,
    FsApproachProcedureType_Ndb,
    FsApproachProcedureType_Ils,
    FsApproachProcedureType_Localizer,
    FsApproachProcedureType_Sdf,
    FsApproachProcedureType_Lda,
    FsApproachProcedureType_VorDme,
    FsApproachProcedureType_NdbDme,
    FsApproachProcedureType_Rnav,
    FsApproachProcedureType_Localizer_Backcourse
  } FsApproachProcedureType;

  #pragma pack(push, 1)

  struct FsRouteIcao
  {
    char type;
    char region[3];
    char airport[9];
    char ident[9];
  };
  typedef struct FsRouteIcao FsRouteIcao;

  struct FsRunwayIdentifier
  {
    FsRunwayIdentifierNumber number;
    FsRunwayIdentifierDesignator designator;
  };
  typedef struct FsRunwayIdentifier FsRunwayIdentifier;

  struct FsVisualPattern
  {
    int pattern;
    bool forcePatternSide;
  };
  typedef struct FsVisualPattern;

  struct FsApproachIdentifier
  {
    FsApproachProcedureType type;
    FsRunwayIdentifier runway;
    char suffix[2];
  };
  typedef struct FsApproachIdentifier FsApproachIdentifier;

  struct FsFlightAltitude
  {
    FsFlightAltitudeType type;
    int altitude;
  };
  typedef struct FsFlightAltitude FsFlightAltitude;

  struct FsEnrouteLeg
  {
    FsEnrouteLegType type;
    FsRouteIcao fixIcao;
    char via[9];
	char* name;
	FsFlightAltitude altitude;
    double lat;
    double lon;
    FsRouteIcao pbdReferenceIcao;
    double bearing;
    double distance;
  };
  typedef struct FsEnrouteLeg FsEnrouteLeg;

  struct FsPlannedRoute
  {
    FsRouteIcao departureAirport;
    FsRunwayIdentifier departureRunway;
    char departure[9];
    char departureTransition[9];
    FsVisualPattern departureVisualPattern;
    FsRouteIcao destinationAirport;
    FsRunwayIdentifier destinationRunway;
    char arrival[9];
    char arrivalTransition[9];
    FsApproachIdentifier approach;
    char approachTransition[9];
    FsVisualPattern approachVisualPattern;
    FsFlightAltitude cruiseAltitude;
    bool isVfr;
    int numEnrouteLegs;
    FsEnrouteLeg* enrouteLegs;
  };
  typedef struct FsPlannedRoute FsPlannedRoute;

  #pragma pack(pop)

  typedef long FsRouteRequestId;
  typedef void (*fsPlannedRouteBroadcastCallback)(const FsPlannedRoute* route, void* ctx);
  typedef void (*fsPlannedRouteRequestCallback)(FsRouteRequestId id, void* ctx);

  extern FsPlannedRoute* fsPlannedRouteGetEfbRoute();
  extern bool fsPlannedRouteRegisterForBroadcast(fsPlannedRouteBroadcastCallback callback, void* ctx);
  extern bool fsPlannedRouteUnregisterForBroadcast(fsPlannedRouteBroadcastCallback callback);
  extern bool fsPlannedRouteRegisterForRequest(fsPlannedRouteRequestCallback callback, void* ctx);
  extern bool fsPlannedRouteUnregisterForRequest(fsPlannedRouteRequestCallback callback);
  extern bool fsPlannedRouteRespondToRequest(FsRouteRequestId id, FsPlannedRoute* route);

#ifdef __cplusplus
}
#endif

#endif