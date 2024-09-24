#include "topaz.h"
#include "../include/topaz_levels.h"

int main() {
    set_application_logging_level(20);

    LOG_LEVEL(5, "test")
    LOG_LEVEL(10, "test")
    LOG_LEVEL(15, "test")
    LOG_LEVEL(20, "test")
    LOG_DEBUG("TEST");
    LOG_INFO("TEST");
    LOG_WARN("TEST");
    LOG_ERROR("TEST");
}
