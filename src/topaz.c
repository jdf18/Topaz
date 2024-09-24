#ifndef TOPAZ_TOPAZ_C
#define TOPAZ_TOPAZ_C

#include "../include/topaz.h"
#include "custom_printf.h"
#include "levels_lut.h"

#if TOPAZ_RUNTIME_LEVEL_CHANGE == 1
int application_logging_level = TOPAZ_MIN_LOGGING_LEVEL;
#endif

// * Define function to set the logging level during runtime
// If runtime level evaluation is disabled, set the function to do nothing
void set_application_logging_level(int level) {
#if (TOPAZ_RUNTIME_LEVEL_CHANGE == 1)
    application_logging_level = level;
#endif
}


void log_message_level(int level, const char* file, char* line, const char* func) {
    const char* lut_code;
    if (level < TOPAZ_LUT_SIZE) {
        lut_code = lut[level];
        // If first char != 0, then entry exists in LUT
        if (*lut_code != 0) {
            log_message(lut_code, level, file, line, func);
            return;
        }
    }

    char code[2];
    sprintf(code, "%d", level);
    log_message(code, level, file, line, func);
}

void log_message(const char* code, int level, const char* file, char* line, const char* func) {
    generated_print_strings(code, file, func, line);
}

#endif