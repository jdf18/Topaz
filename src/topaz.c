#include "../include/topaz.h"

Level application_logging_level = WARN;

void set_application_logging_level(Level level) {
    application_logging_level = level;
}

static void current_time(char* buffer, size_t len) {
    time_t now = time(NULL);
    struct tm *t = localtime(&now);
    strftime(buffer, len, "%Y-%m-%d %H:%M:%S", t);
}

void log_message(Level level, const char* file, int line, const char* func, char* format, ...) {
    va_list args;
    va_start(args, format);

    if (level < application_logging_level) {
        return;
    }
    char time_buffer[20];
    current_time(time_buffer, sizeof(time_buffer));

    char line_buffer[10];
    sprintf(line_buffer, "%d", line);

    char empty = '\0';
    const char* values[5];
    values[0] = &empty;
    values[1] = &empty;
    values[2] = &empty;
    values[3] = &empty;
    values[4] = &empty;

    if (LOG_FORMAT_FILE_INDEX != 0) {
        values[LOG_FORMAT_FILE_INDEX - 1] = file;
    }
    if (LOG_FORMAT_LINE_INDEX != 0) {
        values[LOG_FORMAT_LINE_INDEX - 1] = line_buffer;
    }
    if (LOG_FORMAT_FUNCTION_INDEX != 0) {
        values[LOG_FORMAT_FUNCTION_INDEX - 1] = func;
    }
    if (LOG_FORMAT_TIME_INDEX != 0) {
        values[LOG_FORMAT_TIME_INDEX - 1] = time_buffer;
    }

    printf(LOG_FORMAT, values[0], values[1], values[2], values[3], values[4]);
    vprintf(format, args);
    printf("\n");
}
