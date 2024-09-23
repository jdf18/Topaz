cmake_minimum_required(VERSION 3.10)
project(Topaz VERSION 1.0.0)

#set(CMAKE_C_STANDARD 11)

add_library(Topaz STATIC
        src/topaz.c
        include/topaz.h
)

target_include_directories(Topaz PUBLIC include)

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