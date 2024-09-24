cmake_minimum_required(VERSION 3.10)
project(Topaz VERSION 1.0.0)

#set(CMAKE_C_STANDARD 11)

set(GENERATED_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/gen)

# * Process the configuration file
# This is for reading the config file, outputting the values to cmake, and setting them as C macro directives
execute_process(
        COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/src/output_config_directives.py logging_conf.json
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
        # Store the text output into the variable PYTHON_OUTPUT
        OUTPUT_VARIABLE PYTHON_OUTPUT
        ERROR_VARIABLE script_error
        RESULT_VARIABLE script_result
        OUTPUT_STRIP_TRAILING_WHITESPACE
)
if(script_result EQUAL 0)
    message(STATUS "Python script executed successfully: ${PYTHON_OUTPUT}")

    # Split the resulting string at each semicolon and split up the resulting list
    string(REGEX MATCHALL "[^;]+" PYTHON_VALUES_LIST "${PYTHON_OUTPUT}")

    list(GET PYTHON_VALUES_LIST 0 RUNTIME_LEVEL_EVAL)
    list(GET PYTHON_VALUES_LIST 1 MINIMUM_LEVEL)

    message(STATUS "TOPAZ_RUNTIME_LEVEL_CHANGE: ${RUNTIME_LEVEL_EVAL}")
    message(STATUS "TOPAZ_MIN_LOGGING_LEVEL: ${MINIMUM_LEVEL}")

    # Set the C macro directives
    add_definitions(-DTOPAZ_RUNTIME_LEVEL_CHANGE=${RUNTIME_LEVEL_EVAL})
    add_definitions(-DTOPAZ_MIN_LOGGING_LEVEL=${MINIMUM_LEVEL})
else()
    # If any errors, return
    message(FATAL_ERROR "Python script failed: ${script_error}")
endif()

# Generate the custom print function in /gen/logging_printf.c and the levels macros
add_custom_command(
        OUTPUT ${GENERATED_BINARY_DIR}/logging_printf.c ${GENERATED_BINARY_DIR}/topaz_levels.h
        DEPENDS ${CMAKE_SOURCE_DIR}/logging_conf.json
        COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/src/generate_source_code.py ${CMAKE_SOURCE_DIR}/logging_conf.json ${GENERATED_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${GENERATED_BINARY_DIR}
        COMMENT "generating src/generated_printf_code.c"
)

# * ==== COMPILE TOPAZ LIBRARY =====

add_library(Topaz STATIC
        src/topaz.c
        gen/logging_printf.c
)

target_include_directories(Topaz PRIVATE ${GENERATED_BINARY_DIR})
target_include_directories(Topaz PUBLIC include)

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
