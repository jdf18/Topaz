#ifndef TOPAZ_TOPAZ_H
#define TOPAZ_TOPAZ_H

// * To use this library, add the following lines to CMakeLists.txt:
// e.g. add_subdirectory(path/to/topaz)
//      target_link_libraries(my_app PRIVATE topaz)

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
#include <time.h>

#ifndef __FILENAME__
#define __FILENAME__ (strrchr(__FILE__, '\\') ? strrchr(__FILE__, '\\') + 1 : __FILE__)
#endif

#define STRINGIFY(x) #x
#define TOSTRING(x) STRINGIFY(x)


// * Set the default time format
#ifndef TOPAZ_TIME_FORMAT
#define TOPAZ_TIME_FORMAT "%Y-%m-%d %H:%M:%S"
#endif

// * Set default value for runtime logging level changes
#ifndef TOPAZ_RUNTIME_LEVEL_CHANGE
#define TOPAZ_RUNTIME_LEVEL_CHANGE 1
#endif

// Runtime logging level
#if (TOPAZ_RUNTIME_LEVEL_CHANGE == 1)
extern int application_logging_level;
#endif
void set_application_logging_level(int level);

// * Set minimum logging level at compile time
#ifndef TOPAZ_MIN_LOGGING_LEVEL
#define TOPAZ_MIN_LOGGING_LEVEL 30
#endif

// * Logging functions
void log_message_level(int level, const char* file, char* line, const char* func);
void log_message(const char* code, int level, const char* file, char* line, const char* func);

// * Logging macros
#if TOPAZ_RUNTIME_LEVEL_CHANGE == 1
#define LOG_LEVEL_STR(code, log_level, ...) \
if (log_level >= application_logging_level) { \
    log_message(code, log_level, __FILENAME__, TOSTRING(__LINE__), __FUNCTION__); \
    printf(__VA_ARGS__);    \
    printf("\n");                                \
}
#define LOG_LEVEL(log_level, ...) \
if (log_level >= application_logging_level) { \
    if (log_level < TOPAZ_MIN_LOGGING_LEVEL) { printf("META: This log has a level lower than the MIN_LOGGING_LEVEL. Some logs may be missing.\n"); } \
    log_message_level(log_level, __FILENAME__, TOSTRING(__LINE__), __FUNCTION__); \
    printf(__VA_ARGS__);    \
    printf("\n");\
}
#else
#define LOG_LEVEL_STR(code, log_level, ...) \
log_message(code, log_level, __FILENAME__, TOSTRING(__LINE__), __FUNCTION__); \
printf(__VA_ARGS__);    \
printf("\n");

#define LOG_LEVEL(log_level, ...) \
log_message_level(log_level, __FILENAME__, TOSTRING(__LINE__), __FUNCTION__); \
printf(__VA_ARGS__);    \
printf("\n");
#endif

#endif //TOPAZ_TOPAZ_H
