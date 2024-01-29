#pragma once 

#include <Preferences.h>

//structure for stationlist
typedef struct {
  char url[100];  //stream url
  char name[100]; //stations name
} Station;

#define STATIONS 20 //number of available stations

//station list (stations can now be modified by webinterface)
extern Station stationlist[STATIONS];

//instances of prefernces
extern Preferences pref;
extern Preferences sender;

//global variables
extern uint8_t curStation;   //index for current selected station in stationlist
extern uint8_t actStation;   //index for current station in station list used for streaming 
extern uint32_t lastchange;  //time of last selection change