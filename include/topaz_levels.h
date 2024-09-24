
#ifndef TOPAZ_TOPAZ_LEVELS_H
#define TOPAZ_TOPAZ_LEVELS_H

#include "topaz.h"    


#ifndef TOPAZ_DEBUG
#define TOPAZ_DEBUG 10
#endif

#ifndef TOPAZ_INFO
#define TOPAZ_INFO 20
#endif

#ifndef TOPAZ_WARN
#define TOPAZ_WARN 30
#endif

#ifndef TOPAZ_ERROR
#define TOPAZ_ERROR 40
#endif



#if TOPAZ_DEBUG >= TOPAZ_MIN_LOGGING_LEVEL
#define LOG_DEBUG(...) LOG_LEVEL_STR("DEBUG", TOPAZ_DEBUG,##__VA_ARGS__)
#else
#define LOG_DEBUG(...)
#endif

#if TOPAZ_INFO >= TOPAZ_MIN_LOGGING_LEVEL
#define LOG_INFO(...) LOG_LEVEL_STR("INFO", TOPAZ_INFO,##__VA_ARGS__)
#else
#define LOG_INFO(...)
#endif

#if TOPAZ_WARN >= TOPAZ_MIN_LOGGING_LEVEL
#define LOG_WARN(...) LOG_LEVEL_STR("WARN", TOPAZ_WARN,##__VA_ARGS__)
#else
#define LOG_WARN(...)
#endif

#if TOPAZ_ERROR >= TOPAZ_MIN_LOGGING_LEVEL
#define LOG_ERROR(...) LOG_LEVEL_STR("ERROR", TOPAZ_ERROR,##__VA_ARGS__)
#else
#define LOG_ERROR(...)
#endif

#endif
        