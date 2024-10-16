cmake_minimum_required(VERSION 3.10)
project(Topaz VERSION 1.0.0)
set (TOPAZ_LIBRARY_VERSION "0.1.0")

set(GENERATED_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/gen)

if (NOT DEFINED TOPAZ_CONFIG_FILE)
    set(TOPAZ_CONFIG_FILE ${CMAKE_SOURCE_DIR}/logging_conf.json)
endif()
set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS TOPAZ_CONFIG_FILE)

# When using makefiles, it can error if this directory is not present
file(MAKE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/gen)

# * ===== PROCESS CONFIGURATION FILE =====
# This is done during configuration time, so CMake must be run if the configuration file changes.

include(config.cmake)
topaz_conf_parse_file(${TOPAZ_CONFIG_FILE} topaz_configuration)

message("Configuration file version: " ${TOPAZ_CONFIG_VER})
message("Topaz library version: " ${TOPAZ_LIBRARY_VERSION})

if(NOT "${TOPAZ_CONFIG_VER}" VERSION_LESS_EQUAL "${TOPAZ_LIBRARY_VERSION}")
    message(FATAL_ERROR "Configuration file version ${TOPAZ_CONFIG_VER} is greater than the library version ${TOPAZ_LIBRARY_VERSION}. \
    Please change the configuration file or use a newer version of the library.")
else()
    message(STATUS "Configuration file version is compatible with the library version.")
endif()

# * ==== COMPILE TOPAZ LIBRARY =====

add_library(Topaz STATIC
        src/topaz.c
        gen/logging_printf.c
)

target_include_directories(Topaz PRIVATE ${GENERATED_BINARY_DIR})
target_include_directories(Topaz PUBLIC include)

# Set the C macro directives for source files linking to this project
target_compile_definitions(Topaz PUBLIC TOPAZ_RUNTIME_LEVEL_CHANGE=${RUNTIME_LEVEL_EVAL})
target_compile_definitions(Topaz PUBLIC TOPAZ_MIN_LOGGING_LEVEL=${MINIMUM_LEVEL})

# * ===== LIBRARY INSTALLATION =====

set(CPACK_GENERATOR ZIP TGZ)

# Install the library
install(TARGETS Topaz
        ARCHIVE DESTINATION lib
        COMPONENT libraries
)
install(FILES include/topaz.h
        DESTINATION include
        COMPONENT headers
)

include(CPack)

# * ===== TESTING EXECUTABLE =====

enable_testing()

# Create an executable for testing
add_executable(test_topaz tests/test_topaz.c)

# Link the Topaz library to the test executable
target_link_libraries(test_topaz PRIVATE Topaz)

# Add the test to CTest
add_test(NAME TestTopaz COMMAND test_topaz)
