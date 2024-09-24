cmake_minimum_required(VERSION 3.10)
project(Topaz VERSION 1.0.0)

#set(CMAKE_C_STANDARD 11)

set(GENERATED_BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR}/gen)


# * ==== COMPILE TOPAZ LIBRARY =====
add_library(Topaz STATIC
        src/topaz.c
        gen/generated_printf_code.c
)

add_custom_command(
        OUTPUT ${GENERATED_BINARY_DIR}/generated_printf_code.c ${GENERATED_BINARY_DIR}/topaz_levels.h
        DEPENDS ${CMAKE_SOURCE_DIR}/logging_conf.json
        COMMAND python3 ${CMAKE_CURRENT_SOURCE_DIR}/src/generate_printf.py ${CMAKE_SOURCE_DIR}/logging_conf.json ${GENERATED_BINARY_DIR} ${CMAKE_CURRENT_SOURCE_DIR}
        WORKING_DIRECTORY ${GENERATED_BINARY_DIR}
        COMMENT "generating src/generated_printf_code.c"
)

target_include_directories(Topaz PUBLIC include)
target_include_directories(Topaz PUBLIC ${GENERATED_BINARY_DIR})

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

# * ===== TESTING =====

enable_testing()

# Create an executable for testing
add_executable(test_topaz tests/test_topaz.c)

# Link the Topaz library to the test executable
target_link_libraries(test_topaz PRIVATE Topaz)

# Add the test to CTest
add_test(NAME TestTopaz COMMAND test_topaz)
